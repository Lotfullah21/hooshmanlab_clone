from django.shortcuts import render, redirect
from accounts.models import Course, CourseEnrollment
from django.shortcuts import get_object_or_404
from django.contrib import messages
def index(request):
    courses = Course.objects.all()
    if request.method=="POST":
        searched_name = request.POST.get("search_input")
        searched_sort = request.POST.get("sort_by")
        if searched_name:
            courses = courses.filter(course_title__icontains=searched_name)
        if searched_sort:
            if searched_sort=="low_to_high":
                courses = courses.order_by("course_price")
            elif searched_sort=="high_to_low":
                courses = courses.order_by("-course_price")
            else:
                courses = courses.filter(course_title__icontains=searched_name)
    context = {"courses":courses}
    return render(request, "home/index.html", context=context)



def single_course_page(request, slug):
    course = get_object_or_404(Course, course_slug=slug) 
    if request.method=="POST":
        if request.user.instructor:
            messages.error(request, "Please login as a student to enroll into a course")
            return redirect("login_view")   
        CourseEnrollment.objects.create(
            course = course, 
            course_user = request.user.student   
        )
        messages.success(request, "You are successfully enrolled") 
        return redirect("home_view")
    return render(request, "home/single_course.html", context={"course":course})