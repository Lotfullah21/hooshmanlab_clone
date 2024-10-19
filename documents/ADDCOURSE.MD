## uuid

UUID returns an object, if you want to do string operations, first convert it to a string.

```py
def generate_slug(instance):
    """
    Generate a unique slug for course names.
    If the slug already exists, call the function recursively to generate a new one.
    """
    # Generate a UUID and split it by hyphens, split method returns an array.
    parts = str(uuid.uuid4()).split("-")
    slug = slugify(instance) + "-" + parts[0]
    if Course.objects.filter(course_slug=slug).exists():
        # If slug exists, recursively call the function to generate a new one
        return generate_slug(instance)
    return slug

```

## required attribute in html

Using the required attribute in HTML helps with user experience by preventing submission when fields are empty. but, server-side validation is essential for security, data integrity, and ensuring that our application behaves correctly. Both client-side and server-side validations should work together to ensure a safe and smooth user experience.

for instance, if someone disable JS, still the form will be submitted with `required` attribute being off.
To ensure the data security, server side validation is also required.

```py
  # check if all fields are provided
if not (course_title and course_description and course_level and course_starting_date and course_ending_date and course_price):
    messages.error(request, "All fields are required.")
    return redirect("add_course_view")
```

## datetime.strptime

This method from the `datetime` module is used to parse a string representing a date (or time) into a datetime object based on a given format.

```py
datetime.strptime(date_string, format)
```

`'%Y-%m-%d'`: This is the format string that specifies how the date is structured.

- %Y: Represents a 4-digit year (e.g., 2024).
- %m: Represents a 2-digit month (e.g., 10 for October).
- %d: Represents a 2-digit day of the month (e.g., 17 for the 17th day).

### Example Workflow:

`String input`: Suppose the user submits the date 2024-10-17 as the course_ending_date.

`Conversion`: The datetime.strptime() function will take the string 2024-10-17 and interpret it based on the format '%Y-%m-%d'.

`Resulting object`: After conversion, you will get a datetime object like:

```py
datetime.datetime(2024, 10, 17, 0, 0)
```

This datetime object represents the date 2024-10-17 with the time portion set to midnight (00:00:00), which is the default for dates.

```py
#views.py
def add_course(request):
    if request.method=="POST":
        pass

        try:
            pass
            start_date = datetime.strptime(course_starting_date, '%Y-%m-%d')
            end_date = datetime.strptime(course_ending_date, '%Y-%m-%d')
            course_duration_in_weeks = (end_date-start_date).days//7
            if (course_duration_in_weeks).days<0:
                messages.error("end date must be after starting date")
                return redirect("add_course_view")
```
