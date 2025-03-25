from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'vendor'

urlpatterns = [
    path('add/', add_item, name='add_item'),
    path('vendor_dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('vendor-reply/<int:inquiry_id>/', vendor_reply, name='vendor_reply'),
    path('vendor-inquiries/', vendor_inquiries, name='vendor_inquiries'),

]
