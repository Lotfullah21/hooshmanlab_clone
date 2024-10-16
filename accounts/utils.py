import uuid
from django.core.mail import send_mail
from django.conf import settings


def generate_token():
    """generates a token to be sent to user's email for verification

    Returns:
        _type_: string
    """
    return str(uuid.uuid4())



def send_token_email(email, token):
    subject = 'Verify your email'
    verification_url = f'http://127.0.0.1:8000/account/verify/{token}/'
    message = f'Subject: {subject}\n\nPlease click the following link to verify your email: {verification_url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
def send_instructor_token_email(email, token):
    subject = 'Please verify your email dear Andrew NG'
    verification_url = f'http://127.0.0.1:8000/account/instructor/verify/{token}/'
    message = f'Subject: {subject}\n\nPlease click the following link to verify your email: {verification_url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
    
def send_otp_email(email, otp):
    subject = 'your OTP for hooshmandlab account'
    verification_url = otp
    message = f'Subject: {subject}\n\nPlease click the following link to submit the otp: {verification_url}'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )