```html
<!-- instructor_dashboard -->
{%block content%}
	<div
		class="">
		{%for course in courses%}
				<img class="w-full" src="{{ course.images.first.image.url }}" alt="Course image" />
			</div>
		</div>

		{%endfor%}
	</div>
{% endblock %}
```

Look at the models

```py
class Course(models.Model):
    course_instructor= models.ForeignKey('Instructor', on_delete = models.CASCADE, related_name="courses")
    # rest of the fields

class CourseImageField(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="course_images")
    # rest of the fields

```

Now, we can have multiple images for one course, but one same image cannot be added to multiple courses.

#### Accessing to images through related_name

Before going through the method, keep note of these three methods.

`.get`: It returns a single object, if not, raise `DoestNotExist` error; use this if us are sure there is an item.
`.filter`: It returns a QuerySet (`Collection of objects`), to access individual objects, we need to loop through it.
`.first()`: It returns the first object from the QuerySet and if not object is found,it returns None.

`ForeignKey` relationship helps us to have access to all fields of `CourseImage` model.
Hence, `course_object.related_name.field_name`.

1. ##### Using first

Use `first` when we need a single instance

```py
# views.py(instructor_dashboard_page)
# get the instance of a course
course = Courses.objects.filter(some_condition).first()
# from the first instance, get the first image from images QuerySet.
course.images.first().image.url
```

2. ##### Using filter

we will be using filter to filter the course and we might be having multiple course and for each course we need an image, the loop is done inside the html.

```py
# views.py(instructor_dashboard_page)
# get the instance of a course
courses = Courses.objects.filter(some_condition)
# from the first instance, get the first image from images QuerySet.
for course in courses:
    course.first_image = course.images.first()
```

```py

```

```html
<!-- instructor_dashboard -->
{%block content%}
	<div
		class="">
		{%for course in courses%}
				<img class="w-full" src="{{ course.first_image.image.url }}" alt="Course image" />
			</div>
		</div>
		{%endfor%}
	</div>
{% endblock %}

<!-- second approach -->
```

```html
<!-- instructor_dashboard -->
{%block content%}
	<div
		class="">
		{%for course in courses%}
				<img class="w-full" src="{{ course.images.first.image.url }}" alt="Course image" />
			</div>
		</div>
		{%endfor%}
	</div>
{% endblock %}

```

1. ##### Using get

Use `get` when we need a single instance

```py
# views.py(instructor_dashboard_page)
# get the first matching instance
course = Courses.objects.get(some_condition)
# get the image
image = course.images.first().image.url
```

#### QuerySet

A QuerySet is a collection of database queries that represent a group of objects (instances) from our database
A QuerySet represents a collection of objects. It’s like a list of database records, but it’s not the actual data until it’s evaluated.

###### Features

`Lazy Evaluation`: QuerySets are lazily evaluated, meaning they don’t hit the database until they are actually used. This allows us to build complex queries without querying the database until necessary.

`Chainable`: QuerySets can be modified by chaining different methods, allowing for complex queries that are easy to read and write.

`Iterable`: Once evaluated, a QuerySet behaves like a Python iterable (e.g., list), meaning we can loop over it, access individual elements, etc

## Instance vs Object

#### Object:

An object refers to a data structure that is created from a class. It is an entity that contains both state (data) and behavior (methods) defined by the class, any data that is created from a class.
A `class` is a blue print that defines the structure and behaviors of an entity.

#### Instance

an instance refers to the specific occurrence of an object. When we say "an instance of a class," we mean a particular object that has been instantiated from that class.
In fact both of them can be used interchangeably

### Querying students related to an instructor

```py
class CourseEnrollment(models.Model):
    course = models.ForeignKey("Course", on_delete = models.CASCADE, related_name = "enrollments")
    course_user = models.ForeignKey("Student", on_delete = models.CASCADE, related_name="enrolled_students")
    enrollment_starting_date = models.DateTimeField(auto_now_add=True)

```

```py
@login_required
def instructor_dashboard_page(request):
    courses = Course.objects.filter(course_instructor=request.user.instructor)
    # Get the enrollments for the instructor's courses
    enrollments = CourseEnrollment.objects.filter(course__in=courses).select_related("course_user")
    # Extract the enrolled students from the enrollments
    students = [enrollment.course_user for enrollment in enrollments]
    for course in courses:
        course.first_image = course.images.first()
    context = {"courses":courses, "students":students}
    return render(request, "accounts/instructor/instructor_dashboard.html", context)
```

`course__in=courses`:
This is part of a query that filters the CourseEnrollment records. The key term here is the use of `__in` and how it works with the course field:

`course__in=courses`:

course refers to the ForeignKey
field in CourseEnrollment that links to the Course model (i.e., the course that the student is enrolled in).

`__in` is a special Django query lookup that checks if a value exists within a specified list or queryset.
courses is the list of courses that belong to the current instructor. This is passed into the query.
So, `course_in=courses means`:

"Find all CourseEnrollment objects where the course is one of the courses in the courses list."
Essentially, this is filtering enrollments to only those related to the courses taught by the instructor.

```py
enrollments = CourseEnrollment.objects.filter(course__in=courses).select_related('course_user')
```

we're asking Django to find all course enrollments where the course field matches any course from the courses list (the courses the instructor teaches).
The `select_related('course_user')` part ensures that for each enrollment, the related student `(course_user)` is also fetched efficiently in the same query.

```py
# Get the enrollments for the instructor's courses
enrollments = CourseEnrollment.objects.filter(course__in=courses)
```
