from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib import messages
from .models import Student, Instructor, Course
from .utils import generate_token, send_token_email, send_otp_email, send_instructor_token_email, generate_slug
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import datetime







import random

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        
        # Check if the email or phone number already exists
        user_exists = User.objects.filter(Q(email=email) | Q(student__phone_number=phone_number)).exists()
    
        if user_exists:
            messages.error(request, "A user with this email or phone number already exists.")
            return redirect("register_view")
        
        # Create User with the base user model
        user = User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        
        # Create a student profile
        student = Student.objects.create(
            user=user, 
            first_name=first_name,
            last_name = last_name, 
            phone_number=phone_number,
            full_name = f"{first_name} {last_name}",
            email_verification_token = generate_token(),
            email=email
        )
        send_token_email(email, student.email_verification_token)
        messages.success(request, "Registration successful! An email has been sent to your email.")  
    return render(request, "accounts/register.html")


def verify_email_token(request, token):
    try:
        # Fetch the user with the provided token
        user = Student.objects.get(email_verification_token=token)
        # Set the user as verified
        user.is_verified = True
        user.save()
        messages.success(request, "Email verified successfully!")
        return redirect("login_view")
    
    except Student.DoesNotExist:
        # Handle case where the token is invalid or user is not found
        return HttpResponse("Token is invalid or expired")
    
    except Exception as e:
        # Handle any other potential errors
        return HttpResponse(f"An error occurred: {str(e)}")

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("user_email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            try:
                student = Student.objects.get(user=user)
                if not student.is_verified:
                    messages.error(request, "your account is not verified")
                    return redirect("register_view")
                # if the user is verified, logged them
                login(request, user)
                return redirect("home_view")
            except Student.DoesNotExist:
                messages.error(request,"User with these credentials does not exist")
                return redirect("login_view")
        else:
            messages.error(request,"Invalid email or password")
            return redirect("login_view")
    return render(request, "accounts/login.html")


def send_otp(request, email):
    """It checks if the user already registered, if registered, it will send an otp, if not, it guides the user to register page."""
    try:
        student = Student.objects.get(email=email)
    except ObjectDoesNotExist:
        messages.warning(request, "User does not exist, first register, then try login through otp")
        return redirect("register_view")
    
    otp = random.randint(100, 10000)
    student.otp = otp  # Set the OTP directly
    student.save()
    print("EMAIL ====",email)
    print("OTP ====",otp)
    send_otp_email(email, otp)
    messages.success(request, "An OTP has been sent to your email")
    return redirect(f"/account/verify_otp/{email}")


def verify_otp(request, email):
    """gets the otp from the user and login the user

    Args:
        request (_type_): _description_
        email (_type_): the email which otp had been sent to

    Returns:
        _type_: page
    """

    if request.method=="POST":
        otp = request.POST.get("otp")
        student = Student.objects.get(email=email)
        if otp==student.otp:
            messages.success(request,"login successful")
            login(request, student.user)
            return redirect("home_view")
    return render(request, "accounts/otp_auth.html")


## Instructor



def register_instructor_page(request):
    if request.method=="POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        course_name = request.POST.get("course_name")
        
        instructor = Instructor.objects.filter(email=email, phone_number=phone_number)
        if instructor.exists():
            messages.error(request,"A user with the given email or password already exists")    
            return redirect("register_instructor_view")
        
        user = User.objects.create(username=email
                                , first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        
        instructor = Instructor.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name, 
            course_name=course_name,
            email=email,
            phone_number=phone_number,
            email_verification_token = generate_token()
        )
        send_instructor_token_email(email, instructor.email_verification_token)
        messages.success(request, "Registration Successful!! An email has been sent to your email")
        return redirect("instructor_login_view")
    return render(request, "accounts/instructor/register_instructor.html")


def verify_instructor_email_token(request, token):
    try:
        user = Instructor.objects.get(email_verification_token=token)
        user.is_verified=True
        user.save()
        messages.success(request,"Email is verified successfully!!!")
        return redirect("instructor_login_view")
    except Instructor.ObjectDoesNotExist:
        return HttpResponse("Token is invalid or expired")
    except Exception as e:
        # Handle any other potential errors
        return HttpResponse(f"An error occurred: {str(e)}")
    

def login_instructor_page(request):
    if request.method=="POST":
        email = request.POST.get("user_email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        if user:
            instructor = Instructor.objects.filter(is_verified=True, email=email).first()
            if instructor:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home_view")
            else:
                messages.error(request, "User is not verified, please verify your account first")
                return redirect("instructor_login_view")
        messages.error(request,"Email or password is invalid!!!")
        return redirect("instructor_login_view")
    return render(request, "accounts/instructor/login_instructor.html")




@login_required
def instructor_dashboard_page(request):
    courses = Course.objects.filter(course_instructor=request.user.instructor)
    print(courses)
    context = {"courses":courses}
    return render(request, "accounts/instructor/instructor_dashboard.html", context)


@login_required
def add_course(request):
    try:
        if request.method == "POST":
            course_title = request.POST.get("course_title")
            course_description = request.POST.get("course_description")
            course_level = request.POST.get("course_level")
            course_starting_date = request.POST.get("course_starting_date")
            course_ending_date = request.POST.get("course_ending_date")
            course_price = request.POST.get("course_price")
            slug_field = generate_slug(course_title)
            # check if all fields are provided
            if not (course_title and course_description and course_level and course_starting_date and course_ending_date and course_price):
                    messages.error(request, "All fields are required.")
                    return redirect("add_course_view")
            try:
                # retrieve the instructor associated with the logged-in user
                instructor = Instructor.objects.get(user=request.user)
                
                # parse the starting and ending dates
                start_date = datetime.strptime(course_starting_date, '%Y-%m-%d')
                end_date = datetime.strptime(course_ending_date, '%Y-%m-%d')
                
                # check if the end date is after the start date
                if end_date <= start_date:
                    messages.error(request, "End date must be after starting date.")
                    return redirect("add_course_view")

                # calculate the course duration in weeks
                course_duration_in_weeks = (end_date - start_date).days // 7
                # Create the course
                Course.objects.create(
                    course_instructor=instructor,
                    course_title=course_title,
                    course_description=course_description,
                    course_duration=f"{course_duration_in_weeks} weeks",
                    course_level=course_level,
                    # store as datetime object
                    course_starting_date=start_date,  
                    course_ending_date=end_date,    
                    course_price=course_price,
                    course_slug=slug_field
                )
                messages.success(request, "Course is created successfully.")
                return redirect("add_course_view")
            except ValueError as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect("add_course_view")    
        # Render the add course form for GET requests
        return render(request, "accounts/instructor/add_course.html")
    except Instructor.DoesNotExist:
        messages.error(request, "You don't have permission to add courses.")
        return redirect("instructor_login_view")
    

def upload_image_page(request):
    return render(request, "accounts/instructor/upload_image.html")


def edit_image(request, id):
    return render(request, "accounts/instructor/upload_image.html")


def delete_image(request, id):
    return render(request, "accounts/instructor/upload_image.html")



