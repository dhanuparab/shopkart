from django import forms
from .models import CustomUser


class CustomerSignUpForm(forms.ModelForm):
    image=forms.ImageField(required=False)
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name' ,'email', 'contact')
        