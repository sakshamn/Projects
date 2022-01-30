# Import Begin #
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# Import End #

# Create your models here.
class SignUpForm(UserCreationForm):
    CHOICES = [('Male','Male'),('Female','Female')]

    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    profile_picture = forms.ImageField(required=False)
    email = forms.EmailField(required=True)
    address = forms.CharField()
    category = forms.CharField(label="User", widget=forms.RadioSelect(choices=CHOICES))

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "profile_picture",
            "username",
            "password1",    # Password #
            "password2",    # Confirmation Password #
            "email",
            "address",
            "category"
        )
    # class Meta #

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        user.email = self.cleaned_data["email"]
        user.address = self.cleaned_data["address"]
        user.category = self.cleaned_data["category"]

        if commit:
            user.save()

        return user
    # def save #
# class SignUpForm #


class LoginForm(AuthenticationForm):
    CHOICES = [('Male','Male'),('Female','Female')]
    category = forms.CharField(label="User", widget=forms.RadioSelect(choices=CHOICES))

