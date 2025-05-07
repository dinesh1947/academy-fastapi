from sqlalchemy import and_, desc
from datetime import datetime
from app.api.v1.models.BookingModel import BookingTagMail, BookingTagStudent, BookingTags
from app.api.v1.models.UserModel import User
from app.api.v1.utils.helper import cleanCommaIntValues


def GetStudentEmailListForTagMail(to_tags, avoid_tags, from_id, db):
    #clean = cleanCommaIntValues("42,67,89")
    stud_in = cleanCommaIntValues(to_tags)
    
    in_stud_detail = db.query(BookingTagStudent).filter(
        and_(
            BookingTagStudent.addedBy == from_id,
            BookingTagStudent.tag_id.in_(stud_in),
        )
    ).all()
   
    student_ids = [booking.student_id for booking in in_stud_detail]
    

    if avoid_tags:
        stud_not_in = cleanCommaIntValues(avoid_tags)
        not_in_stud = db.query(BookingTagStudent).filter(
            and_(
                BookingTagStudent.addedBy == from_id,
                BookingTagStudent.tag_id.in_(stud_not_in),
            )
        ).all()

    
        not_student_ids = [booking.student_id for booking in not_in_stud]

        not_student_ids_set = set(not_student_ids) # Convert not_student_ids to a set for faster lookups
        # Filter student_ids
        filtered_student_ids = [student_id for student_id in student_ids if student_id not in not_student_ids_set]

        # Getting unique student IDs from the filtered list
        filtered_student_ids = list(set(filtered_student_ids))
    else:
        filtered_student_ids = list(set(student_ids))

    students = db.query(User).filter(User.id.in_(filtered_student_ids)).all()
    student_emails = [{"email":student.email, "name":student.fullName, "roll_number":student.roll_number} for student in students]
    ids_str = ','.join(map(str, filtered_student_ids))
    result = {"emails":student_emails, "ids":ids_str}
    return result

def GetListTags(id, db):
    list_detail = db.query(BookingTagMail).filter(BookingTagMail.id == id).first()

    to_tag_idz = cleanCommaIntValues(list_detail.to_tags)
    avoid_tag_idz = cleanCommaIntValues(list_detail.avoid_tags)

    to_tag_obj = db.query(BookingTags).filter(BookingTags.id.in_(to_tag_idz)).all()
    avoid_tag_obj = db.query(BookingTags).filter(BookingTags.id.in_(avoid_tag_idz)).all()

    to_tag_arr = [one.tag_name for one in to_tag_obj]
    avoid_tag_arr = [one.tag_name for one in avoid_tag_obj]

    to_tag_str = ','.join(to_tag_arr)
    avoid_tag_str = ','.join(avoid_tag_arr)

    result = {"to_tag": to_tag_str, "avoid_tag": avoid_tag_str}

    return result

def GetRegisteredUsersByDate(dt, db): #Not in use
    print("+++++++++++++++++++++++++++++++++YYYYYYYYYYYYYYYYYYYYYYY+++++++++++++++++++++++++++++++")
    print(dt)
    dt = dt.strip()
    gt_dt = dt + " 00:00:00"
    gt_dt = datetime.strptime(gt_dt, "%Y-%m-%d %H:%M:%S")
    lt_dt = dt + " 23:59:00"
    lt_dt = datetime.strptime(lt_dt, "%Y-%m-%d %H:%M:%S")
    print(gt_dt)
    print(lt_dt)
    users = db.query(User).filter(User.joinDate >= gt_dt).filter(User.joinDate <= lt_dt).order_by(desc(User.id)).all()
    return users

def GetRegisteredUsersByIds(ids, db):
    print("+++++++++++++++++++++++++++++++++YYYYYYYYYYYYYYYYYYYYYYY+++++++++++++++++++++++++++++++")
    print(ids)
    ids = cleanCommaIntValues(ids)
    users = db.query(User).filter(User.id.in_(ids)).order_by(desc(User.id)).all()
    return users
