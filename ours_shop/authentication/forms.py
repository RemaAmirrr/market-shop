from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

user = get_user_model()

class ContactusForm(forms.Form):

    fullname = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class" : "form-control"}))

class LoginForm(forms.Form):
    phone = forms.CharField(
        label="شماره موبایل:",
        widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "لطفا شماره موبایلی که با ان ثبت نام کرده اید وارد کنید"})) 
    password = forms.CharField(
        label="پسورد:",
        widget=forms.PasswordInput(attrs={"class" : "form-control"}))   

    # def clean(self): 
    #     phone = self.cleaned_data.get("phone")
    #     passWord = self.cleaned_data.get("password")
    #     query = user.objects.filter(username=phone, password=passWord).first()
    #     print("=================================================",query)
    #     if query == None:
    #          raise forms.ValidationError("پسورد یا شماره اشتباه است")              
    #     return phone    

class Forget_Password(forms.Form):
    number_phone = forms.CharField(
        label="موبایل",
        widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "لطفا موبایل خود را وارد کنید"})) 
   
class RegisterForm(forms.Form):
    
    phone = forms.CharField(
        label="شمار موبایل ",
        widget=forms.NumberInput(attrs={"class" : "form-control", "placeholder" : "نام کاربری شما شماره موبایل شما میباشد وارد کنید"}), validators=[ 
        validators.MaxLengthValidator(limit_value=20, message="نام کاربری نباید از ۲۰ کارکتر بیشتر باشد")
    ])

    password = forms.CharField(
        label="پسورد ",
        widget=forms.PasswordInput(attrs={"class" : "form-control",}))
    
    password2 = forms.CharField(
        label="تایید پسورد",
        widget=forms.PasswordInput(attrs={"class" : "form-control"})) 
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        query = user.objects.filter(username=phone).all()

        if query.exists():
            raise forms.ValidationError("این شماره قبلا ثبت شده است")
        return phone
           
    def clean(self):
        data = self.cleaned_data
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("پسوردها یکی نیستند")
        return data
       
class UserUpdateForm(forms.ModelForm):

    image = forms.ImageField(
        label='',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        # validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    full_name = forms.CharField(
        label='نام کامل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'full_name'}),
        required=False,                                              
    )

    phone = forms.CharField(
        label='موبایل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
        required=False,                                              
    )

    email = forms.CharField(
        label='ایمیل',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}),
        required=False,                                              
    )

    address = forms.CharField(
        label='ادرس ',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
        required=False,                                              
    )

    city = forms.CharField(
        label='شهر',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}),
        required=False,                                              
    )

    state = forms.CharField(
        label='استان',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
        required=False,                                              
    )

    zipcode = forms.CharField(
        label='کدپستی',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),
        required=False,                                              
    )    
        
    class Meta:
        model = Profile
        fields = (
           'image', 'full_name', 'phone', 'email', 'address', 'city', 'state', 'zipcode', 
        )
        exclude = ['user', 'description']

class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(
        label="تلفن همراه",
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="شماره تلفن باید با 09 شروع شود و 11 رقم باشد"
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': '09123456789',
            'class': 'form-control'
        })
    )

class CodeVerificationForm(forms.Form):
    code = forms.CharField(
        label="کد تایید",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'کد ۶ رقمی',
            'class': 'form-control'
        })
    )

class PersianSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user set a new password without entering the old password
    with Persian translations and custom validation messages.
    """
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید را وارد کنید',
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        strip=False,
        help_text=_(
            "رمز عبور شما باید حداقل 8 کاراکتر داشته باشد و از اعداد و حروف تشکیل شده باشد."
        ),
    )
    
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید را تکرار کنید',
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.pop("autofocus", None)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمزهای عبور وارد شده یکسان نیستند")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user  

# accounts/forms.py


class PersianPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("رمز عبور فعلی"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور فعلی خود را وارد کنید',
            'autocomplete': 'current-password'
        }),
        error_messages={'required': 'لطفاً رمز عبور فعلی را وارد کنید'}
    )
    new_password1 = forms.CharField(
        label=_("رمز عبور جدید"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید خود را وارد کنید',
            'autocomplete': 'new-password',
            'id': 'newPass'
        }),
        error_messages={'required': 'لطفاً رمز عبور جدید را وارد کنید'}
    )
    new_password2 = forms.CharField(
        label=_("تکرار رمز عبور جدید"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید خود را تکرار کنید',
            'autocomplete': 'new-password'
        }),
        error_messages={'required': 'لطفاً تکرار رمز عبور جدید را وارد کنید'}
    )

