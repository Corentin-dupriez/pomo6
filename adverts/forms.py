from django import forms

from adverts.models import Advertisement

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    category = forms.ChoiceField(choices=[('', 'All categories')] +
                                         list(Advertisement.CategoryChoices.choices),
                                 required=False)


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title',
                  'description',
                  'category',
                  'image',
                  'is_fixed_price',
                  'fixed_price',
                  'min_price',
                  'max_price', ]