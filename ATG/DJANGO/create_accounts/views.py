# Imports Begin #
from django.shortcuts import  render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
# Imports End #

# Create your views here.
def homepage(request):
    if request.session["form_data"]["category"] == "Doctor":
        return render (request=request, template_name="doctor.html", context={"form_data": request.session["form_data"]})
    elif request.session["form_data"]["category"] == "Patient":
        return render (request=request, template_name="patient.html", context={"form_data": request.session["form_data"]})
    else:
        return HttpResponse("You're not registered as either a Patient or Doctor! This is a System Issue Contact IT!")
# def homepage #


def signup_form(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            request.session["form_data"] = form.cleaned_data
            return redirect("create_accounts:homepage")
        else:
            messages.error(request, f"Unsuccessful registration. Invalid information.")
    return render (request=request, template_name="signup.html", context={"signup_form": form})
# def signup #


def login_form(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #category = form.cleaned_data.get('category')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                request.session["form_data"] = form.cleaned_data
                return redirect("create_accounts:homepage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    return render(request=request, template_name="login.html", context={"login_form":form})
# def login_form #


def logout_form(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("create_accounts:login")
# def logout_form #

