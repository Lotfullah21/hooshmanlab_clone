## Instructor dashboard

#### 1. Instructor Model

```py
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ...
```

We have created one-to-one relationship between the `Instructor` model and `User` model.
Now, each `Instructor` is associated with a single `User` and each user can have one associated `Instructor`.

By having `OneToOneField(User)`, Django automatically creates a reverse relation, which in turns, we get access to the `Instructor` mode from `User` model using `user.instructor`

#### 2. Course Model

```py
class Course(models.Model):
    course_instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE, related_name="courses")
    ...
```

The `Course` model has a foreignKey field called `course_instructor` that points to the Instructor model.

using `related_name`, we will be having access all courses related to one instructor.

`instructor.courses.all()` to access to all course associated with that instructor.

#### Main point

```py

# accounts/views.py
@login_required
def instructor_dashboard_page(request):
    courses = Course.objects.filter(course_instructor=request.user.instructor)
    print(courses)
    context = {"courses":courses}
    return render(request, "accounts/instructor/instructor_dashboard.html", context)
```

`request.user`: this returns the `User` instance of current model.
`request.user.instructor`: django using the reverse relationship we have created, automatically assigns a `.instructor` attribute to the `User` model due to `OneToOneField(User)` in the `Instructor` model.

#### How they are connected

##### User to Instructor

- we log in as a user, and the logged-in user is associated with an instructor via the OneToOneField(User) in the Instructor model.

##### Instructor to Course

- Courses are linked to the Instructor model via the ForeignKey(course_instructor). Each course belongs to one instructor, but an instructor can have many courses.

#### Work flow

1. You log in as a user who is an instructor.
2. Django knows that this user has an associated Instructor profile due to the one-to-one relationship.
3. In the instructor_dashboard_page view, request.user.instructor fetches the logged-in user's Instructor profile.
4. You query all courses where the course_instructor is the current user's Instructor.
5. The courses are passed to the template and displayed on the instructor's dashboard.

We can use:

```py
@login_required
def instructor_dashboard_page(request):
    instructor = request.user.instructor
    courses = instructor.courses.all()
    return render(request, "accounts/instructor/instructor_dashboard.html", {"courses": courses})
```
