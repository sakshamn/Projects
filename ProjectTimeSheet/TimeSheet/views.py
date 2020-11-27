from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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
    privilege = record[0].privilege

    if privilege == "manager" :
        return redirect("/manager/")
    else :
        return redirect("/employee/")


#@login_required
def manager(request) :
    """Manager main page when a manager logins."""
    frame_src = request.GET.get("iframe_src")
    return render(request, "manager.html", {"iframe_src" : frame_src})


@csrf_exempt
def manager_actions(request) :
    """Manager main page when a manager logins."""
    if request.POST.get("dashboard") :
        iframe_src = "dashboard.html"
    elif request.POST.get("reports") :
        iframe_src = "reports.html"
    elif request.POST.get("projects") :
        iframe_src = "projects.html"
    elif request.POST.get("teams") :
        iframe_src = "teams.html"
    elif request.POST.get("clients") :
        iframe_src = "clients.html"
    elif request.POST.get("settings") :
        iframe_src = "settings.html"

    parameter = urlencode({"iframe_src" : iframe_src})
    return redirect(redirect_parameters("manager", parameter))


#@login_required
def employee(request) :
    """Employee main page when a employee logins."""
    return render(request, "employee.html")


def employee_actions(request) :
    """Employee main page when a employee logins."""
    pass


def dashboard(request) :
    return render(request, "dashboard.html")


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

            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


