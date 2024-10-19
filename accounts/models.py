from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=120)  
    last_name = models.CharField(max_length=120)
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(unique=True,max_length=120, 
                                    validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    email_verification_token = models.EmailField()
    email= models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)
    otp = models.CharField(max_length=10, null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.full_name +"is verified = " + str(self.is_verified)

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=120, default="king")  
    last_name = models.CharField(max_length=120, default="king")
    phone_number = models.CharField(unique=True,max_length=120,
                                    validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    email_verification_token = models.EmailField()
    course_name = models.CharField(max_length=120)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to="profile", blank=True, null=True)
    otp = models.CharField(max_length=120, null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self) -> str:
        return self.first_name +"is verified = " + str(self.is_verified)


class Course(models.Model):
    LEVEL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )
    
    course_instructor= models.ForeignKey('Instructor', on_delete = models.CASCADE, related_name="courses")
    course_title = models.CharField(max_length = 120)
    course_description = models.TextField()
    # course_image = models.ImageField(upload_to='courses', blank=True, null=True) 
    course_duration = models.CharField(max_length=120)
    course_level = models.CharField(choices=LEVEL_CHOICES,max_length=120)
    course_starting_date = models.DateField()
    course_ending_date = models.DateField()
    course_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    course_slug = models.SlugField(max_length=1000, unique=True)
    
    def __str__(self) -> str:
        return f"{self.course_title} - {self.course_description}"
        
class CourseImageField(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="course_images")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Image for {self.course.course_title} created"

    
    
class CourseManager(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="course_manager")
    manager_name = models.CharField(max_length=120)
    manager_contact = models.CharField(max_length=140)
    def __str__(self) -> str:
        return f"{self.manager_name} - {self.course.course_title}"
    
class CourseEnrollment(models.Model):
    course = models.ForeignKey("Course", on_delete = models.CASCADE, related_name = "enrollments")
    course_user = models.ForeignKey("Student", on_delete = models.CASCADE, related_name="enrolled_students")
    enrollment_starting_date = models.DateTimeField(auto_now_add=True)
