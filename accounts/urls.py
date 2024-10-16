from django.urls import path
from .views import  register_page, login_page,verify_email_token, verify_otp, send_otp, register_instructor_page, login_instructor_page, verify_instructor_email_token

urlpatterns = [
    path("login/", login_page, name="login_view"),
    path("register/",register_page, name="register_view"),
    path("verify/<token>/",verify_email_token, name="verify_email_token"),
    path("send_otp/<email>/",send_otp, name="send_otp_view"),
    path("verify_otp/<email>/",verify_otp, name="verify_otp_view"),  
    path("instructor/register", register_instructor_page, name="instructor_register_view"),
    path("instructor/login/", login_instructor_page, name="instructor_login_view"),
    path("instructor/verify/<token>/",verify_instructor_email_token, name="verify_instructor_email_token")]







