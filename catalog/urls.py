from django.urls import path
from .views import catalog, subcategory_detail, item_detail  # Explicit imports

app_name = 'catalog'

urlpatterns = [
    path("", catalog, name="catalog"),
    path("subcategory/<int:subcategory_id>/", subcategory_detail, name="subcategory_detail"),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
]
