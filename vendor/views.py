from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Item
from .forms import ItemForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from user.models import Inquiry
from catalog.models import Item 
from user.forms import InquiryForm
from django.urls import reverse

@login_required
def add_item(request):
    if request.user.role != 'vendor':  # Ensure only vendors can add items
        messages.error(request, "Only vendors can submit items.")
        return redirect('home')

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.vendor = request.user  # Assign vendor
            item.published = False  # Requires admin approval
            item.save()
            messages.success(request, "Item submitted for approval.")
            return redirect('vendor:vendor_dashboard')

    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})


def vendor_dashboard(request):
    return render(request, 'vendor_dashboard.html')

@login_required
def vendor_reply(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, vendor=request.user)
    
    if request.method == "POST":
        response = request.POST.get('response')
        inquiry.response = response
        inquiry.save()

        # Send email to the user
        send_mail(
            'Vendor Response to Your Inquiry',
            f'The vendor has responded: {response}',
            'yourshop@example.com',
            [inquiry.user.email],
            fail_silently=False,
        )

        return redirect(reverse('vendor:vendor_inquiries'))


    return render(request, 'vendor_reply.html', {'inquiry': inquiry})


@login_required
def vendor_inquiries(request):
    inquiries = Inquiry.objects.filter(vendor=request.user)
    return render(request, 'vendor_inquiries.html', {'inquiries': inquiries})