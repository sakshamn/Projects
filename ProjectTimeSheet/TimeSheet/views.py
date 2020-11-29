from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
## We need to set xframe_options_sameorigin decorator to prevent clickjacking.
## Clickjacking prevents loading of iframe sources by default for security.
from django.views.decorators.clickjacking import xframe_options_sameorigin
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

#from TimeSheet.forms import Login, CreateProfile
from TimeSheet.models import Credentials#, EmployeeProfile


## Create your views here.

def redirect_parameters(base_url, parameter) :
    """Use redirect with parameters to be passed to the page you are redirecting to."""
    url = "/{}/?{}".format(base_url, parameter)
    return url


#@login_required
def home(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    record = Credentials.objects.filter(username=username)

    if (user := authenticate(username=username, password=password)) is None :
        msg = "Invalid Credentials! Try Again or Contact IT Support!"
        return render(request, "registration/login.html", {"login_msg" : msg})
    else :
        login(request, user)

    privilege = record[0].privilege
    if privilege == "manager" :
        return redirect("/manager/")
    else :
        return redirect("/employee/")


@csrf_exempt
def manager(request) :
    """Manager main page when a manager logins.

    Send html page to be shown according to the buttons clicked in the manager.html
    """
    if (iframe_src := request.POST.get("iframe_src")) is None : ## Default
        iframe_src = "dashboard.html"

    return render(request, "manager.html", {"iframe_src" : iframe_src})


## We use the decorator to tell that this source view is safe to load in an iframe.
@xframe_options_sameorigin
@csrf_exempt
def teams(request) :
    """Send html page to be shown according to the buttons clicked in the teams.html"""
    if (html_page := request.POST.get("html_page")) is None :   ## Default
        html_page = "members.html"
        params_dict = {"teams" : ["Digital", "Analog", "Mixed Signal"]}
    elif (html_page := request.POST.get("html_page")) == "members" :
        html_page = "members.html"
        params_dict = {"teams" : ["Digital", "Analog", "Mixed Signal"]}

    return render(request, html_page, params_dict)


def employee(request) :
    """Employee main page when a employee logins."""
    return render(request, "employee.html")


@xframe_options_sameorigin
def dashboard(request) :
    """We need to set xframe_options_sameorigin decorator to prevent clickjacking.

    Clickjacking prevents loading of iframe sources by default for security.
    We use the decorator to tell that this source view is safe to load in an iframe.
    """
    return render(request, "dashboard.html")


@xframe_options_sameorigin
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            privilege = form.cleaned_data.get('privilege')
            user = authenticate(username=username, password=password)
            login(request, user)

            obj = Credentials(username = username, password = password, privilege = privilege)
            ## Save the data
            obj.save()

            return redirect('teams')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


