from django import forms

from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')])
        }

class Comment_Form(forms.Form):
    name = forms.CharField(
        label='نام شما',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
           
        })
    )
    description = forms.CharField(
        label='نظر شما',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
        })
    )
        