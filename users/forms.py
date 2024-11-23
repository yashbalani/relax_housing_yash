from django import forms
from .models import UserModel

class UserSignUpForm(forms.ModelForm):
    country = forms.IntegerField(required=True)
    state = forms.IntegerField(required=True)
    city = forms.IntegerField(required=True)
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email_address', 'date_of_birth', 'gender', 'passport','interests','phone_number','profile_picture','password']

    # Additional validation, if needed, can go here
