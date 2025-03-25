from django.urls import path
from .views import *

app_name='user'

urlpatterns = [
    path('submit-inquiry/<int:item_id>/', submit_inquiry, name='submit_inquiry'),
    path('my-inquiries/', my_inquiries, name='my_inquiries'),
    path('account_details/', account_details, name='account_details'),
    path('detailed-enquiry/<int:inquiry_id>/', detailed_enquiry, name='detailed_Enquiry'),
    
    # path('cart/', view_cart, name='view_cart'),
]
