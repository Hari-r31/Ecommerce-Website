from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # ✅ Keep this

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_email_verified = models.BooleanField(default=False)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Correct reference
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password Reset Token for {self.user.username}"  # ✅ Use 'username' instead of 'email' if needed
