from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Inquiry
from catalog.models import *
from .forms import InquiryForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegistrationForm  # Import the form
from accounts.models import CustomUser

@login_required
def account_details(request):
    user = request.user  # Get logged-in user

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_details')  # Redirect to same page after update
    else:
        form = UserRegistrationForm(instance=user)

    return render(request, 'account_details.html', {'user': user, 'form': form})

@login_required
def submit_inquiry(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Ensure item exists
    
    if request.method == 'POST':
        message = request.POST.get('message')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')
        state = request.POST.get('state')
        country = request.POST.get('country')

        inquiry = Inquiry.objects.create(
            user=request.user,
            vendor=item.vendor,
            item=item,
            message=message,
            name=name,
            phone=phone,
            email=email,
            address=address,
            city=city,
            pin_code=pin_code,
            state=state,
            country=country,
        )

        # Send email to vendor
        send_mail(
            subject=f"New Inquiry for {item.name}",
            message=f"Dear {inquiry.vendor.username},\n\n"
                    f"You have a new inquiry about {item.name}.\n\n"
                    f"Name: {name}\nPhone: {phone}\nEmail: {email}\n"
                    f"Address: {address}, {city}, {state}, {country} - {pin_code}\n\n"
                    f"Message: {message}\n\n"
                    f"Please respond via the vendor dashboard.",
            from_email="noreply@yourdomain.com",
            recipient_list=[inquiry.vendor.email],
        )

        return redirect('user:my_inquiries')  # Redirects correctly

    # Instead of redirecting to 'home', render the form again
    return render(request, 'submit_inquiry.html', {'item': item})



@login_required
def my_inquiries(request):
    inquiries = Inquiry.objects.filter(user=request.user)
    return render(request, 'my_inquiries.html', {'inquiries': inquiries})

@login_required
def detailed_enquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, user=request.user)
    return render(request, 'detailed_enquiry.html', {'inquiry': inquiry})


