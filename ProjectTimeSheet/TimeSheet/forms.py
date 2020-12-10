from django import forms
from django.core import validators  ## For validation in forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


## Create your forms here

class SignUpForm(UserCreationForm):
    firstname = forms.CharField(max_length=30, required=False, help_text="Optional")
    lastname = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address")
    team = forms.CharField(max_length=30, required=True, help_text="Enter Employee's Team")
    employee_id = forms.IntegerField(required=True)
    employee_ctc = forms.IntegerField(required=True)
    privilege = forms.ChoiceField(label="Login As:", required=True, widget=forms.RadioSelect, choices=[("manager", "Manager"), ("employee", "Employee")])

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "email", "team", "employee_id", "employee_ctc", "privilege", "password1", "password2")


class TimeSheetForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, help_text="Enter Employee's Username")
    start_date = forms.DateField(widget=forms.SelectDateWidget(), required=True, help_text="Enter the Start Date of Project/Activity")
    end_date = forms.DateField(widget=forms.SelectDateWidget(), required=True, help_text="Enter the End Date of Project/Activity")
    project_or_activity = forms.CharField(max_length=30, required=True, help_text="Enter Project/Activity Name to be Assigned to the Employee")

    class Meta:
        model = User
        fields = ("username", "start_date", "end_date", "project_or_activity")


class EmployeeTimeSheetForm(forms.Form) :
    tasks = forms.CharField(widget=forms.Textarea, required=True, help_text="Tasks Completed for current Project")
    hours = forms.IntegerField(min_value=0, max_value=12, required=True, help_text="Hours Worked (max 12hrs)")
    comments = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":15}), required=False, help_text="Optional Comments")

    class Meta:
        model = User
        fields = ("tasks", "hours", "comments")


