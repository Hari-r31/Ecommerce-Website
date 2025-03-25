from django.shortcuts import render, redirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from .forms import UserRegistrationForm
from .models import CustomUser 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm
from .forms import PasswordResetRequestForm
from .models import PasswordResetToken
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import PasswordResetToken
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator

User = get_user_model() 

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email is confirmed
            user.save()
            # Build activation email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            send_mail(subject, message, 'noreply@example.com', [user.email])
            return redirect('accounts:activation_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# User Activation View
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser .objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser .DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        login(request, user)
        return HttpResponse('Sucefucelly Activated u can close this page')  # Redirect to a success page
    else:
        return render(request, 'registration/activation_invalid.html')
    
def activation_sent(request):
    return render(request, 'registration/activation_sent.html')

def login_register(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'user':
                login(request, user)
                return redirect("home")  # Redirect to home page after login  
            elif user is not None and user.role == 'vendor':
                login(request, user)
                return redirect("vendor:vendor_dashboard")  # Redirect to home page after login 
        else:
                messages.error(request, "Invalid username or password.")

    else:
        form = UserLoginForm()

    return render(request, "registration/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("home")

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.get(email=email)

            # Generate token
            token = get_random_string(50)
            PasswordResetToken.objects.create(user=user, token=token)

            # Encode user ID
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # ✅ Ensure reverse() matches urls.py
            reset_link = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
            )

            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password:\n{reset_link}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect("accounts:login_register")

    else:
        form = PasswordResetRequestForm()

    return render(request, "reset_password/password_reset_form.html", {"form": form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(f"Decoded UID: {uid}")  # 🔍 Debugging step
        user = User.objects.get(pk=uid)
        print(f"User found: {user.username}")  # 🔍 Debugging step
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("Invalid UID")  # 🔍 Debugging step
        user = None

    if user is None:
        return render(request, "reset_password/password_reset_confirm.html", {"valid": False})

    # Check if token matches the stored token
    reset_token = PasswordResetToken.objects.filter(user=user, token=token).first()
    if reset_token is None:
        print("Invalid token")  # 🔍 Debugging step
        return render(request, "reset_password/password_reset_confirm.html", {"valid": False})

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "reset_password/password_reset_confirm.html", {"valid": True, "error": "Passwords do not match!"})

        user.password = make_password(password)
        user.save()
        reset_token.delete()  # Remove the used token
        return redirect("accounts:login_register")  # Redirect to login page after resetting password

    return render(request, "reset_password/password_reset_confirm.html", {"valid": True})
