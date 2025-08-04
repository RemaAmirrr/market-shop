from django import forms
from .models import FinalModel
from django.core import validators

class CouponForm(forms.Form):
    code = forms.CharField(
      widget=forms.TextInput(attrs={"class": "form-control", "id" : "input-coupon"}),
      label="کد تخفیف:"
    )

class InputForm(forms.Form):
    qty = forms.CharField(
      widget=forms.TextInput(attrs={"class": "form-control", "id" : "input-coupon"}),
      label="تعداد"
    )    

CHOISE_WAY = [     
    ('1', 'تی باکس'),
    ('2', 'پست'),
    ('3', 'چاپار'),
    ('4', 'باربری'),
]

CHOISE_PIMENT = [     
    ('1', ' درگاه بانک ملت'),
    ('2', 'درگاه زرین پال'),
    ('3', 'درگاه بانک پاسارگاد'),
    ('4', 'هنگام دریافت'),
]

STATUS = [     
    ('1', 'ثبت نام حساب کاربری'),
    ('2', 'تسویه حساب مهمان'),
    ('3', 'مشتری قبلی'),
]

class FinalForm(forms.ModelForm):
      
    full_name = forms.CharField(
        label='نام کامل',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'full_name'}),
                                                    
    )

    phone = forms.CharField(
        label='موبایل',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
                                                    
    )

    # email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control", "placeholder" : "place intpu you email"}),
    # required=False, 
    # validators=[
    #     validators.EmailValidator("!ایمیل نامعتبر است"),   
    # ])


    city = forms.CharField(
        label='شهر',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}),
                                                     
    )

    state = forms.CharField(
        label='استان',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
                                                   
    )

    zip_code = forms.CharField(
        label='کدپستی',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip_code'}),
                                                    
    ) 

    
    address = forms.CharField(
        label='ادرس ',
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'address'}),
                                                   
    )

    pay_way = forms.ChoiceField(
      label="شیوه ارسال",
      choices=CHOISE_WAY,
      widget=forms.RadioSelect ) 
    
    payed_way = forms.ChoiceField(
          label="شیوه پرداخت",
          choices=CHOISE_PIMENT,
          widget=forms.RadioSelect )   
    
    description = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':''}),
        required=False,) 

    order_id = forms.CharField(widget=forms.HiddenInput(), required=False) 
    user = forms.CharField(widget=forms.HiddenInput(), required=False)   

    class Meta:
      model = FinalModel
      fields = [
          'full_name', 'phone', 'address', 'city', 'state',
          'zip_code', 'pay_way', 'payed_way', 'description','user', 'order_id'
        ]
 


        
   