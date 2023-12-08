import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import random
from django.conf import settings


def send_email(recipient_email, receiver_name):
    password = settings.APP_PASSWORD
    sender_email = settings.SENDER_EMAIL

    print(password, sender_email)

    print(recipient_email, receiver_name)

    code = random.randint(10000, 99999)
    subject = 'Book store web app'

    body = f"""
    Dear {receiver_name},
    
    We hope this message finds you well. As part of our security measures, we require you to verify your identity by entering the following verification code on our platform:
    
    Verification Code: {code}
    
    Please use the provided code to complete the verification process. If you did not initiate this request or have any concerns, please contact our support team immediately.
    
    Thank you for choosing our service.
    
    Best regards,
    Book store web app
    
    """
    # Create the MIME object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        # Log in to the Gmail account
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
    return code

