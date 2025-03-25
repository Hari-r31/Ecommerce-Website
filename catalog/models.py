from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    specification = models.TextField()
    photos = models.ImageField(upload_to='item_photos/')
    videos = models.FileField(upload_to='item_videos/', null=True, blank=True)
    custom_fields = models.JSONField(null=True, blank=True)
    published = models.BooleanField(default=False)

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
