from django import forms
from django.core import validators  ## For validation in forms

## Create your forms here

#class Login(forms.Form) :
#    username = forms.IntegerField(label="Enter Username:")
#    password = forms.CharField(label="Enter Password:", help_text="Min. 6 characters", widget=forms.PasswordInput, validators=[validators.MinLengthValidator(6)])   ## Password should be of 6 chars using a validator.
#    privilege = forms.ChoiceField(label="Login As:", widget=forms.RadioSelect, choices=[("manager", "Manager"), ("employee", "Employee")])
#
#
#class CreateProfile(forms.Form) :
#    username = forms.IntegerField(label="Enter Username:")
#    name = forms.CharField(label="Enter Employee's Name:", max_length=30)
#    password = forms.CharField(initial="login123", max_length=10)
#    email = forms.EmailField(label="Enter Employee's Email:", max_length=30)
#    team = forms.CharField(label="Enter Employee's Team:", max_length=30)
#    project = forms.CharField(label="Enter Employee's Assigned Projects:")
#    privilege = forms.ChoiceField(label="Login As:", widget=forms.RadioSelect, choices=[("manager", "Manager"), ("employee", "Employee")])


