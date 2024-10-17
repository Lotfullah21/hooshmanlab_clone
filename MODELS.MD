```py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    email_token = models.EmailField()
    profile_picture = models.ImageField(upload_to="profile")
    otp = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    email_token = models.EmailField()
    profile_picture = models.ImageField(upload_to="profile")
    otp = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name


```

#### One-to-One

in a database design, it means that each record in one table is associated with exactly one record in another table.

##### Characteristics of One-to-One Relationships

`Uniqueness`: Each entry in the first table corresponds to a single entry in the second table. For instance, if we have a table for users and another for profiles, each user can have only one profile, and each profile can belong to only one user.

`Key Constraints`: In the context of a database, one table will have a foreign key that references the primary key of the other table. This foreign key is also unique, ensuring that each record in the second table corresponds to only one record in the first table.

`Use Cases`: Common use cases for one-to-one relationships include:

- Splitting a large table into smaller tables for better organization or performance.
- Extending the existing user model with additional fields (like profile information) without altering the original user table.
- Storing optional information that may not apply to every record in the primary table

- The Student and Instructor classes contain a OneToOneField that links to the User model.

- Each model now has a user field that establishes a relationship with the User model.

```sql

User Table               Student Table
-----------              ---------------
| User ID (PK) | <--- | User ID (FK) |
| Username     |      | Name          |
| Password     |      | Phone Number  |
| Email        |      | Profile Pic   |
-----------              ---------------

```

Pk: primary and FK: foreign key.

Here, the Student model has a OneToOneField linking it to the User model. Each Student is associated with exactly one User, and each User can be linked to only one Student.

`User Table`: Contains basic user information (username, password, email, first_name, last_name, is_active, is_superuser, date_joined).
`Student Table`: Contains additional information specific to students (name, phone number, profile picture, etc.).
`Instructor Table`: Contains additional information specific to instructors (name, phone number, profile picture, etc.).

`email`: The email field typically stores the user's email address for communication, notifications, and account management.
`email_token`: Purpose: The email_token field is used primarily for email verification and account confirmation purposes. It usually stores a temporary token sent to the user's email.

#### Crucial

Since, we are not having `phone_number` field default `User` model, we have to look in `Student` model for duplicate phone number.

```py
user_exists = User.objects.filter(Q(email=email) | Q(student__phone_number=phone_number)).exists()
```

`student__phone_number` refers to a related field between the User model and the Student model

foreign key in our Student model links to the User model, which creates a one-to-one or many-to-one relationship between Student and User.

`related_name='student'` allows us to access the Student model from the User model using `user.student.`.

### Reverse Lookup:

When we use `student__phone_number`, Django is performing a reverse lookup from the User model to the Student model.

`student__phone_number` means:

`student:` the reverse relation from User to Student. This comes from the `related_name='student'` specified in the Student model.
`phone_number:` the field inside the Student model we're interested in.
So, `student__phone_number` lets Django look for the `phone_number` in the related Student instance for each User.

`Q` objects are used to combine conditions with the logical `OR` (|) operator. This allows us to check both conditions in a single query.

```text
-templates
    - home
        -utils
            -navbar.html
            -base.html
        -index.html
```

We have to be careful when creating a user and save only the fields that comes with `User` model, for instance, `phone_number` is no included in User model, hence we cannot store it here.

```py
      # Create User with the base user model
        user = User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
```

### Sending Verification email to user.

```py
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'your_email_password'  # Replace with your email password

```

```py
from django.core.mail import send_mail

send_mail(
    "Subject here",
    "Here is the message.",
    "from@example.com",
    ["to@example.com"],
    fail_silently=False,
)
```

```py
#account/utils.py

def sendTokenEmail(email, token):
    subject = "Please verify your email"
    message = f""" please verify your email by clicking on this link
    http://127.0.0.1:8000/account/verify-account/{token}

    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
```

## How to send email to the user

error

```sh
SSLCertVerificationError at /account/register/

[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (\_ssl.c:1000)

```

#### 1. Install SSL Certificates (for macOS)

```sh
/Applications/Python\ 3.12/Install\ Certificates.command
```

#### 2. Verify Email Settings in Django

```py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP host
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

use a real email and set a password by going to `https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4ONDtnOZYfwfAq4KEmdrgJC1nxNpROSOfiviDcMDLK_-VnbjYqNQ7TUTdZw7tOgIWrcZTeD-0nJ1wupGUYulll5PxoC6ouS6e8ugxMFGysXXD_f32E`
and setting a password for the app, copy the generated password and paste it here.

You should be good to go after this.

for safety, store the credentials in `.env` file and use `dotenv` to access them

```py

# Sending emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER ")  # Replace with your email
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Replace with your email password
```

## Login

```py
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("user_email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
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
```

`authenticate`: `user = authenticate(request, username=email, password=password)`

We cannot use `filter` method to check for existence of a user, because we hashed the passwords when we stored them, hence we use `authenticate`, a built in function from django.
It returns a user object, if provided inputs matched in the database and `None` otherwise.
Note that by default, it takes the first argument as `username`, you cannot pass email or any other field unless you customized your `User` model.

`login(request, user)`: This function logs the authenticated user into the Django session.

When we call login, Django creates a session for the user and stores their user ID in the session data. This allows Django to keep track of the user's login status and other session-related information across requests.
After this call, the user is considered "logged in," meaning they can access views and resources that require authentication

```py
# If user is authenticated, log them in
login(request, user)
return redirect("home_view")
```

## Sending OTP

```JS
window.location.href = `/account/send_otp/${email}`;
```

using `/account`, it will make our path absolute and when we click, it will take us to `https://your-domain.com/account/send_otp/${email}`, but if we omit `/account`, it will take us to a relative path adding the current `ulr` before our path, hence it is crucial ot use `/` before account to make absolute.

```py
#login.html
<script>
function sendOTP(){
	const email =  document.getElementById("email").value
	if(email==""){
		alert("Email cannot be blanked")
	}
	alert(email)
	window.location.href=`/account/send_otp/${email}`
}
</script>
```

extremely crucial to use `window.location.href=/account/send_otp/${email}` and in urls also `path("send_otp/<email>/",send_otp, name="send_otp_view")`, the path should match, otherwise, the `send_top.view` will never gets rendered and otp will not be sent.

Here also, it is important to check if the user already in our database.

```py
#views.py
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
    send_token_email(email, otp)
    messages.success(request, "An OTP has been sent to your email")
    return redirect(f"/account/verify_otp/{email}")
```

in current project, authentications are done using base `User` model, hence, login using `login(request, student.user)`, not using `login(request, student)`

in Django, the `login()` function expects a User object, which typically comes from django.contrib.auth.models.User or a custom user model that extends it.

If our Student model is not our custom user model (i.e., it doesn't subclass AbstractBaseUser or AbstractUser), it won’t be compatible with the login() function because Django won’t recognize Student as a valid user.

```py
# views.py
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

```

## filter vs get

### 1. get()

```py
user = User.objects.get(email="example@example.com")
```

- If one and only one object matches the query, get() returns that object.
- If no object matches the query, it raises a DoesNotExist exception.
- If more than one object matches the query, it raises a MultipleObjectsReturned exception.

### 2. filter()

```py
users = User.objects.filter(email="example@example.com")

```

`Returns`: A queryset (which can contain zero, one, or many objects)

- If objects match the query, filter() returns a queryset containing all the matching objects.
- If no objects match, it returns an empty queryset (not an exception).

#### Use Case:

When you want to retrieve multiple objects or you're unsure if the query will return zero, one, or many results. You can chain methods like exists(), count(), or first() to handle different cases.

```table
| Method   | Returns                     | Behavior on No Result    | Behavior on Multiple Results     |
|----------|-----------------------------|--------------------------|----------------------------------|
| `get()`  | A single object              | Raises `DoesNotExist`     | Raises `MultipleObjectsReturned` |
| `filter()` | A queryset (can be empty)   | Returns an empty queryset | Returns all matching objects     |

```

#### Crucial:

When checking for existence of one object, use `filter` as it does not raise an exception.
