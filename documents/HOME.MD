### urls.py

```py
# home/urls.py
from django.urls import path
from .views import index
urlpatterns = [
    path("",index, name="home_view"),
]
```

### views.py

in views.py, get the courses and pass it to the template that is going to handle it.

```py
# home/views.py
from django.shortcuts import render
from accounts.models import Course
def index(request):
    courses = Course.objects.all()
    context = {"courses":courses}
    return render(request, "home/index.html", context=context)
```

```html
{% extends "home/utils/base.html" %} {% block content %}
<div class="max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
		{% for item in courses %}
		<div
			class="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
			{% with first_image=item.images.first %} {% if first_image %}
			<img
				class="w-full h-48 object-cover"
				src="{{ first_image.image.url }}"
				alt="{{ course.course_title }}" />
			{% else %}
			<img class="w-full h-48 object-cover" src="" alt="Default Image" />
			{% endif %} {% endwith %}
			<div class="p-6">
				<h2 class="font-bold text-xl text-gray-900 mb-2">
					{{ item.course_title }}
				</h2>
				<p class="text-gray-700 text-base mb-4">
					{{ item.course_description }}
				</p>
				<div class="text-sm text-gray-500 space-y-1">
					<p>Duration: {{ item.course_duration }}</p>
					<p>Level: {{ item.course_level }}</p>
					<p>
						Instructor: {{ item.course_instructor.first_name }}
						{{item.course_instructor.last_name }}
					</p>
				</div>
			</div>
		</div>
		{% endfor %}
	</div>
</div>
{% endblock %}
```

```py
{% for item in courses %}
		<div
			class="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
			{% with first_image=item.images.first %} {% if first_image %}
			<img
				class="w-full h-48 object-cover"
				src="{{ first_image.image.url }}"
				alt="{{ course.course_title }}" />
			{% else %}
			<img class="w-full h-48 object-cover" src="" alt="Default Image" />
			{% endif %} {% endwith %}

```

`with` in template create a temporarily variable to hold a value.

```py
class CourseImageField(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="course_images")
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

with the foreignKey relationship we have defined here, we can get access to all images related to a course object using `relate_name` attribute.
To get a single image, we use `course.images.first.image.url`, where images refer to all images related to a single course, `.first` refers to the first instance and `image` refers to the image field in `CourseImageField` and `url` refers to the path of the image which we have configured in `settings.py`.

### Search and filter

```py
from django.shortcuts import render
from accounts.models import Course

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
```

We create a form to grab the user's input.

```html
<form method="POST" class="flex flex-col sm:flex-row sm:items-center gap-4">
	{%csrf_token%}
	<input
		type="text"
		name="search_input"
		placeholder="Search for a course"
		class="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
	<select
		name="sort_by"
		class="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
		<option value="" disabled selected>Select sorting option</option>
		<option value="low_to_high">Low to High</option>
		<option value="high_to_low">High to Low</option>
	</select>
	<button
		type="submit"
		class="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600 transition duration-200">
		Submit
	</button>
</form>
```

`searched_sort = request.POST.get("sort_by")`, the value returned by .get will be the value we selection from `option` inside select options.
In input fields, we are directly adding the text field, but `select` field value is from `options`.
so define the value inside the `option` tags.
