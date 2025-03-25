from django.contrib import admin
from django.utils.timezone import now
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  # Show Parent-Child Relationship
    search_fields = ('name',)
    list_filter = ('parent',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vendor', 'published', 'approved', 'created_at', 'approved_at')
    list_filter = ('category', 'published', 'approved')
    search_fields = ('name', 'vendor__username')
    actions = ['approve_items']

    def approve_items(self, request, queryset):
        """Mark selected items as approved & published."""
        queryset.update(approved=True, published=True, approved_at=now())
        self.message_user(request, "Selected items have been approved and published.")
    
    approve_items.short_description = "Approve and publish selected items"

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'added_at')
    search_fields = ('user__username', 'item__name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)

