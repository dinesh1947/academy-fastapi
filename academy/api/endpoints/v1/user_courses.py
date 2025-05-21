
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Sequence, Tuple
import asyncio
from sqlalchemy.future import select
from config.database import get_sync_db, get_async_db
from utils.project_jwt import *
from utils.pagination import *
from utils.common import *
from api.models.v1.UserCourseModel import *
from api.schemas.v1.UserCourseSchema import *
from sqlalchemy.orm import joinedload
import json
from fastapi.responses import JSONResponse
from sqlalchemy import text
from fastapi import BackgroundTasks



router = APIRouter()



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








# @router.post("/update-uta-is-correct-by-test", response_model=PaginatedResponse[UserTestAnswerSchema])
# async def get_test_user_answer(
#     request: Request,
#     db: Session = Depends(get_sync_db),
#     page: int = 1,
#     page_size: int = 10,
# ):
#     raw_body = await request.body()  # await here works in async def
#     body_str = raw_body.decode('utf-8')
#     body = json.loads(body_str)

#     test_id = body.get("test_id")
#     print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKUUUUUUUUUUUUUUUUUUUUUUUUUUUUUoooooooooooooooooooooooU")
#     print(test_id)
#     print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")




#     user_test_ids = db.query(UserTest.id).filter(UserTest.test_id == test_id,UserTest.test_status == "completed" )
#     print(user_test_ids)
#     print("KKKKKKKKKKKKKKKKKKKKKKKeeeeeeeeeeeeddddddddddddddddddddddd")


#     query = (
#         db.query(UserTestAnswer)
#         .filter(UserTestAnswer.user_test_id.in_(user_test_ids))
#         .options(joinedload(UserTestAnswer.question))
#         .order_by(UserTestAnswer.id)
#     )

#     print(query)
#     print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUEEEEEEEEEEEEEEEEEEEEEEEEEE")





#     return paginate_query(
#         request=request,
#         query=query,
#         schema=UserTestAnswerSchema,  
#         page=page,
#         page_size=page_size
#     )









# @router.post("/update-uta-is-correct-by-test")
# async def update_uta_is_correct_by_test(
#     request: Request,
#     db: Session = Depends(get_sync_db),
# ):
#     raw_body = await request.body()
#     body = json.loads(raw_body.decode("utf-8"))

#     test_id = body.get("test_id")
#     if not test_id:
#         raise HTTPException(status_code=400, detail="Missing 'test_id' in request body.")

#     user_test_ids = [
#         t[0] for t in db.query(UserTest.id).filter(
#             UserTest.test_id == test_id,
#             UserTest.test_status == "completed"
#         ).all()
#     ]

#     if not user_test_ids:

#         return JSONResponse(
#             status_code=404,
#             content={"flag": 0, "message": "No completed user tests found", "data": 0}
#         )
        



#     answers = db.query(UserTestAnswer).options(joinedload(UserTestAnswer.question)).filter(
#         UserTestAnswer.user_test_id.in_(user_test_ids)
#     ).all()

#     for uta in answers:
#         answer = (uta.answer or "").strip().lower()
#         correct_option = (uta.question.correct_option or "").strip().lower()

#         if not answer:
#             uta.is_correct = 0
#         elif answer == correct_option:
#             uta.is_correct = 1
#         else:
#             uta.is_correct = -1

#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         return JSONResponse(
#             status_code=500,
#             content={"flag": 0, "message": "Failed to update user test answers", "data": 0}
#         )

#     result_data = len(answers)

#     return JSONResponse(
#         status_code=200,
#         content={
#             "flag": 1,
#             "message": f"{result_data} user test answers updated successfully",
#             "data": result_data
#         }
#     )       








# @router.post("/update-uta-is-correct-by-test")
# async def update_uta_is_correct_by_test(request: Request,db: Session = Depends(get_sync_db),):
#     raw_body = await request.body()
#     body = json.loads(raw_body.decode("utf-8"))
#     test_id = body.get("test_id")
#     if not test_id:
#         raise HTTPException(status_code=400, detail="Missing 'test_id' in request body.")
#     user_test_id_result = db.execute(text("""
#         SELECT id FROM user_courses_usertest
#         WHERE test_id = :test_id AND test_status = 'completed'
#     """), {"test_id": test_id})
#     user_test_ids = [row[0] for row in user_test_id_result.fetchall()]
#     if not user_test_ids:
#         return JSONResponse(content={"flag": 0, "message": "No completed user tests found", "data": 0}, status_code=404)
#     ut_ids = ",".join(str(uid) for uid in user_test_ids)
#     try:
#         print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
#         update_query = f"""
#         UPDATE user_courses_usertestanswer uta
#         JOIN pts_question q ON uta.question_id = q.id
#         SET uta.is_correct = 
#         CASE
#             WHEN TRIM(LOWER(uta.answer)) = '' THEN 0
#             WHEN TRIM(LOWER(uta.answer)) = TRIM(LOWER(q.correct_option)) THEN 1
#             ELSE -1
#         END
#         WHERE uta.user_test_id IN ({ut_ids})
#         """
#         print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSss")
#         result = db.execute(text(update_query))
#         db.commit()
#         print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
#     except Exception:
#         db.rollback()
#         return JSONResponse(content={"flag": 0, "message": "Failed to update user test answers", "data": 0},status_code=500)
#     updated_count = result.rowcount  
#     user_test_id_result = db.execute(text("""SELECT * FROM pts_test WHERE id = :test_id """), {"test_id": test_id})
#     print(user_test_id_result)
#     first_row = user_test_id_result.fetchone()
#     # print(first_row)
#     # print(dict(first_row._mapping))
#     x = dict(first_row._mapping)
#     print(x['question_paper_id'])  
#     question_paper_id =  x['question_paper_id']
#     rows = db.execute(
#         text("""
#             SELECT
#                 question_id,
#                 COUNT(CASE WHEN is_correct =  1 THEN 1 END) AS correct_answer,
#                 COUNT(CASE WHEN is_correct =  0 THEN 1 END) AS incorrect_answer,
#                 COUNT(CASE WHEN is_correct = -1 THEN 1 END) AS not_answer
#             FROM user_courses_usertestanswer
#             WHERE question_paper_id = :question_paper_id
#             GROUP BY question_id
#             ORDER BY question_id
#         """),
#         {"question_paper_id": question_paper_id}
#     ).fetchall()

#     correct_answer_case = "CASE id\n"
#     incorrect_answer_case = "CASE id\n"
#     not_answer_case = "CASE id\n"
#     question_ids = []
#     for row in rows:
#         question_id = row._mapping["question_id"]
#         question_ids.append(str(question_id))
#         correct_answer_case += f"    WHEN {question_id} THEN {row._mapping['correct_answer']}\n"
#         incorrect_answer_case += f"    WHEN {question_id} THEN {row._mapping['incorrect_answer']}\n"
#         not_answer_case += f"    WHEN {question_id} THEN {row._mapping['not_answer']}\n"
#     correct_answer_case += "    ELSE correct_answer END"
#     incorrect_answer_case += "    ELSE incorrect_answer END"
#     not_answer_case += "    ELSE not_answer END"
#     question_ids_str = ", ".join(question_ids)
#     update_query = f"""
#         UPDATE pts_question
#         SET
#             correct_answer = {correct_answer_case},
#             incorrect_answer = {incorrect_answer_case},
#             not_answer = {not_answer_case}
#         WHERE id IN ({question_ids_str})
#     """
#     db.execute(text(update_query))
#     db.commit()
#     return JSONResponse(content={"flag": 1,"message": f"Updated successfully","data": updated_count},status_code=200 )









@router.post("/update-uta-is-correct-by-test")
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


