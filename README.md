# Hooshmandlab Clone - Project Documentation

---

## Project Overview

The **Hooshmandlab Clone** is an online learning platform where users can enroll in courses, and instructors can create and manage their own courses. The platform is built using **Django** for both the backend and frontend (via Django templates) and uses **PostgreSQL** as the database. The platform includes authentication with user roles, allowing for differentiated access between users and instructors. The project consists of two apps:

- **Account**: Manages user authentication (login, register) and user roles.
- **Home**: Handles course display, search functionality, and course details.

---

## Table of Contents

- [Hooshmandlab Clone - Project Documentation](#hooshmandlab-clone---project-documentation)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [1. Technologies Used](#1-technologies-used)
  - [2. Project Structure](#2-project-structure)
  - [2. How to run locally](#2-how-to-run-locally)
    - [Prerequisites](#prerequisites)
    - [Setup Steps](#setup-steps)
  - [3. Features](#3-features)
    - [User Login and Authentication (Account)](#user-login-and-authentication-account)
    - [Instructor Management (Account)](#instructor-management-account)
    - [Course Display and Search (Home)](#course-display-and-search-home)
    - [Course Enrollment (Home)](#course-enrollment-home)
  - [4. Models](#4-models)
    - [Student](#student)
    - [Instructor](#instructor)
      - [Course](#course)
    - [CourseImageField](#courseimagefield)
    - [CourseManager](#coursemanager)
    - [CourseEnrollment](#courseenrollment)
  - [5. URLS](#5-urls)
    - [Account URLs](#account-urls)
    - [Home URLs](#home-urls)
  - [6. 7. Future Enhancements](#6-7-future-enhancements)

---

## 1. Technologies Used

- **Backend and Frontend**: Django (with Django templates for frontend rendering)
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication system
- **UI Framework**: Bootstrap (for styling)
- **Database ORM**: Django ORM

---

## 2. Project Structure

Here is the high-level folder structure for the project:

```bash
hooshmandlab_clone/
├── manage.py
├── hooshmandlab_clone/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── account/  # Authentication-related logic
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── account/
│           ├── login.html
│           ├── register.html
│           └── dashboard.html
├── home/  # Course-related logic
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── home/
│           ├── course_list.html
│           ├── course_detail.html
│           ├── search.html
├── README.md
└── .gitignore
```

## 2. How to run locally

[project_setup.md](./documents/PROJECTSETUP.MD)

#### Prerequisites

- Python (Version 3.8 or above)
- PostgreSQL (installed and configured locally)
- Pip (Python package manager

### Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hooshmandlab_clone.git
cd hooshmandlab_clone

```

2. Create a virtual environment:

```py
python3 -m venv venv
source venv/bin/activate

```

3. Install the dependencies:

```py
pip install -r requirements.txt

```

4. Set up PostgreSQL:

```py
psql
CREATE DATABASE hooshmandlab_clone;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hooshmandlab_clone TO myuser;

```

5. Configure Django settings:

In hooshmandlab_clone/settings.py, update the DATABASES section to match your PostgreSQL settings:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hooshmandlab_clone',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}

```

6. Run migrations:

```py
Run migrations:
```

7. python manage.py runserver

```py
python manage.py runserver
```

## 3. Features

[authentication_README.md](./documents/VIEWS.MD)

[logout_README.md](./documents/LOGOUT.MD)

### User Login and Authentication (Account)

- **Functionality**: Users (students and instructors) can log in and register. The platform uses Django's built-in authentication system with role differentiation.
  - **User**: Can browse and enroll in courses.
  - **Instructor**: Can create, edit, and manage their own courses.
- **Registration**: Users can register, and during registration, they can choose whether they want to be an instructor or a regular user.

### Instructor Management (Account)

- **Instructor Dashboard**: After login, instructors have access to a dashboard where they can manage their courses.
- **Course Creation**: Instructors can create new courses through a form.
- **Course Editing**: Instructors can update or delete their courses.

### Course Display and Search (Home)

- **Course Listing**: All courses are listed on the homepage.
- **Course Search**: Users can search for courses using a search field to find courses based on titles or descriptions.
- **Course Detail Page**: Clicking on a course shows detailed information, including the instructor and course description.

### Course Enrollment (Home)

- **Enrollment**: Users can enroll in a course by clicking the "Enroll" button on the course detail page.

## 4. Models

[models_README.md](./documents/MODELS.MD)

### Student

Represents the users who enroll in courses.

```python
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(unique=True, max_length=120,
                                    validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    email_verification_token = models.EmailField()
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.full_name + " is verified = " + str(self.is_verified)
```

### Instructor

Represents the users who can create and manage courses.

```py
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, default="king")
    last_name = models.CharField(max_length=120, default="king")
    phone_number = models.CharField(unique=True, max_length=120,
                                    validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    email_verification_token = models.EmailField()
    course_name = models.CharField(max_length=120)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)
    otp = models.CharField(max_length=120, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name + " is verified = " + str(self.is_verified)

```

#### Course

Represents the courses available on the platform.

```py
class Course(models.Model):
    LEVEL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    course_instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE, related_name="courses")
    course_title = models.CharField(max_length=120)
    course_description = models.TextField()
    course_duration = models.CharField(max_length=120)
    course_level = models.CharField(choices=LEVEL_CHOICES, max_length=120)
    course_starting_date = models.DateField()
    course_ending_date = models.DateField()
    course_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    course_slug = models.SlugField(max_length=1000, unique=True)

    def __str__(self) -> str:
        return f"{self.course_title} - {self.course_description}"

```

### CourseImageField

Stores images associated with a course.

```py
class CourseImageField(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="course_images")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Image for {self.course.course_title} created"

```

### CourseManager

Represents the manager for a specific course.

```py
class CourseManager(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="course_manager")
    manager_name = models.CharField(max_length=120)
    manager_contact = models.CharField(max_length=140)

    def __str__(self) -> str:
        return f"{self.manager_name} - {self.course.course_title}"

```

### CourseEnrollment

Tracks which students are enrolled in which courses.

```py
class CourseEnrollment(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="enrollments")
    course_user = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="enrolled_students")
    enrollment_starting_date = models.DateTimeField(auto_now_add=True)


```

## 5. URLS

[static_files_README.md](./documents/STATICFILES.MD)

[accessing_static_files_README.md](./documents/ACCESSINGSTATICFILES.MD)

#### Account URLs

```py

from django.urls import path
from .views import register_page, login_page, verify_email_token, verify_otp, send_otp, \
    register_instructor_page, login_instructor_page, verify_instructor_email_token, \
    add_course, instructor_dashboard_page, upload_image_page, edit_image_page, delete_image, instructor_logout_view

urlpatterns = [
    path("login/", login_page, name="login_view"),
    path("register/", register_page, name="register_view"),
    path("verify/<token>/", verify_email_token, name="verify_email_token"),
    path("send_otp/<email>/", send_otp, name="send_otp_view"),
    path("verify_otp/<email>/", verify_otp, name="verify_otp_view"),
    path("instructor/register", register_instructor_page, name="instructor_register_view"),
    path("instructor/login/", login_instructor_page, name="instructor_login_view"),
    path("instructor/logout/", instructor_logout_view, name="instructor_logout_view"),
    path("instructor/verify/<token>/", verify_instructor_email_token, name="verify_instructor_email_token"),
    path("dashboard/", instructor_dashboard_page, name="instructor_dashboard_view"),
    path("add_course/", add_course, name="add_course_view"),
    path("upload_image/<course_slug>", upload_image_page, name="upload_image_view"),
    path("edit_image/<course_slug>", edit_image_page, name="edit_image_view"),
    path("delete_image/<id>", delete_image, name="delete_image_view"),
]
```

#### Home URLs

```py
from django.urls import path
from .views import index, single_course_page

urlpatterns = [
    path("", index, name="home_view"),
    path("<slug>/", single_course_page, name="single_course_view"),
]

```

## 6. 7. Future Enhancements

- Deployment: Deploy the frontend and backend using services like PythonAnywhere for Django and Heroku for PostgreSQL hosting.
- Enhance User Roles: Implement additional roles, such as course reviewers or admin-level controls.
- Payment Integration: Add support for payments to allow users to purchase courses.
- Course Content: Expand course features to include multimedia uploads such as video lectures and interactive quizzes.
