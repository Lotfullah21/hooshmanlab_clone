## home template

Wrap the entire course card in `anchor tag <a>` and pass `single_course_view` and `course.course_slug` as a parameter.

```html
	<div class="grid gap-6 ">
		{% for item in courses %}
		<a href="{%url 'single_course_view' item.course_slug%}">
            <!-- rest of the code -->
			<div></a
		>
		{% endfor %}
	</div>
```

Define a pattern with given `slug` as a parameter.

```py
#home/urls.py
from django.urls import path
from .views import index, single_course_page

urlpatterns = [
    path("",index, name="home_view"),
    path("/<slug>",single_course_page, name="single_course_view"),
]

```

### views

Create a view function, note that don't use `course = Course.objects.filter(course_slug=slug)` alone as it returns a collection of object.

either use .first method or get or get_object_or_404.

```py
def single_course_page(request, slug):
    course = get_object_or_404(Course, course_slug=slug)
    course = Course.objects.filter(course_slug=slug)
    course = Course.objects.get(course_slug=slug)
    course = Course.objects.filter(course_slug=slug).first()
    return render(request, "home/single_course.html", context={"course":course})
```

```py
#### Finalized code
def single_course_page(request, slug):
    course = get_object_or_404(Course, course_slug=slug)
    return render(request, "home/single_course.html", context={"course":course})
```

### template

Create a single course html

```html
<!-- home/single_course.html -->
{% extends "home/utils/base.html" %} {% block content %}
<div class="max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
		<div
			class="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
			{% with first_image=course.images.first %} {% if first_image %}
			<img
				class="w-full h-48 object-cover"
				src="{{ first_image.image.url }}"
				alt="{{ course.course_title }}" />
			{% else %}
			<img class="w-full h-48 object-cover" src="" alt="Default Image" />
			{% endif %} {% endwith %}
			<div class="p-6">
				<h2 class="font-bold text-xl text-gray-900 mb-2">
					{{ course.course_title }}
				</h2>
				<p class="text-gray-700 text-base mb-4">
					{{ course.course_description }}
				</p>
				<div class="text-sm text-gray-500 space-y-1">
					<p>Duration: {{ course.course_duration }}</p>
					<p>Level: {{ course.course_level }}</p>
					<p>Price: {{ course.course_price }}</p>
					<p>
						Instructor: {{ course.course_instructor.first_name }}
						{{course.course_instructor.last_name }}
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
{% endblock %}
```
