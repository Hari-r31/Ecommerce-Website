from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
     path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation_sent/', views.activation_sent, name='activation_sent'),

    path('login_register/', views.login_register, name='login_register'),
    path("user_logout/", views.user_logout, name="logout"),

    path("password_reset/", views.password_reset_request, name="password_reset_request"),
    path("reset/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),

]
