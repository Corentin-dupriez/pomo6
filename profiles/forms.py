from django import forms

from profiles.models import UserProfile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'image': forms.FileInput()
        }