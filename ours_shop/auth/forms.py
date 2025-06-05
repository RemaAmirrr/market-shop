from django import forms
from django.contrib.auth import get_user_model
from django.core import validators


class ContactusForm(forms.Form):

    fullname = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class" : "form-control"}))

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "place input you username"})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "form-control"}))   

user = get_user_model()
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control"}), validators=[ 
        validators.MaxLengthValidator(limit_value=20, message="نام کاربری نباید از ۲۰ کارکتر بیشتر باشد")
    ])
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control", "placeholder" : "place intpu you email"}), validators=[
        validators.EmailValidator("!ایمیل نامعتبر است")
    ])
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "form-control",}))
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput(attrs={"class" : "form-control"})) 
    
    def clean_username(self):
        userName = self.cleaned_data.get("username")
        query = user.objects.filter(username=userName)

        if query.exists():
            raise forms.ValidationError("این نام قبلا ثبت شده است")
        return userName
           
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qurey = user.objects.filter(email=email)
        if qurey.exists():
            raise forms.ValidationError("این ایمیل قبلا ثبت شده است")
        return email
    
    def clean(self):

        data = self.cleaned_data
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("پسوردها یکی نیستند")
        return data
