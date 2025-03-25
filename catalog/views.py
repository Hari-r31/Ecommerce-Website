from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Category, Item  # Import only necessary models

def catalog(request):
    categories = Category.objects.prefetch_related("subcategories").all()
    return render(request, "catalog/home_view.html", {"categories": categories})

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)
    items = Item.objects.filter(category=subcategory, published=True, approved=True)  # Fetch only approved & published items
    return render(request, "catalog/subcategory_detail.html", {"subcategory": subcategory, "items": items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id, published=True)
    return render(request, 'catalog/Item_Details.html', {'item': item})
