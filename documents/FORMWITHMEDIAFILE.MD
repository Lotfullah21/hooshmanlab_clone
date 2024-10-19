## Submitting media files in form data

While submitting and handling form data, two major points to remember.

- for forms, apart from `method` attribute, `enctype="multipart/form-data"` also should be added.
- `request.POST` can be used only with form data, to get the files, we use `request.FILES`.

```html
<form method="POST" enctype="multipart/form-data">
	{%csrf_token%}
	<label for="file_upload"> <span>Upload a file</span> </label>
	<input id="file-upload" name="file_upload" type="file" class="sr-only" />
	<button type="submit"></button>
</form>
```

```py
# view.py
def upload_image_page(request, course_slug):
    course = Course.objects.get(course_slug=course_slug)
    if request.method=="POST":
        file = request.FILES.get("file_upload")
        if file:
            CourseImageField.objects.create(
                course=course,
                image=file
            )
            messages.success(request, "Image uploaded successfully")
            return redirect("instructor_dashboard_view")
        else:
            messages.error(request, "No file is uploaded")
    images = course.images.all()
    return render(request, "accounts/instructor/upload_image.html",context={"images":images})
```

It will always returns a query set.

```py
images = course.images.all()
```

```html
{% extends "../utils/base.html"%} {%block content%}

<div>{%include "../utils/navbar.html"%}</div>

<div class="grid item-center justify-center">
	<div class="w-full sm:max-w-sm p-8 flex justify-center items-center">
		<form method="POST" enctype="multipart/form-data">
			{%csrf_token%}
			<!-- <label for="file_upload">upload file</label> -->
			<input type="file" name="file_upload" id="file_upload" />
			<button type="submit" class="mt-4 p-1 bg-green-400 rounded text-md">
				submit
			</button>
		</form>
	</div>
	<div class="grid grid-cols-3 items-center justify-center gap-2">
		{% for item in images%}
		<img
			src="{{item.image.url}}"
			alt="course image"
			class="h-48 w-full object-cover" />
		{%endfor%}
	</div>
</div>
{%endblock%}
```

each item represents one instance returned from images and we are looking for image field which stores our file `image = models.ImageField(upload_to="course_images")` and `url` is the location where the files are saved.

```html
{% for item in images%}
<img
	src="{{item.image.url}}"
	alt="course image"
	class="h-48 w-full object-cover" />
{%endfor%}
```

`item.image.url` :

- Retrieves the file path stored in the image field `course_images`
- Converts that file path into a full URL based on your MEDIA_URL setting
- Provides the public URL where the image can be accessed.

### Example Flow:

- we have a CourseImageField instance (let's say x).
- x.image contains the uploaded image file, for example, python_course_image.jpg.
- x.image.url will return the full URL for that image, like http://yourdomain.com/media/course_images/python_course_image.jpg.
