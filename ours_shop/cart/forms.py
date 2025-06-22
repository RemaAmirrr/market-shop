from django import forms
from .models import ShippingPayment 

class ShippingForm(forms.ModelForm):

    shipping_fullname = forms.CharField(
        label='  نام کامل  ',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'full_name'}),
        required=True,                                              
    )

    shipping_phone = forms.CharField(
        label='موبایل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
        required=True,                                              
    )

    shipping_email = forms.CharField(
        label='ایمیل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}),
        required=True,                                              
    )

    shipping_address1 = forms.CharField(
        label='ادرس اول',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}),
        required=True,                                              
    )

    shipping_address2 = forms.CharField(
        label='ادرس دوم',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'address2'}),
        required=False,                                              
    )

    shipping_city = forms.CharField(
        label='شهر',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}),
        required=True,                                              
    )

    shipping_state = forms.CharField(
        label='استان',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
        required=False,                                              
    )

    shipping_zipcode = forms.CharField(
        label='کد پستی',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),
        required=False,                                              
    ) 

    shipping_country = forms.CharField(
        label='کشور',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),
        required=True,                                              
    )   

    class Meta:
        model = ShippingPayment
        fields = (

            'shipping_fullname',
            'shipping_email',
            'shipping_phone',
            'shipping_address1',
            'shipping_address2',
            'shipping_city',
            'shipping_state',
            'shipping_zipcode',
            'shipping_country',
        ) 

        # exclude = ['user',]

class CouponForm(forms.Form):
    code = forms.CharField(
      widget=forms.TextInput(attrs={"class": "form-control", "id" : "input-coupon"}),
      label="کد تخفیف:"
    )        
        
     