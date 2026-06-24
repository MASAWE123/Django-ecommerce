from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from .models import Profile

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1','new_password2']
    
    def __init__(self,*args,**kwargs):
        super(ChangePasswordForm,self).__init__(*args,**kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['new_password1'].label = 'Password 1'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = 'Password 2'

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),required=False)
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'address1'}),required=False)
    address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'address2'}),required=False)
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'city'}),required=False)
    state =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'state'}),required=False)
    zipcode =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'zipcode'}),required=False)
    country =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'country'}),required=False)     

    class Meta:
        model = Profile
        fields = ['phone','address1','address2','city','state','zipcode','country']


class UpdateUserForm(UserChangeForm):
    password = None
    email =forms.EmailField(max_length=100,)
    first_name =forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def __init__(self,*args,**kwargs):
        super(UpdateUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your fist name:'
        self.fields['first_name'].label = ''


        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name:'
        self.fields['last_name'].label = ''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your emial:'
        self.fields['email'].label = ''



class SignUpForm(UserCreationForm):
    email =forms.EmailField(max_length=100,)
    first_name =forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your fist name:'
        self.fields['first_name'].label = ''


        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name:'
        self.fields['last_name'].label = ''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your emial:'
        self.fields['email'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password:'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        self.fields['password2'].label = ''


        
