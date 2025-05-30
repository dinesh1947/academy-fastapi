
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










@router.get("/pts-list/")
def admin_read_tests(
    request: Request,
    db: Session = Depends(get_sync_db),
    current_user: dict = Depends(get_current_user),
    page: int = 1,
    page_size: int = 10
):
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found")

    offset = (page - 1) * page_size

    query = text("""
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

    result = db.execute(query, {
        "user_id": user_id,
        "limit": page_size,
        "offset": offset
    })

    rows = result.mappings().all()
    data = [dict(row) for row in rows]

    return JSONResponse(
        content={"flag": 1, "message": "Success", "data": data},
        status_code=200,
    )





