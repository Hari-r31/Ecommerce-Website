from django import forms
from catalog.models import Item, Category

class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select an Existing Category"
    )
    new_category = forms.CharField(
        required=False,
        max_length=255
    )

    class Meta:
        model = Item
        fields = [
            'category', 'name', 'description', 
            'specification', 'photos', 'videos', 'custom_fields'
        ]

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        # Ensure either an existing category or a new one is provided
        if not category and not new_category:
            raise forms.ValidationError("You must select an existing category or enter a new one.")

        return cleaned_data

    def save(self, commit=True):
        """Handles saving a new category if provided."""
        item = super().save(commit=False)  # Don't save yet

        # Create new category if needed
        if not self.cleaned_data['category'] and self.cleaned_data['new_category']:
            category, created = Category.objects.get_or_create(name=self.cleaned_data['new_category'])
            item.category = category  # Assign to item

        if commit:
            item.save()

        return item
