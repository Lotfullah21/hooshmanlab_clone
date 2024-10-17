from django.urls import path
from .views import  register_page, login_page,verify_email_token, verify_otp, send_otp, register_instructor_page, login_instructor_page, verify_instructor_email_token, add_course, instructor_dashboard_page, upload_image_page, edit_image, delete_image

urlpatterns = [
    path("login/", login_page, name="login_view"),
    path("register/",register_page, name="register_view"),
    path("verify/<token>/",verify_email_token, name="verify_email_token"),
    path("send_otp/<email>/",send_otp, name="send_otp_view"),
    path("verify_otp/<email>/",verify_otp, name="verify_otp_view"),  
    path("instructor/register", register_instructor_page, name="instructor_register_view"),
    path("instructor/login/", login_instructor_page, name="instructor_login_view"),
    path("instructor/verify/<token>/",verify_instructor_email_token, name="verify_instructor_email_token"),
    path("dashboard/", instructor_dashboard_page, name="instructor_dashboard_view"),
    path("add_course/", add_course, name="add_course_view"),
    path("upload_image/", upload_image_page, name="upload_image_view"),
    path("edit_image/<id>", edit_image, name="edit_image_view"),
    path("delete_image/<id>", delete_image, name="delete_image_view"),
    ]







