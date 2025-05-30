
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
from urllib.parse import urlencode

from sqlalchemy import bindparam


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
async def admin_read_tests(
    request: Request,
    db: AsyncSession = Depends(get_async_db),  # async session
    current_user: dict = Depends(get_current_user),
    page: int = 1,
    page_size: int = 50
):
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found")

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
    total_count = count_result.scalar() or 0

    page_count = (total_count + page_size - 1) // page_size  # ceil division

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

        response_list.append(item)


    base_url = str(request.url).split('?')[0]
    query_params = dict(request.query_params)


    def build_url(page_num: int):
        params = query_params.copy()
        params['page'] = page_num
        return f"{base_url}?{urlencode(params)}"

    next_url = build_url(page + 1) if page < page_count else None
    prev_url = build_url(page - 1) if page > 1 else None
    first_page_url = build_url(1) if page_count > 0 else None
    last_page_url = build_url(page_count) if page_count > 0 else None

    response_data = {
        "count": total_count,
        "next": next_url,
        "previous": prev_url,
        "first_page": first_page_url,
        "last_page": last_page_url,
        "page_count": page_count,
        "result": response_list,
    }

    return JSONResponse(
        content={"flag": 1, "message": "Success", "data": response_data},
        status_code=200,
    )













