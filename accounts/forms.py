from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        error_messages={'required': 'Password is required.'}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        error_messages={'required': 'Please confirm your password.'}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        help_texts = {
            "username": None,  # Removes "150 characters or fewer..."
            "password1": None,  # Removes default Django password rules
            "password2": None,  # Removes "Enter the same password..."
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email.")
        return email