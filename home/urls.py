from django.urls import path
from .views import index, single_course_page

urlpatterns = [
    path("",index, name="home_view"),
    path("<slug>/",single_course_page, name="single_course_view"),
]
