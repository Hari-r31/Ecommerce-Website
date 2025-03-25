from django.contrib import admin
from django.contrib import messages
from catalog.models import Item

@admin.action(description="Approve selected items")
def approve_items(modeladmin, request, queryset):
    from django.utils.timezone import now
    count = queryset.update(published=True, approved=True)  # Update all selected items
    messages.success(request, f"{count} items approved successfully!")

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'published', 'approved', 'created_at', 'approved_at')
    list_filter = ('published', 'approved')
    search_fields = ('name', 'vendor__username')  # Allow searching by item name & vendor username
    actions = [approve_items]  # Add approval action

admin.site.register(Item, ItemAdmin)
