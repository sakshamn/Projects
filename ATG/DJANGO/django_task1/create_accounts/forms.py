# Import Begin #
from django import forms
from models import UserSignUp
# Import End #

# Create your models here.
class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserSignUp
        fields = (
            "first_name",
            "last_name",
            #"profile_picture",
            "username",
            "password",
            "email",
            "address"
        )

