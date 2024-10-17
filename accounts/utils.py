import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Course


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
    


def generate_slug(field_name):
    """Generate a unique slug based on a field name from the Course model.
    If the slug already exists, call the function recursively to generate a new one.

    Args:
        field_name (str): A field name from the Course model to be slugified.

    Returns:
        str: A unique slugified field name.
    """
    # Generate a UUID and split it by hyphens
    parts = str(uuid.uuid4()).split("-")
    slug = slugify(field_name) + "-" + parts[0]  # Combine slugified field name with UUID part
    # Check if the slug already exists
    if Course.objects.filter(course_slug=slug).exists():
        # If the slug exists, recursively call the function to generate a new one
        return generate_slug(field_name)
    return slug
