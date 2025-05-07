from datetime import datetime
from app.api.v1.models.BookingModel import BookingTagMail
from app.api.v1.models.UserModel import User, RegistrationMailLog
from .helper import SendEmail, nl2br
from .common import GetStudentEmailListForTagMail, GetListTags, GetRegisteredUsersByIds

def SendTagMailToApprove(list_id, mentor_detail, mail_subject, body, to_tas_str, avoid_tag_str, compose, db):
    students = GetStudentEmailListForTagMail(compose.to_tags, compose.avoid_tags, mentor_detail["id"],  db)
    
    total_students = len(students["emails"])
    subject = f'APPROVAL : {mentor_detail["fullName"]} wants to send a mail to {total_students} students'
    from_email = "no-reply@forumias.com"
    from_name = "[SIMS Tag] ForumIAS Academy"
    student_to = [
            {"email": "forumias@gmail.com"},
            {"email": "director@flaviant.com"},
            {"email": "shantanu@stellardigital.in"},
            {"email": "chandan@stellardigital.in"}
        ]
    '''student_to = [
            {"email": "stellardevteam@gmail.com"},
            {"email": "chandan@stellardigital.in"}
        ]'''
    body_html = nl2br(body)
    body_student = f"""<div>
				<div style="background-color:#f4f4f4;padding:20px">
				<div style="max-width:600px;margin:0 auto">
				<div style="background:#fff;font:14px sans-serif;color:#737373;margin-bottom:20px">
				<div style="background:#f1f1f1;padding-bottom:20px;padding-top:20px">
				<div class="adM"><br></div>
				<img width="150" alt="forumIAS" style="display:block;padding-left:30px;max-width:100%" src="http://academy.forumias.com/assets/images/forum_IAS.jpg" class="CToWUd a6T" tabindex="0">
				</div>
				<div style="padding:30px 20px;line-height:1.5em;color:#737373">
				<p>Hi Manager,</p>	
                <p>Please review the below mail content:-</p>
                <p><b>Mentor Name:</b> {mentor_detail["fullName"]}</p>	
                <p><b>Tags:</b> {to_tas_str}</p>
                <p><b>Avoid Tags:</b> {avoid_tag_str}</p>	
                <p><b>Subject:</b> {mail_subject}</p>	
                <p><b>Body:</b> {body_html}</p>		
                <div style="margin-top: 20px;">
                    <a href="https://sims.forumias.com/bookings/per_mail_tag.php?ref={list_id}&s=1" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">Approve</a>
                    <a href="https://sims.forumias.com/bookings/per_mail_tag.php?ref={list_id}&s=2" style="background-color: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reject</a>
                </div>	
				
				<p style="color:#737373;margin-top:100px;"> Thanks,</p>
				<p style="color:#737373;"> Your Team at ForumIAS</p>
				
				</div>
				</div>
				<div style="font:11px sans-serif;color:#737373">
				<p style="font-size:11px;color:#737373">@copyright ForumIAS.</p>
				</div>
				</div>
				</div>
			</div>"""
    #SendEmail(to, from_email, from_name, subject, body, cc, attachment, tag)
    result = SendEmail(student_to, from_email, from_name, subject, body_student, 'Tag list to approve')
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQq")
    print(result)
    return True


def SendTagListMailToStudents(id, db):
    list_detail = db.query(BookingTagMail).filter(BookingTagMail.id == id).first()
    if list_detail.mentor_id != 0:
        from_id = list_detail.mentor_id
    else:
        from_id = list_detail.manager_id
    from_user = db.query(User).filter(User.id == from_id).first()
    
    subject = list_detail.subject
    from_email = "no-reply@forumias.com"
    from_name = f"{from_user.fullName} [ForumIAS]"
    #main_to = [{"email":"dev@flaviant.com"}]
    
    students = GetStudentEmailListForTagMail(list_detail.to_tags, list_detail.avoid_tags, from_id,  db)
    
    list_detail.student_ids = students['ids']
    db.add(list_detail)
    db.commit()

    for student in students['emails']:
        student_to = [{"email": student["email"]}]

        name_var = "[[name]]"
        email_var = "[[email]]"
        roll_var = "[[rollnumber]]"
        body_html = nl2br(list_detail.body)
        body_html = body_html.replace(name_var, student["name"]) #Replace name
        body_html = body_html.replace(email_var, student["email"]) #Replace email
        body_html = body_html.replace(roll_var, str(student["roll_number"])) #Replace roll_number
        body_student = f"""<div>
                    <div style="background-color:#f4f4f4;padding:20px">
                    <div style="max-width:600px;margin:0 auto">
                    <div style="background:#fff;font:14px sans-serif;color:#737373;margin-bottom:20px">
                    <div style="background:#f1f1f1;padding-bottom:20px;padding-top:20px">
                    <div class="adM"><br></div>
                    <img width="150" alt="forumIAS" style="display:block;max-width:100%; margin:0 auto" src="http://academy.forumias.com/assets/images/forum_IAS.jpg" class="CToWUd a6T" tabindex="0">
                    </div>
                    <div style="padding:30px 20px;line-height:1.5em;color:#737373">
                    <p>{body_html}</p>	
                    
                    
                    </div>
                    </div>
                    <div style="font:11px sans-serif;color:#737373">
                        <p style="color:#737373;margin-top:100px;">-------------</p>
                        <p style="font:11px; color:#737373;"> This email is being sent from: 19, Pusa Road, 2nd Floor, IAPL House, Opposite Metro Pillar 95-96, Karol Bagh, New Delhi-110005. Email Unique ID #{id}</p>
                        <p style="font-size:11px;color:#737373">@copyright ForumIAS.</p>
                    </div>
                    </div>
                    </div>
                </div>"""
        #SendEmail(to, from_email, from_name, subject, body, cc, attachment, tag)
        result = SendEmail(student_to, from_email, from_name, subject, body_student, 'Tag mail to student', '', '')
        print("++++++++++++++++++++++++++++++++++Mail Sent To:+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(student_to)
        print(result)
    return True





def SendListConfMailToMentor(id, db):
    list_detail = db.query(BookingTagMail).filter(BookingTagMail.id == id).first()

    if list_detail.mentor_id != 0:
        from_id = list_detail.mentor_id
    else:
        from_id = list_detail.manager_id

    from_user = db.query(User).filter(User.id == from_id).first()

    tags = GetListTags(list_detail.id, db)

    subject = 'APPROVED : Your email has been approved '
    from_email = "no-reply@forumias.com"
    from_name = "[SIMS Tag] ForumIAS Academy"
    
    to = [
            {"email": from_user.email}
        ]
    body_html = nl2br(list_detail.body)
    body_student = f"""<div>
				<div style="background-color:#f4f4f4;padding:20px">
				<div style="max-width:600px;margin:0 auto">
				<div style="background:#fff;font:14px sans-serif;color:#737373;margin-bottom:20px">
				<div style="background:#f1f1f1;padding-bottom:20px;padding-top:20px">
				<div class="adM"><br></div>
				<img width="150" alt="forumIAS" style="display:block;padding-left:30px;max-width:100%" src="http://academy.forumias.com/assets/images/forum_IAS.jpg" class="CToWUd a6T" tabindex="0">
				</div>
				<div style="padding:30px 20px;line-height:1.5em;color:#737373">
				<p>Dear {from_user.fullName},</p>	
                <p>Your email #{list_detail.id} has been approved by the LMS team.</p>
                <p>Please find the content of the email below:</p><br/>
                <p><b>Tags:</b> {tags["to_tag"]}</p>
                <p><b>Avoid Tags:</b> {tags["avoid_tag"]}</p>	
                <p><b>Subject:</b> {list_detail.subject}</p>	
                <p><b>Body:</b> {body_html}</p>		
                
				
				<p style="color:#737373;margin-top:100px;"> Thanks,</p>
				<p style="color:#737373;"> Your Team at ForumIAS</p>
				
				</div>
				</div>
				<div style="font:11px sans-serif;color:#737373">
				<p style="font-size:11px;color:#737373">@copyright ForumIAS.</p>
				</div>
				</div>
				</div>
			</div>"""
    #SendEmail(to, from_email, from_name, subject, body, cc, attachment, tag)
    result = SendEmail(to, from_email, from_name, subject, body_student, 'Taglist confirmation to mentor')
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQq")
    print(result)
    return True

#Working-------------------------------------------------------------------------
def SendTestingMailToMentor(data, db):
    if data.mentor_id != 0:
        from_id = data.mentor_id
    else:
        from_id = data.manager_id
    from_user = db.query(User).filter(User.id == from_id).first()
    subject = f'[Test Mail] {data.subject}'
    from_email = "no-reply@forumias.com"
    from_name = "[SIMS Tag] ForumIAS Academy"
    
    to = [
            {"email": from_user.email}
        ]
    body_html = nl2br(data.body)
    body_student = f"""<div>
				<div style="background-color:#f4f4f4;padding:20px">
				<div style="max-width:600px;margin:0 auto">
				<div style="background:#fff;font:14px sans-serif;color:#737373;margin-bottom:20px">
				<div style="background:#f1f1f1;padding-bottom:20px;padding-top:20px">
				<div class="adM"><br></div>
				<img width="150" alt="forumIAS" style="display:block;padding-left:30px;max-width:100%" src="http://academy.forumias.com/assets/images/forum_IAS.jpg" class="CToWUd a6T" tabindex="0">
				</div>
				<div style="padding:30px 20px;line-height:1.5em;color:#737373">
				<p>{body_html},</p>	
                
				<p style="color:#737373;margin-top:100px;"> Thanks,</p>
				<p style="color:#737373;"> Your Team at ForumIAS</p>
				
				</div>
				</div>
				<div style="font:11px sans-serif;color:#737373">
				<p style="font-size:11px;color:#737373">@copyright ForumIAS.</p>
				</div>
				</div>
				</div>
			</div>"""
    #SendEmail(to, from_email, from_name, subject, body, cc, attachment, tag)
    result = SendEmail(to, from_email, from_name, subject, body_student, 'Tag testing mail by mentor')
    print(result)
    return True

def SendRegistrationMailToStudents(data, db):
    subject = data.subject
    from_email = "no-reply@forumias.com"
    from_name = "ForumIAS Academy"
    #main_to = [{"email":"dev@flaviant.com"}]
    
    students = GetRegisteredUsersByIds(data.mail_sent_to, db)
    
    stud_idz = []
    for student in students:
        print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        print(student.email)
        #student_to = [{"email": student.email}]
        student_to = [{"email": "stellardevteam@gmail.com"},
                      {"email": "chandan@stellardigital.in"}
                      ]

        name_var = "[[name]]"
        email_var = "[[email]]"
        phone_var = "[[phone]]"
        roll_var = "[[rollnumber]]"
        body_html = nl2br(data.body)
        body_html = body_html.replace(name_var, student.fullName) #Replace name
        body_html = body_html.replace(email_var, student.email) #Replace email
        body_html = body_html.replace(phone_var, student.phone) #Replace phone
        body_html = body_html.replace(roll_var, str(student.roll_number)) #Replace roll_number
        body_student = f"""<div>
                    <div style="background-color:#f4f4f4;padding:20px">
                    <div style="max-width:600px;margin:0 auto">
                    <div style="background:#fff;font:14px sans-serif;color:#737373;margin-bottom:20px">
                    <div style="background:#f1f1f1;padding-bottom:20px;padding-top:20px">
                    <div class="adM"><br></div>
                    <img width="150" alt="forumIAS" style="display:block;max-width:100%; margin:0 auto" src="http://academy.forumias.com/assets/images/forum_IAS.jpg" class="CToWUd a6T" tabindex="0">
                    </div>
                    <div style="padding:30px 20px;line-height:1.5em;color:#737373">
                    <p>{body_html}</p>	
                    
                    
                    </div>
                    </div>
                    <div style="font:11px sans-serif;color:#737373">
                        <p style="color:#737373;margin-top:100px;">-------------</p>
                        <p style="font:11px; color:#737373;"> This email is being sent from: 19, Pusa Road, 2nd Floor, IAPL House, Opposite Metro Pillar 95-96, Karol Bagh, New Delhi-110005.</p>
                        <p style="font-size:11px;color:#737373">@copyright ForumIAS.</p>
                    </div>
                    </div>
                    </div>
                </div>"""
        result = SendEmail(student_to, from_email, from_name, subject, body_student, 'registration mail from admin', '', '')
        stud_idz.append(str(student.id))
        print("++++++++++++++++++++++++++++++++++Mail Sent To:+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(student_to)
        break
        #print(result)
    stud_idz_str = ','.join(stud_idz)
    mail_dt = datetime.strptime(data.registration_date, "%Y-%m-%d")
    obj = RegistrationMailLog(agent_id=data.agent_id, subject=data.subject, body = data.body, mail_sent_to = stud_idz_str, status = 1, registration_date = mail_dt)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return True
