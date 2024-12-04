from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, text, and_, func
from app.config.database import get_db
from typing import Optional, List
from fastapi.templating import Jinja2Templates

from app.api.v1.models.BookingModel import BookingTags
from app.api.v1.schemas.BookingSchema import TagListSchema, CreateTagMailSchema, TestingMailSchema
from app.api.v1.utils.mails import SendTagMailToApprove, SendTagListMailToStudents, SendListConfMailToMentor, SendTestingMailToMentor
from app.api.v1.utils.helper import EncriptMe, DecriptMe, cleanCommaValues, cleanCommaIntValues

from app.api.v1.models.BookingModel import BookingTagMail, BookingTagStudent
from app.api.v1.models.UserModel import User
from app.api.v1.schemas.UserSchema import UserListSchema

from app.api.v1.utils.helper import cleanCommaIntValues
from app.api.v1.utils.common import GetStudentEmailListForTagMail

templates = Jinja2Templates(directory="app/api/v1/templates")

router = APIRouter()

@router.get("/tag_list", response_model=List[TagListSchema])
async def tag_list(db:Session=Depends(get_db)):
    return db.query(BookingTags).order_by(desc(BookingTags.id)).limit(100).all()

@router.post("/create_tag_mail_list")
async def create_tag_mail_list(compose:CreateTagMailSchema, background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    if compose.mentor_id != 0:
        from_id = compose.mentor_id
    else:
        from_id = compose.manager_id

    from_user = db.query(User).filter(User.id == from_id).first()
    if from_user:

        to_tag_idz = cleanCommaValues(compose.to_tags)
        if compose.avoid_tags:
            avoid_tag_idz = cleanCommaValues(compose.avoid_tags)
        else:
            avoid_tag_idz = ''
        
        to_tags = db.query(BookingTags).filter(BookingTags.id.in_(to_tag_idz)).all()
        to_tag_list = [tag.tag_name for tag in to_tags]
        to_tas_str = ', '.join(to_tag_list)

        avoid_tag_str = ''
        if avoid_tag_idz:
            avoid_tags = db.query(BookingTags).filter(BookingTags.id.in_(avoid_tag_idz)).all()
            avoid_tag_list = [tag.tag_name for tag in avoid_tags]
            avoid_tag_str = ', '.join(avoid_tag_list)

        
        #print(from_user.__dict__)
        obj = BookingTagMail(to_tags=compose.to_tags, avoid_tags=compose.avoid_tags, subject = compose.subject, body = compose.body, mentor_id = compose.mentor_id, manager_id = compose.manager_id, status = 0)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        list_id = EncriptMe(str(obj.id))
        list_id = list_id.decode('utf-8')
        #SendTagMailToApprove(list_id, from_user.fullName, compose.subject, compose.body, to_tas_str, avoid_tag_str)
        mentor_detail = {"id": from_user.id, "fullName": from_user.fullName}
        background_tasks.add_task(SendTagMailToApprove, list_id, mentor_detail, compose.subject, compose.body, to_tas_str, avoid_tag_str, compose, db)
        print("###########################################################Mentor++++++++++++++")
        print(list_id)
        return {"code":1, "message":"Mail sent for approval"}
    else:
        return {"code":0, "message":"Mentor not found"}
    
@router.post('/approve_reject_tag_mail')
async def approve_reject_tag_mail(q: str, s:int, background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    id = DecriptMe(q)
    print("+++++++++++++++++++++++++++++++++YYYYYYYYYYYYYYYYYYYYYYY+++++++++++++++++++++++++++++++")
    print(id)
    obj = db.query(BookingTagMail).filter(BookingTagMail.id == id).first()
    if obj.status == 0:
        print(obj)
        obj.status = s
        obj.approved_rejected_at = func.now()
        db.add(obj)
        db.commit()

        if s == 1:
            background_tasks.add_task(SendTagListMailToStudents, id, db)
            background_tasks.add_task(SendListConfMailToMentor, id, db)
            return {"code":1, "action":1, "message":"Mail sent for approval"}
        else:
            return {"code":1, "action":2, "message":"Mail rejected successfully"}
    else:
        return {"code":0, "action":3, "message":"This link has expired"}

@router.get("/get_sent_mail_students", response_class=HTMLResponse)
def get_sent_mail_students(request: Request, list_id:int, db:Session = Depends(get_db)):
    list = db.query(BookingTagMail).filter(BookingTagMail.id == list_id).first()
    
    student_ids = cleanCommaIntValues(list.student_ids)
    students = db.query(User).filter(User.id.in_(student_ids)).all()
    return templates.TemplateResponse("bookings/sent_mail_students.html", {"request":request, "students":students})

@router.get("/get_compose_students", response_class=HTMLResponse)
def get_compose_students(request: Request, tags:str, avoid:str, mentor=int, db:Session = Depends(get_db)):
    student_data = GetStudentEmailListForTagMail(tags, avoid, mentor, db)
    
    student_ids = cleanCommaValues(student_data['ids'])
   
    students = db.query(User).filter(User.id.in_(student_ids)).all()
    return templates.TemplateResponse("bookings/compose_students.html", {"request":request, "students":students})

@router.post("/testing_mail_to_mentor") #This is used in functionlity
def sent_testing_mail(test_compose: TestingMailSchema, background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    print(test_compose)
    background_tasks.add_task(SendTestingMailToMentor, test_compose, db)
    return {"flag":1, "message":"Mail set to your registered email address"}

    

@router.get('/testing', response_class=HTMLResponse)
async def testing(request: Request):
    import os
    print("Current working directory:", os.getcwd())
    return templates.TemplateResponse("bookings/testing.html", {"request":request})

@router.get('/query_test')
async def mail_test(db:Session = Depends(get_db)):
    clean = cleanCommaIntValues("42,67,89")
    stud_in = [95]
    stud_not_in = [96]

    in_stud_detail = db.query(BookingTagStudent).filter(
        and_(
            BookingTagStudent.addedBy == 72208,
            BookingTagStudent.tag_id.in_(stud_in),
        )
    ).all()
    not_in_stud = db.query(BookingTagStudent).filter(
        and_(
            BookingTagStudent.addedBy == 72208,
            BookingTagStudent.tag_id.in_(stud_not_in),
        )
    ).all()

    student_ids = [booking.student_id for booking in in_stud_detail]
    not_student_ids = [booking.student_id for booking in not_in_stud]

    not_student_ids_set = set(not_student_ids) # Convert not_student_ids to a set for faster lookups
    # Filter student_ids
    filtered_student_ids = [student_id for student_id in student_ids if student_id not in not_student_ids_set]

    # Getting unique student IDs from the filtered list
    filtered_student_ids = list(set(filtered_student_ids))

    students = db.query(User).filter(User.id.in_(filtered_student_ids)).all()
    student_emails = [{"email":student.email} for student in students]

    return {"in_tud": in_stud_detail, 'not_in':not_in_stud, "student_ids":student_ids, "not_student_ids":not_student_ids, "filtered_student_ids":filtered_student_ids, "student_emails":student_emails, "clean":clean}

    '''return db.query(BookingTagStudent).filter(
        and_(
            BookingTagStudent.addedBy == 593,
            BookingTagStudent.tag_id.in_(stud_in),
            BookingTagStudent.tag_id.notin_(stud_not_in)
        )
    ).options(joinedload(BookingTagStudent.student)).limit(10).all()'''

@router.get("/raw_query", response_model=List[TagListSchema])
async def tag_list(db:Session=Depends(get_db)):
    #Define your raw SQL query
    query = "SELECT * FROM bookings_tags"  # Replace with your actual SQL

    # Execute the raw query
    result = db.fetch_all(query)

    

    return result