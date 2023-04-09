import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

def create_object_with_required_fields(model_instance,required_fields,request_data,result):
    for field in required_fields:
        field_value = request_data.get(field,None)
        if field_value is not None:
            model_instance[field] = field_value
        else:
            result["error"] = f"{field} is required"
            break
        
    if result.get("error",None) is None:
            model_instance.save()
            result["status"] = True
            result["response"] = f"{model_instance.__class__.__name__} saved"
    
    return result

def send_email(mail_object, receiver_address):
    result = False
    sender_address = 'emat.asdc.g4@gmail.com'
    sender_pass = 'nkgvrglfwuuwsoxb'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = mail_object.get('subject',"EMAT - Email Update")
    mail_content = mail_object.get('message',None)
    if mail_content is not None:
        message.attach(MIMEText(mail_content, 'html'))
        try:
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            result = True
        except:
                import traceback
                print(traceback.format_exc())
    
    return result
    
def generate_verification_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
