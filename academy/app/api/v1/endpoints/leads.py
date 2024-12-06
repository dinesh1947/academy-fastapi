# from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session, joinedload
# from sqlalchemy import desc, text, and_, func
# from app.config.database import get_db
# from typing import Optional, List
# from fastapi.templating import Jinja2Templates

# from app.api.v1.models.LeadModel import Counselling
# from app.api.v1.schemas.LeadSchema import AssignCounsellingSchema, CancelCounsellingSchema

# templates = Jinja2Templates(directory="app/api/v1/templates")

# router = APIRouter()

# @router.get("/counselling_list")
# async def pending_counselling(request: Request, log_user:int=0, log_role:int=0, status:int=1, page:int = 0, db:Session=Depends(get_db)):
#     limit = 10
#     offset = int(page) * limit
#     if log_role == 2:
#         result = db.execute(text("SELECT schedules.*, agent.fullName as agent_name FROM schedules LEFT JOIN user as agent ON agent.id = schedules.agent_id WHERE schedules.status = :status AND schedules.agent_id = :agent_id ORDER BY schedules.schedule_date DESC, schedules.schedule_time DESC LIMIT :limit OFFSET :offset"), {"status": status, "agent_id":log_user, "limit":limit, "offset":offset})
#     else:
#         result = db.execute(text("SELECT schedules.*, agent.fullName as agent_name FROM schedules LEFT JOIN user as agent ON agent.id = schedules.agent_id WHERE schedules.status = :status ORDER BY schedules.schedule_date DESC, schedules.schedule_time DESC LIMIT :limit OFFSET :offset"), {"status": status, "limit":limit, "offset":offset})
            
#     #keys = result.keys()
#     #response = [dict(zip(keys, row)) for row in result.fetchall()]
#     response = [dict(row) for row in result.mappings().all()]

#     #html_temp = templates.TemplateResponse("elements/leads/counselling.html", {"request":request, "counsellings":result})
#     if status == 2:
#         html_content = templates.get_template("elements/leads/assigned_counselling.html").render({"request": request, "counsellings":response})
#     elif status == 3:
#         html_content = templates.get_template("elements/leads/completed_counselling.html").render({"request": request, "counsellings":response})
#     elif status == 4:
#         html_content = templates.get_template("elements/leads/canceled_counselling.html").render({"request": request, "counsellings":response})
#     else:
#         html_content = templates.get_template("elements/leads/counselling.html").render({"request": request, "counsellings":response})

#     page = int(page) + 1
#     return {"code":1, "status":"success", "message":"Schedule list", "page":page, "result":html_content}

# @router.get("/counselling_detail")
# async def counselling_detail(request: Request, uq:int=0, db:Session=Depends(get_db)):
#     counselling = db.query(Counselling).filter(Counselling.id == uq).first()

#     agent_qr = db.execute(text("SELECT user.id, user.fullName, user.email, lur.status FROM user LEFT JOIN leads_user_role AS lur ON lur.userId = user.id WHERE role_id = 2 AND lur.status = 1 ORDER BY user.fullName"), {})
#     agents = [dict(row) for row in agent_qr.mappings().all()]

#     if counselling.status == 1:
#         html_content = templates.get_template("elements/leads/counselling_detail.html").render({"request": request, "counselling":counselling, "agents":agents})
#     elif counselling.status == 2:
#         html_content = templates.get_template("elements/leads/pop_assigned_counselling_detail.html").render({"request": request, "counselling":counselling, "agents":agents})
#     elif counselling.status == 3:
#         html_content = templates.get_template("elements/leads/pop_completed_counselling_detail.html").render({"request": request, "counselling":counselling, "agents":agents})

#     return {"code":1, "status":"success", "message":"Counselling detail found", "pop_body":html_content}

# @router.post("/assign_counselling")
# async def assign_counselling(request: Request, rq_data:AssignCounsellingSchema, db:Session=Depends(get_db)):
#     #form_data = await request.form()
#     counselling = db.query(Counselling).filter(and_(Counselling.id == rq_data.counselling_id, Counselling.status == 1)).first()
#     if counselling:
#         counselling.status = 2
#         counselling.agent_id = rq_data.assigned_to
#         counselling.assigned_by = rq_data.log_user
#         db.add(counselling)
#         db.commit()
#         db.refresh(counselling)
#         return {"code":1, "status":"success", "message":"Counselling assigned successfully", "form_data":counselling}
#     else:
#         return {"code":0, "status":"failed", "message":"Counselling not fount"}
    
# @router.post("/cancel_counselling")
# async def assign_counselling(request: Request, rq_data:CancelCounsellingSchema, db:Session=Depends(get_db)):
#     #form_data = await request.form()
#     counselling = db.query(Counselling).filter(and_(Counselling.id == rq_data.counselling_id)).first()
#     if counselling:
#         counselling.status = 4
#         counselling.cancel_by = rq_data.log_user
#         db.add(counselling)
#         db.commit()
#         db.refresh(counselling)
#         return {"code":1, "status":"success", "message":"Counselling canceled successfully", "form_data":counselling}
#     else:
#         return {"code":0, "status":"failed", "message":"Counselling not fount"}
    