import requests
import json
from cryptography.fernet import Fernet, InvalidToken

def SendLoginOTP(phone, otp):
    print("In otp")
    phone = str(91) + str(phone)
    url = "https://control.msg91.com/api/v5/otp"

    payload = {'template_id': '607a91263a0ca765df060936', 'mobile':phone, 'var1':'ForumIAS', 'otp':otp, 'otp_expiry':1, 'authkey': '150066ASgxBjCBBIb59e078f6'}
    files=[]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    return True

def EncriptMe(user_data):
    key = "wEqSuKfhvruT7Z3i1rwSMZhXOLXDXyBQLeEyYWr4U-Q="
    fernet = Fernet(key)
    #user_data_str = str(user_data)
    user_data_str = user_data.encode('utf-8')
    encrypted_msg=fernet.encrypt(user_data_str)
    return encrypted_msg

def DecriptMe(encrypted_msg):
    key = "wEqSuKfhvruT7Z3i1rwSMZhXOLXDXyBQLeEyYWr4U-Q="
    fernet = Fernet(key)
    try:
        decrypted_msg=fernet.decrypt(encrypted_msg)
        decrypted_msg=decrypted_msg.decode('utf-8')
        return decrypted_msg
    except InvalidToken:
        return False
    
def AuthUser(request):
    user_token = request.META.get('HTTP_TOKEN', None)
    if user_token:
        token_str = DecriptMe(user_token)
        if token_str:
            token_list = token_str.split(",")
            log_user = {"id":token_list[0], "phone":token_list[1], "email":token_list[2], "role":token_list[3], "fullName":token_list[4], "userName":token_list[5]}
            return log_user
        else:
            return False
    else: 
        return False


#This function not used till now
def SendEmailWithAttachment(to, from_email, from_name, subject, body, cc, attachment, attch_name, tag):
    api_url = "https://emailapi.netcorecloud.net/v5.1/mail/send"
    api_key = "6d2248449728b25212602f6ee315aaba"
    
    
    payload = {
        "from": {
            "email": from_email,
            "name": from_name
        },
        "reply_to": from_email,
        "subject": subject,
        "tags": [tag],
        "content": [
            {
                "type": "html",
                "value": body
            }
        ],
        "personalizations": [
            {
                "to": to,
                #"cc": [{ "email": "april.ludgate@parksnrec.com" }, { "email": "ben.white@parksnrec.com" }],
                #"bcc": [{ "email": "jerry.gergich@parksnrec.com" }],
                #"token_to": "noble-land-mermaid",
                #"token_cc": "MSGID657243",
                #"token_bcc": "MSGID657244",
                
            }
        ],
        "attachments": [
            {
            "name": attch_name,
            "content": attachment
            }
        ]
       
    }
    headers = {
        "api_key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    #response = requests.post(url, json=payload, headers=headers)

    
    #######################################################

    try:
        # Make a POST request to Pepipost API
        response = requests.post(api_url, json=payload, headers=headers)
        print("Email response")
        print(response.json())
        # Check the response status code
        return response.status_code
        '''
        if response.status_code == 200:
            return HttpResponse("Email sent successfully!")
        else:
            return HttpResponse(f"Failed to send email. Status code: {response.status_code}")
        '''
    except Exception as e:
        return str(e)

def SendEmail(to, from_email, from_name, subject, body, tag, cc='', bcc=''):
    api_url = "https://emailapi.netcorecloud.net/v5.1/mail/send"
    api_key = "6d2248449728b25212602f6ee315aaba"
    personalize = {"to":to}
    if cc:
        personalize["cc"] = cc
    if bcc:
        personalize["bcc"] = bcc

    
    payload = {
        "from": {
            "email": from_email,
            "name": from_name
        },
        "reply_to": from_email,
        "subject": subject,
        "tags": [tag],
        "content": [
            {
                "type": "html",
                "value": body
            }
        ],
        "personalizations": [
            personalize
        ]
       
    }
    headers = {
        "api_key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    #response = requests.post(url, json=payload, headers=headers)

    
    #######################################################

    try:
        # Make a POST request to Pepipost API
        response = requests.post(api_url, json=payload, headers=headers)
        print("Email response")
        print(response.json())
        # Check the response status code
        return response.status_code
        '''
        if response.status_code == 200:
            return HttpResponse("Email sent successfully!")
        else:
            return HttpResponse(f"Failed to send email. Status code: {response.status_code}")
        '''
    except Exception as e:
        return str(e)
 
def SendLeadWhatsappMsg():
    recipient_number = '7840057432'
    recipient_number1 = '9958028909'
    data = {
        "integrated_number": "919311740901",
        "content_type": "template",
        "payload": {
            "messaging_product": "whatsapp",
            "type": "template",
            "template": {
                "name": "test_lead",
                "language": {
                    "code": "en_US",
                    "policy": "deterministic"
                },
                "namespace": None,
                "to_and_components": [
                    {
                        "to": [
                            recipient_number, recipient_number1
                        ],
                        "components": {
                            "body_1": {
                                "type": "text",
                                "value": "User"
                            },
                            "body_2": {
                                "type": "text",
                                "value": "This is a test msg"
                            }
                        }
                    }
                ]
            }
        }
    }
    json_string = json.dumps(data, indent=4)
    

    url = "https://api.msg91.com/api/v5/whatsapp/whatsapp-outbound-message/bulk/"
    payload=json_string
    files=[]
    headers = {'Content-Type':'application/json', 'authkey':'150066ASgxBjCBBIb59e078f6'}
    #headers = header_details
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    data = response.json()
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
    print(data)
    return data

def cleanCommaValues(tags):
    tag_list = tags.split(",")  # Split the input string by commas
    tag_list = [tag.strip() for tag in tag_list]  
    return tag_list
def cleanCommaIntValues(tags):
    tag_list = tags.split(",")  # Split the input string by commas
    tag_list = [int(tag.strip()) for tag in tag_list]  
    return tag_list

def nl2br(value: str) -> str:
    """Convert newlines to <br> tags."""
    return value.replace("\n", "<br>")