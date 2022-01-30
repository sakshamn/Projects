# Imports Begin #
from django.shortcuts import  render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
#from django.contrib.auth.hashers import make_password
# Imports End #

# Create your views here.
def homepage(request):
    if request.session.get("form_data") is None:
        return render (request=request, template_name="base.html")
    else:
        return render (request=request, template_name="base.html", context={"form_data": request.session["form_data"]})
# def homepage #


def signup_form(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # The password printed shows it to be encrypted. #
            #print(user.password)

            # Not required with crispy forms #
            #user = form.save(commit=False)
            #user.password = make_password(user.password)
            #user.save()

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

