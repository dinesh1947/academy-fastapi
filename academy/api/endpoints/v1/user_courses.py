
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Sequence, Tuple
import asyncio
from config.database import get_sync_db, get_async_db
from utils.project_jwt import *
from utils.pagination import *
from utils.common import *
from api.models.v1.PtsModel import *
from api.models.v1.UserCourseModel import *
from api.schemas.v1.UserCourseSchema import *
from sqlalchemy.orm import joinedload
import json
from fastapi.responses import JSONResponse
from sqlalchemy import text
from fastapi import BackgroundTasks
from urllib.parse import urlencode

from sqlalchemy import bindparam


from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Body


router = APIRouter()


from sqlalchemy import select, distinct






@router.get("/list/")
def admin_read_tests(request: Request,db: Session = Depends(get_sync_db),current_user: dict = Depends(get_current_user),page: int = 1,page_size: int = 10):
    user_id = current_user.get("id")
    offset = (page - 1) * page_size

    count_query = text("""
        SELECT COUNT(*) FROM user_courses_usercoursepackage AS ucp
        JOIN users AS u ON u.id = ucp.user_id
        WHERE ucp.user_id = :user_id
        AND ucp.course_id IS NOT NULL
        AND ucp.status = 'active'
        AND u.status = 'active'
    """)
    count = db.execute(count_query, {"user_id": user_id}).scalar()

    page_count = (count + page_size - 1)//page_size 


    query = text("""
        SELECT 
            ucp.id AS id,
            ucp.package_id,
            ucp.course_id,
            cp.name AS package_name,
            cc.title AS course_name,
            ucp.show_status
        FROM user_courses_usercoursepackage AS ucp
        LEFT JOIN courses_package AS cp ON cp.id = ucp.package_id
        LEFT JOIN courses_course AS cc ON cc.id = ucp.course_id
        JOIN users AS u ON u.id = ucp.user_id
        WHERE ucp.user_id = :user_id
        AND ucp.course_id IS NOT NULL
        AND ucp.status = 'active'
        AND u.status = 'active'
        ORDER BY ucp.id DESC
        LIMIT :limit OFFSET :offset
    """)

    result = db.execute(query, { "user_id": user_id, "limit": page_size, "offset": offset})

    rows = result.mappings().all()
    results = [dict(row) for row in rows]
    

    pagination_urls = build_pagination_urls(request, page, page_count)


    data= { "count": count, "current_page": page,"page_size": page_size, "page_count": page_count, **pagination_urls }

    data['results']=results

    content={ "flag": 1, "message": "Success", "data": data, }



    return JSONResponse(status_code=200, content=content)













@router.get("/pts-list/")
async def admin_read_tests(
    request: Request,
    db: AsyncSession = Depends(get_async_db), 
    current_user: dict = Depends(get_current_user),
    page: int = 1,
    page_size: int = 50
):
    user_id = current_user.get("id")
   

    offset = (page - 1) * page_size
    count_query = text("""
        SELECT COUNT(*) AS total_count
        FROM user_courses_usercoursepackage AS ucp
        JOIN users AS u ON u.id = ucp.user_id
        WHERE ucp.user_id = :user_id
          AND ucp.test_series_id IS NOT NULL
          AND ucp.status = 'active'
          AND u.status = 'active'
    """)

    count_result = await db.execute(count_query, {"user_id": user_id})
    count = count_result.scalar() or 0
    page_count = (count + page_size - 1) // page_size  



    main_query = text("""
        SELECT 
            ucp.id AS id,
            ucp.package_id,
            ucp.test_series_id,
            cp.name AS package_name,
            ucp.show_status                     
        FROM user_courses_usercoursepackage AS ucp
        LEFT JOIN courses_package AS cp ON cp.id = ucp.package_id
        JOIN users AS u ON u.id = ucp.user_id
        WHERE ucp.user_id = :user_id
          AND ucp.test_series_id IS NOT NULL
          AND ucp.status = 'active'
          AND u.status = 'active'
        ORDER BY ucp.id DESC
        LIMIT :limit OFFSET :offset
    """)

    main_result = await db.execute(main_query, {
        "user_id": user_id,
        "limit": page_size,
        "offset": offset
    })

    rows = main_result.mappings().all()
    response_list = []

    for row in rows:
        item = dict(row)
        package_id = item['package_id']

        test_ids_query = text("""
            SELECT test_id
            FROM pts_testpackage
            WHERE package_id = :package_id
              AND start_date_time IS NOT NULL
              AND end_date_time IS NOT NULL
        """)

        test_ids_result = await db.execute(test_ids_query, {"package_id": package_id})
        test_ids = [r['test_id'] for r in test_ids_result.mappings().all()]

        item['total_test_count'] = len(test_ids)

        if test_ids:
            completed_count_query = text("""
                SELECT COUNT(*) AS completed_count
                FROM user_courses_usertest
                WHERE user_id = :user_id
                  AND test_id IN :test_ids
                  AND test_status = 'completed'
            """).bindparams(bindparam("test_ids", expanding=True))

            completed_result = await db.execute(completed_count_query, {
                "user_id": user_id,
                "test_ids": test_ids
            })

            attempt_count = completed_result.scalar() or 0
        else:
            attempt_count = 0

        item['attempt_count'] = attempt_count
        if attempt_count == 0:
            item['show_status']="start"
        elif attempt_count==item['total_test_count']:
            item['show_status']="completed"
        else:
            item['show_status']="continue"
        
        response_list.append(item)



    pagination_urls = build_pagination_urls(request, page, page_count)
    data= { "current_page": page,"page_size": page_size, "count": count, "page_count": page_count, **pagination_urls }
    data['results'] = response_list
    content={ "flag": 1, "message": "Success", "data": data }
    return JSONResponse(status_code=200, content=content)

















@router.get("/start-upcoming-resume/")
async def admin_read_tests(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Depends(get_current_user),
    ucp_id: int = None,
    page: int = 1,
    page_size: int = 10
):
    try:
        if not ucp_id:
            raise HTTPException(status_code=400, detail="Invalid or missing ucp_id.")
        
        user_id = current_user.get("id")
        current_time = datetime.utcnow().replace(tzinfo=ZoneInfo("UTC"))
        indian_tz = ZoneInfo("Asia/Kolkata")

        result = await db.execute(text("""
            SELECT ucp.*, p.name as package_name
            FROM user_courses_usercoursepackage ucp
            JOIN courses_package p ON ucp.package_id = p.id
            WHERE ucp.id = :ucp_id AND ucp.user_id = :user_id AND ucp.status = 'active'
        """), {"ucp_id": ucp_id, "user_id": user_id})
        
        ucp_data = result.fetchone()
        if not ucp_data:
            return JSONResponse(status_code=200, content={"flag": 0, "message": "No record Found", "data": {}})
            
        
        package_name = ucp_data.package_name


        result = await db.execute(text("""
            SELECT
                UCP.user_id,
                TP.test_id AS id,
                TP.start_date_time,
                TP.end_date_time,
                T.name,
                T.total_question,
                T.duration,
                T.schedule_date_time,
                UT.id AS user_test__id,
                UT.is_agree,
                UT.language,
                UT.test_status,
                UT.test_type,
                UT.answer_mode
            FROM user_courses_usercoursepackage AS UCP
            INNER JOIN pts_testpackage AS TP ON TP.package_id = UCP.package_id  
            INNER JOIN pts_test AS T ON T.id = TP.test_id
            LEFT JOIN user_courses_usertest AS UT 
                ON UT.test_id = T.id 
                AND UT.user_id = UCP.user_id 
                AND UT.test_type = 'pts'
            WHERE
                UCP.id = :ucp_id
                AND T.is_quiz = FALSE
                AND TP.start_date_time IS NOT NULL
                AND TP.end_date_time IS NOT NULL
                AND (UT.id IS NOT NULL OR TP.end_date_time > NOW())
               
                AND (UT.test_status != 'completed' OR UT.test_status IS NULL)
            ORDER BY TP.start_date_time DESC
        """), {"ucp_id": ucp_id})

        rows = result.fetchall()
        columns = result.keys()
        all_results = [dict(zip(columns, row)) for row in rows]
        total = len(all_results)
        page_count = (total + page_size - 1) // page_size

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = all_results[start_idx:end_idx]

        upcoming, resume, start = [], [], []
        pagination_urls = build_pagination_urls(request, page, page_count)


        for i in paginated_results:
          
            i['start_date_time'] = i['start_date_time'].astimezone(indian_tz)
            i['end_date_time'] = i['end_date_time'].astimezone(indian_tz)
            i["before_show"] = 0

            if i['schedule_date_time']:
                i['schedule_date_time'] = i['schedule_date_time'].astimezone(indian_tz)
                i["result_type"] = "scheduled" if i['schedule_date_time'] > current_time else "instant"
            else:
                i["result_type"] = "instant"

            if i['start_date_time'] <= current_time:
                if not i['user_test__id']:
                    i['test_status'] = 'start'
                    start.append(i)
                else:
                    if i.get('is_agree') and i.get('language') in ["hindi", "english"]:
                        i['test_status'] = 'resume'
                        resume.append(i)
                    else:
                        i['test_status'] = 'start'
                        start.append(i)
            else:
                i['test_status'] = 'upcoming'
                future_time = current_time + timedelta(minutes=6)
                if future_time > i['start_date_time']:
                    i["before_show"] = 1
                upcoming.append(i)

        combined_results = upcoming + resume + start
        for item in combined_results:
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = value.isoformat()

        return JSONResponse(
            status_code=200,
            content={
                "flag": 1,
                "message": "Record fetched successfully.",
                "data": {
                    "current_page": page,
                    "page_size": page_size,
                    "count": total,
                    "page_count": page_count,
                    **pagination_urls,
                    "results": combined_results
                },
                "package_name": package_name
            }
        )


    except Exception as e:
        return JSONResponse( status_code=500, content={"flag": 0, "message": f"Something went wrong - {str(e)}",  "data": {} })

























@router.get("/user-test-list", response_model=PaginatedResponse[UserTestSchema])
def get_test_users(
    request: Request,
    db: Session = Depends(get_sync_db),
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(UserTest).order_by(UserTest.id)  

    return paginate_query(
        request=request,
        query=query,
        schema=UserTestSchema,  
        page=page,
        page_size=page_size
    )





@router.get("/user-test-answer-list", response_model=PaginatedResponse[UserTestAnswerSchema])
def get_test_user_answer(
    request: Request,
    db: Session = Depends(get_sync_db),
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(UserTestAnswer).options(joinedload(UserTestAnswer.question)).order_by(UserTestAnswer.id)

    return paginate_query(
        request=request,
        query=query,
        schema=UserTestAnswerSchema,  
        page=page,
        page_size=page_size
    )












@router.post("/update-rank-n-uta-is-correct-by-test")
async def update_uta_is_correct_by_test(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_sync_db), ):
    raw_body = await request.body()
    body = json.loads(raw_body.decode("utf-8"))
    test_id = body.get("test_id")
    if not test_id:
        raise HTTPException(status_code=400, detail="Missing 'test_id' in request body.")

    user_test_id_result = db.execute(text("""
        SELECT id FROM user_courses_usertest
        WHERE test_id = :test_id AND test_status = 'completed'
    """), {"test_id": test_id})
    user_test_ids = [row[0] for row in user_test_id_result.fetchall()]

    if not user_test_ids:
        return JSONResponse(
            content={"flag": 0, "message": "No completed user tests found", "data": 0},
            status_code=404,
        )

    ut_ids = ",".join(str(uid) for uid in user_test_ids)

    try:
        update_query = f"""
        UPDATE user_courses_usertestanswer uta
        JOIN pts_question q ON uta.question_id = q.id
        SET uta.is_correct = 
        CASE
            WHEN TRIM(LOWER(uta.answer)) = '' THEN 0
            WHEN TRIM(LOWER(uta.answer)) = TRIM(LOWER(q.correct_option)) THEN 1
            ELSE -1
        END
        WHERE uta.user_test_id IN ({ut_ids})
        """
        result = db.execute(text(update_query))
        db.commit()
    except Exception:
        db.rollback()
        return JSONResponse(
            content={"flag": 0, "message": "Failed to update user test answers", "data": 0},
            status_code=500,
        )

    updated_count = result.rowcount

    test_row = db.execute(
        text("""SELECT question_paper_id FROM pts_test WHERE id = :test_id"""),
        {"test_id": test_id},
    ).fetchone()

    if test_row is None:
        return JSONResponse(
            content={"flag": 0, "message": "Test not found", "data": 0},
            status_code=404,
        )

    question_paper_id = test_row._mapping["question_paper_id"]

    background_tasks.add_task(update_user_test, db, ut_ids,test_id)
    background_tasks.add_task(update_pts_question_stats, db, question_paper_id)

    return JSONResponse(
        content={"flag": 1, "message": "Updated successfully", "data": updated_count},
        status_code=200,
    )










@router.post("/start")
async def start_test(
    request: Request,   
    payload: StartTestSchema = Body(...), 
    db: AsyncSession = Depends(get_async_db), 
    current_user: dict = Depends(get_current_user),
):
    print("####################################################################################################")
    print(current_user)

    user_id = current_user.get("id")

    ucp_id = payload.ucp_id
    test_id = payload.test_id
    answer_mode = payload.answer_mode
    test_type = payload.test_type

    test_result = await db.execute(select(Test).where(Test.id == test_id))
    test = test_result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    ucp_result = await db.execute(
        select(UserCoursePackage).where(
            UserCoursePackage.id == ucp_id,
            UserCoursePackage.user_id == user_id
        )
    )
    ucp = ucp_result.scalar_one_or_none()
    if not ucp:
        raise HTTPException(status_code=404, detail="UserCoursePackage not found")

    tp_result = await db.execute(
        select(TestPackage).where(
            TestPackage.test_id == test_id,
            TestPackage.package_id == ucp.package_id
        )
    )
    tp = tp_result.scalar_one_or_none()
    if not tp:
        raise HTTPException(status_code=404, detail="TestPackage not found")

    usertest_result = await db.execute(
        select(UserTest).where(
            UserTest.user_id == user_id,
            UserTest.test_id == test_id,
            UserTest.test_type == test_type
        )
    )
    user_test = usertest_result.scalar_one_or_none()

    if user_test:
        created = False
    else:
        user_test = UserTest(
            user_id=user_id,
            test_id=test_id,
            user_course_package_id=ucp_id,
            question_paper_id=test.question_paper_id,
            answer_mode=answer_mode,
            test_type=test_type,
            test_status="start",
            language="english",  
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(user_test)
        await db.commit()
        await db.refresh(user_test)
        created = True


    data = {"created":created}

    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")


    



    stmt = (
        select(distinct(Question.language))
        .where(Question.question_paper_id == test.question_paper_id)
        .order_by(Question.language)
    )

    result = await db.execute(stmt)
    languages = result.scalars().all()
    language_values = [lang.value for lang in languages if lang is not None]

    print(language_values)


    return JSONResponse(
        content={"flag": 1, "message": "Updated successfully", "data": data},
        status_code=200,
    )



















