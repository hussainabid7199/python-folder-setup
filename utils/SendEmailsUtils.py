from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os

from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader

dotenv_path = ".env"
load_dotenv(dotenv_path)

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(email: str,  email_body):
    print(f"📩 Attempting to send email to: {email} with subject: Verify your email")
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = "Verify Your Email"
    
        msg.attach(MIMEText(email_body, "html"))
    
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        
        print("Email sent successfully")
        return {"status": 200, "message": "Email Sent Successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Email sent failed")
            