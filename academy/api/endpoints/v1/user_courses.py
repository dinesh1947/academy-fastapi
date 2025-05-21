
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Sequence, Tuple
import asyncio
from sqlalchemy.future import select
from config.database import get_sync_db, get_async_db
from utils.project_jwt import *
from utils.pagination import *
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











def update_consolidated_rank_from_rows( db,rows: Sequence[Tuple[int, float]]) -> int:
    if not rows:
        return 0
    updates = []
    curr_rank, count, prev_score = 1, 0, None
    for uid, score in rows:
        count += 1
        if score != prev_score:
            curr_rank = count
        updates.append((uid, curr_rank))
        prev_score = score
    when_clauses = "\n    ".join(f"WHEN {uid} THEN {rk}" for uid, rk in updates)
    id_list      = ", ".join(str(uid) for uid, _ in updates)
    sql = f"""
        UPDATE user_courses_usertest
        SET consolidated_rank = CASE id
            {when_clauses}
            ELSE consolidated_rank
        END
        WHERE id IN ({id_list})
    """
    db.execute(text(sql))
    db.commit()
    return len(updates)








from typing import Sequence, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session

def update_rank_from_rows( db: Session, rows: Sequence[Tuple[int, float]] ) -> int:

    if not rows:
        return 0

    # 1) compute (id, rank) pairs
    updates = []
    current_rank = 1
    count = 0
    previous_score = None

    for user_test_id, score in rows:
        count += 1
        if score != previous_score:
            current_rank = count
        updates.append((user_test_id, current_rank))
        previous_score = score

    # 2) build the CASE … WHEN fragment and the IN list
    when_clauses = "\n        ".join(
        f"WHEN {uid} THEN {rk}" for uid, rk in updates
    )
    id_list = ", ".join(str(uid) for uid, _ in updates)

    # 3) run a single UPDATE … CASE, with backticks around `rank`
    sql = f"""
        UPDATE user_courses_usertest
        SET `rank` = CASE id
            {when_clauses}
            ELSE `rank`
        END
        WHERE id IN ({id_list})
    """
    db.execute(text(sql))
    db.commit()

    return len(updates)















def update_user_test(db: Session, ut_ids: list[int],test_id):
 
    test = db.execute(
            text("""
                SELECT 
                    id,
                    name,
                    duration,
                    question_paper_id,
                    mark_per_right,
                    mark_per_wrong
                FROM pts_test
                WHERE id = :test_id
                LIMIT 1
            """),
            {"test_id": test_id}
        ).fetchone()
    

    mark_per_right = test._mapping["mark_per_right"]
    mark_per_wrong = test._mapping["mark_per_wrong"]

    if not ut_ids:
        return

    rows = db.execute(
        text(f"""
            SELECT
                user_test_id,
                COUNT(CASE WHEN is_correct = 1 THEN 1 END) AS correct_answer,
                COUNT(CASE WHEN is_correct = 0 THEN 1 END) AS incorrect_answer,
                COUNT(CASE WHEN is_correct = -1 THEN 1 END) AS not_answer
            FROM user_courses_usertestanswer
            WHERE user_test_id IN ({ut_ids})
            GROUP BY user_test_id
        """),
        
    ).fetchall()

    if not rows:
        return




    correct_answer_case = "CASE user_courses_usertest.id\n"
    incorrect_answer_case = "CASE user_courses_usertest.id\n"
    not_answer_case = "CASE user_courses_usertest.id\n"
    score_case = "CASE user_courses_usertest.id\n"
    user_test_ids = []

    for row in rows:
        user_test_id = row._mapping["user_test_id"]
        user_test_ids.append(user_test_id)
        correct_answer_case += f"    WHEN {user_test_id} THEN {row._mapping['correct_answer']}\n"
        incorrect_answer_case += f"    WHEN {user_test_id} THEN {row._mapping['incorrect_answer']}\n"
        not_answer_case += f"    WHEN {user_test_id} THEN {row._mapping['not_answer']}\n"
     
        score_case += (f"    WHEN {user_test_id} THEN ROUND({row._mapping['correct_answer']} * {mark_per_right} - "f"{row._mapping['incorrect_answer']} * {mark_per_right} / {mark_per_wrong}, 2)\n")




    correct_answer_case += "    ELSE correct_answer END"
    incorrect_answer_case += "    ELSE incorrect_answer END"
    not_answer_case += "    ELSE not_answer END"
    score_case += "    ELSE NULL END"

    id_str = ", ".join(str(i) for i in user_test_ids)

    update_query = f"""
        UPDATE user_courses_usertest
        SET
            correct_answer = {correct_answer_case},
            incorrect_answer = {incorrect_answer_case},
            not_answer = {not_answer_case},
            score = {score_case}
        WHERE id IN ({id_str})
    """

    db.execute(text(update_query))
    db.commit()






    rows = db.execute(text("""
        SELECT id, score
        FROM user_courses_usertest
        WHERE test_id = :tid AND test_status = 'completed'
        ORDER BY score DESC
    """), {"tid": test_id}).fetchall()


    updated_count = update_consolidated_rank_from_rows(db, rows)
    print("update_consolidated_rank_from_rows",updated_count)


    rows = db.execute(text("""
        SELECT id, score
        FROM user_courses_usertest
        WHERE test_id = :tid AND test_status = 'completed' AND answer_mode !='offline'
        ORDER BY score DESC
    """), {"tid": test_id}).fetchall()

    updated_count = update_rank_from_rows(db, rows)
    print("update_rank_from_rows",updated_count)







    return len(user_test_ids)








def update_pts_question_stats(db: Session, question_paper_id: int):
    rows = db.execute(
        text("""
            SELECT
                question_id,
                COUNT(CASE WHEN is_correct =  1 THEN 1 END) AS correct_answer,
                COUNT(CASE WHEN is_correct =  0 THEN 1 END) AS incorrect_answer,
                COUNT(CASE WHEN is_correct = -1 THEN 1 END) AS not_answer
            FROM user_courses_usertestanswer
            WHERE question_paper_id = :question_paper_id
            GROUP BY question_id
            ORDER BY question_id
        """),
        {"question_paper_id": question_paper_id}
    ).fetchall()

    correct_answer_case = "CASE id\n"
    incorrect_answer_case = "CASE id\n"
    not_answer_case = "CASE id\n"
    question_ids = []

    for row in rows:
        question_id = row._mapping["question_id"]
        question_ids.append(str(question_id))
        correct_answer_case += f"    WHEN {question_id} THEN {row._mapping['correct_answer']}\n"
        incorrect_answer_case += f"    WHEN {question_id} THEN {row._mapping['incorrect_answer']}\n"
        not_answer_case += f"    WHEN {question_id} THEN {row._mapping['not_answer']}\n"

    correct_answer_case += "    ELSE correct_answer END"
    incorrect_answer_case += "    ELSE incorrect_answer END"
    not_answer_case += "    ELSE not_answer END"

    question_ids_str = ", ".join(question_ids)

    update_query = f"""
        UPDATE pts_question
        SET
            correct_answer = {correct_answer_case},
            incorrect_answer = {incorrect_answer_case},
            not_answer = {not_answer_case}
        WHERE id IN ({question_ids_str})
    """

    db.execute(text(update_query))
    db.commit()





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


