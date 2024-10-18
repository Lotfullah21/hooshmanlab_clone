from django.shortcuts import render
from accounts.models import Course

def index(request):
    courses = Course.objects.all()
    context = {"courses":courses}
    return render(request, "home/index.html", context=context)


