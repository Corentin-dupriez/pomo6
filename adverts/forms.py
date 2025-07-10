from django import forms

from adverts.models import Advertisement, RatingResponse


class SearchForm(forms.Form):
    query = forms.CharField(required=False,
                            label='Search for')

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
        labels = {'title': 'Title',
                  'description': 'Description',
                  'category': 'Category',
                  'image': 'Image',
                  'is_fixed_price': 'Fixed Price',
                  'fixed_price': 'Price',
                  'min_price': 'Min Price',
                  'max_price': 'Max Price',}
        widgets = {
            'title': forms.TextInput(attrs={'id': 'id-title'}),
            'description': forms.Textarea(),
            'category': forms.Select(attrs={'id': 'id-category'}),
            'image': forms.FileInput(),
            'is_fixed_price': forms.CheckboxInput(attrs={'id': 'fixed-price'}),
            'fixed_price': forms.NumberInput(attrs={'id': 'fixed-price-field'}),
            'min_price': forms.NumberInput(attrs={'id': 'range-price-field'}),
            'max_price': forms.NumberInput(attrs={'id': 'range-price-field'}),
        }

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop('user', None)
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True) -> Advertisement:
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj


class RatingResponseForm(forms.ModelForm):
    to_rating_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = RatingResponse
        fields = ['comment']
        labels = {'comment': ''}
