from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from .models import Profile
# from django.core.validators import FileExtensionValidator
from .models import Account
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm



class ContactusForm(forms.Form):

    fullname = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class" : "form-control"}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "place input you username"})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "form-control"}))   

    def clean_username(self):
        userName = self.cleaned_data.get("username")
        passWord = self.cleaned_data.get("password")
        query = user.objects.filter(username=userName, password=passWord).all()

        if query.exists():
             raise forms.ValidationError("پسورد یا نام کاربری اشتباه است")              
        return userName    

    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "place input you username"})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class" : "form-control"}))   

    def clean_username(self):
        userName = self.cleaned_data.get("username")
        passWord = self.cleaned_data.get("password")
        query = user.objects.filter(username=userName, password=passWord).all()

        if query.exists():
             raise forms.ValidationError("پسورد یا نام کاربری اشتباه است")              
        return userName


class Forget_Password(forms.Form):
    number_phone = forms.CharField(
        label="موبایل",
        widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "لطفا موبایل خود را وارد کنید"})) 
   

user = get_user_model()
class RegisterForm(forms.Form):
    
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={"class" : "form-control", "placeholder" : "نام کاربری را وارد کنید"}), validators=[ 
        validators.MaxLengthValidator(limit_value=20, message="نام کاربری نباید از ۲۰ کارکتر بیشتر باشد")
    ])
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={"class" : "form-control", "placeholder" : "ایمیل خود را وارد کنید"}), validators=[
        validators.EmailValidator("!ایمیل نامعتبر است")
    ])
    password = forms.CharField(
        label="پسورد ",
        widget=forms.PasswordInput(attrs={"class" : "form-control",}))
    
    password2 = forms.CharField(
        label="تایید پسورد",
        widget=forms.PasswordInput(attrs={"class" : "form-control"})) 
    
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
    
    
class UserUpdateForm(forms.ModelForm):
    
    # widgets = {
    #         'image': forms.FileInput(attrs={'class': 'form-control'}),
    #     }

    image = forms.ImageField(
        label='',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        # validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    
    # image = forms.ImageField(label='Upload Image')

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

# from .models import Account
# from django.contrib.auth import authenticate
# from django.contrib.auth.forms import UserCreationForm


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='email', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login!")


class RegistrationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


class AccountUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account