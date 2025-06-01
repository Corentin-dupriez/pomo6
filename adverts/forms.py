from django import forms

from adverts.models import Advertisement


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'category']