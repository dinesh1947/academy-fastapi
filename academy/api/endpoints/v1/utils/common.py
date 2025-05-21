# from sqlalchemy import and_, desc
# from datetime import datetime
# # from api.endpoints.v1.models.BookingModel import BookingTagMail, BookingTagStudent, BookingTags
# from api.models.v1.UserModel import *
# from api.models.v1.BookingModel import *
# from api.models.v1.UserModel import *
# # from .v1.models.UserModel import *
# # from app.api.v1.utils.helper import cleanCommaIntValues



from fastapi import Request
from math import ceil
from typing import List, Type, TypeVar, Dict, Any
from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Sequence, Tuple
from sqlalchemy import text


T = TypeVar("T", bound=BaseModel)

# def paginate(
#     request: Request,
#     items: List[T],
#     total_count: int,
#     page: int,
#     page_size: int,
#     response_model: Type[BaseModel]
# ):
#     total_pages = ceil(total_count / page_size)
#     base_url = str(request.url).split('?')[0]

#     def page_link(p):
#         return f"{base_url}?page={p}&page_size={page_size}"

#     return response_model(
#         total_count=total_count,
#         page=page,
#         page_size=page_size,
#         total_pages=total_pages,
#         first=page_link(1) if page > 1 else None,
#         last=page_link(total_pages) if page < total_pages else None,
#         next=page_link(page + 1) if page < total_pages else None,
#         previous=page_link(page - 1) if page > 1 else None,
#         results=items
#     )




def paginate(
    request: Request,
    items: List[Any],
    total_count: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    total_pages = ceil(total_count / page_size)
    base_url = str(request.url).split('?')[0]

    def page_link(p: int) -> str:
        return f"{base_url}?page={p}&page_size={page_size}"

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "first": page_link(1) if page > 1 else None,
        "last": page_link(total_pages) if page < total_pages else None,
        "next": page_link(page + 1) if page < total_pages else None,
        "previous": page_link(page - 1) if page > 1 else None,
        "results": items
    }










# def get_columns_from_pydantic_model(pydantic_model: Type[BaseModel], sqlalchemy_model):
#     pydantic_fields = set(pydantic_model.__annotations__.keys())
#     columns = [getattr(sqlalchemy_model, field) for field in pydantic_fields if hasattr(sqlalchemy_model, field)]
#     return columns




def get_columns_from_pydantic_model(schema: Type[BaseModel], model: DeclarativeMeta) -> List:
    """Select only the columns from SQLAlchemy model that match the Pydantic schema fields."""
    return [getattr(model, field) for field in schema.__fields__.keys()]



# def GetStudentEmailListForTagMail(to_tags, avoid_tags, from_id, db):
#     #clean = cleanCommaIntValues("42,67,89")
#     stud_in = cleanCommaIntValues(to_tags)
    
#     in_stud_detail = db.query(BookingTagStudent).filter(
#         and_(
#             BookingTagStudent.addedBy == from_id,
#             BookingTagStudent.tag_id.in_(stud_in),
#         )
#     ).all()
   
#     student_ids = [booking.student_id for booking in in_stud_detail]
    

#     if avoid_tags:
#         stud_not_in = cleanCommaIntValues(avoid_tags)
#         not_in_stud = db.query(BookingTagStudent).filter(
#             and_(
#                 BookingTagStudent.addedBy == from_id,
#                 BookingTagStudent.tag_id.in_(stud_not_in),
#             )
#         ).all()

    
#         not_student_ids = [booking.student_id for booking in not_in_stud]

#         not_student_ids_set = set(not_student_ids) # Convert not_student_ids to a set for faster lookups
#         # Filter student_ids
#         filtered_student_ids = [student_id for student_id in student_ids if student_id not in not_student_ids_set]

#         # Getting unique student IDs from the filtered list
#         filtered_student_ids = list(set(filtered_student_ids))
#     else:
#         filtered_student_ids = list(set(student_ids))

#     students = db.query(User).filter(User.id.in_(filtered_student_ids)).all()
#     student_emails = [{"email":student.email, "name":student.fullName, "roll_number":student.roll_number} for student in students]
#     ids_str = ','.join(map(str, filtered_student_ids))
#     result = {"emails":student_emails, "ids":ids_str}
#     return result

# def GetListTags(id, db):
#     list_detail = db.query(BookingTagMail).filter(BookingTagMail.id == id).first()

#     to_tag_idz = cleanCommaIntValues(list_detail.to_tags)
#     avoid_tag_idz = cleanCommaIntValues(list_detail.avoid_tags)

#     to_tag_obj = db.query(BookingTags).filter(BookingTags.id.in_(to_tag_idz)).all()
#     avoid_tag_obj = db.query(BookingTags).filter(BookingTags.id.in_(avoid_tag_idz)).all()

#     to_tag_arr = [one.tag_name for one in to_tag_obj]
#     avoid_tag_arr = [one.tag_name for one in avoid_tag_obj]

#     to_tag_str = ','.join(to_tag_arr)
#     avoid_tag_str = ','.join(avoid_tag_arr)

#     result = {"to_tag": to_tag_str, "avoid_tag": avoid_tag_str}

#     return result

# def GetRegisteredUsersByDate(dt, db): #Not in use
#     print("+++++++++++++++++++++++++++++++++YYYYYYYYYYYYYYYYYYYYYYY+++++++++++++++++++++++++++++++")
#     print(dt)
#     dt = dt.strip()
#     gt_dt = dt + " 00:00:00"
#     gt_dt = datetime.strptime(gt_dt, "%Y-%m-%d %H:%M:%S")
#     lt_dt = dt + " 23:59:00"
#     lt_dt = datetime.strptime(lt_dt, "%Y-%m-%d %H:%M:%S")
#     print(gt_dt)
#     print(lt_dt)
#     users = db.query(User).filter(User.joinDate >= gt_dt).filter(User.joinDate <= lt_dt).order_by(desc(User.id)).all()
#     return users

# def GetRegisteredUsersByIds(ids, db):
#     print("+++++++++++++++++++++++++++++++++YYYYYYYYYYYYYYYYYYYYYYY+++++++++++++++++++++++++++++++")
#     print(ids)
#     ids = cleanCommaIntValues(ids)
#     users = db.query(User).filter(User.id.in_(ids)).order_by(desc(User.id)).all()
#     return users














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





    rows = db.execute(text("""
        SELECT id, score
        FROM user_courses_usertest
        WHERE test_id = :tid AND test_status = 'completed' AND answer_mode ='offline'
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























