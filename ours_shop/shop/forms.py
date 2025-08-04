from django import forms

from .models import Rating
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')])
        }