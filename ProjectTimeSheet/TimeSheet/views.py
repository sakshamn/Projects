from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode

## We need to set xframe_options_sameorigin decorator to prevent clickjacking.
## Clickjacking prevents loading of iframe sources by default for security.
## We use the below decorator to tell that this source view is safe to load in an iframe.
from django.views.decorators.clickjacking import xframe_options_sameorigin

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

#from TimeSheet.forms import Login, CreateProfile
from TimeSheet.models import CredentialsModel, TeamModel, TimeSheetModel
from TimeSheet.forms import SignUpForm, TimeSheetForm, EmployeeTimeSheetForm

from datetime import date 

## User Global Constants
TODAY = date.today().strftime("%d/%m/%Y")

## Dicts that shall initialise dicts inside function for the first time.
TEAM_DETAILS = dict(
    team_id         = "",   ## Auto Increment
    team_name       = "",
    team_lead       = "",
    members         = [],
    team_cost       = "",
    team_projects   = ""
)

PROJECT_DETAILS = dict(
    project_id          = "",   ## Auto Increment
    project_name        = "",
    project_lead        = "",
    client              = "",
    teams               = [],
    project_cost        = "",
    completion_percent  = "",
    deadline            = ""
)

## Create your views here.

def redirect_parameters(base_url, parameter) :
    """Use redirect with parameters to be passed to the page you are redirecting to."""
    url = "/{}/?{}".format(base_url, parameter)
    return url


#@login_required
def home(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    record = CredentialsModel.objects.filter(username=username)

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
@login_required
def manager(request) :
    """Manager main page when a manager logins.

    Send html page to be shown according to the buttons clicked in the manager.html
    """
    if (iframe_src := request.POST.get("iframe_src")) is None : ## Default
        iframe_src = "dashboard.html"

    return render(request, "manager/manager.html", {"iframe_src" : iframe_src})


## We use the decorator to tell that this source view is safe to load in an iframe.
@xframe_options_sameorigin
@csrf_exempt
def teams(request) :
    """Send html page to be shown according to the buttons clicked in the teams.html"""
    if (html_page := request.POST.get("html_page")) is None :   ## Default
        html_page = "manager/members.html"
        params_dict = {"teams" : ["Digital", "Analog", "Mixed Signal"]}
    elif (html_page := request.POST.get("html_page")) == "members" :
        html_page = "manager/members.html"
        params_dict = {"teams" : ["Digital", "Analog", "Mixed Signal"]}

    return render(request, html_page, params_dict)


@login_required
@csrf_exempt
def employee(request) :
    """Employee main page when a employee logins."""

    if (timesheet_date := request.POST.get("mydate")) is None :
        timesheet_date = TODAY
    print(timesheet_date)

    if (data := request.POST.get("data")) is None :
        data = ""

    if (edit_btn := request.POST.get("edit_btn")) is None :
        edit_btn = ""

    if (delete_btn := request.POST.get("delete_btn")) is None :
        delete_btn = ""

    print("data", data)
    print("edit_btn", edit_btn)
    print("delete_btn", delete_btn)

    employee_id = 1
    project = ""

    employee_timesheet_dict = employee_timesheet(request, employee_id, project, timesheet_date)

    timesheet_record = TimeSheetModel.objects.all()
    username = request.POST.get("username")
    employee_timesheet_dict["projects"] = []
    if len(timesheet_record) > 0 :
        for record in timesheet_record :
            pass
            #if record.timesheet["timesheet_date"] == timesheet_date and record.timesheet["username"] == request.POST.get("username") :
            #if record.timesheet["timesheet_date"] == timesheet_date :
                ## Append all projects for the particular date & employee id
                #employee_timesheet_dict["projects"].append(record.timesheet["project"])

    return render(request, "employee/employee.html", employee_timesheet_dict)


@xframe_options_sameorigin
def dashboard(request) :
    """
    """
    return render(request, "manager/dashboard.html")


@xframe_options_sameorigin
def timesheets(request) :
    """
    """
    return render(request, "manager/timesheets.html")


@xframe_options_sameorigin
@csrf_exempt
def signup(request):
    msg = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")   ## password1 is password entered. password2 is confirmation password.
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            email = form.cleaned_data.get("email")
            team = form.cleaned_data.get("team")
            employee_id = form.cleaned_data.get("employee_id")
            employee_ctc = form.cleaned_data.get("employee_ctc")
            privilege = form.cleaned_data.get("privilege")

            user = authenticate(username=username, password=password)
            login(request, user)

            obj = CredentialsModel(username = username, password = password, firstname = firstname, lastname = lastname, email = email, team = team, employee_id = employee_id, employee_ctc = employee_ctc, privilege = privilege)
            obj.save()  ## Save the data

            update_teams()

            msg = "Signup Done Successfully!"
        else :
            msg = "Please Correct The Errors Below:"
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"msg" : msg, "form": form})


@xframe_options_sameorigin
@csrf_exempt
def timesheet(request):
    msg = ""
    if request.method == 'POST':
        form = TimeSheetForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get("employee_id")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            project = form.cleaned_data.get("project")

            update_timesheet("manager", employee_id, start_date, end_date, project, tasks="", hours=0, comments="", timesheet_date="")

            msg = "Employee TimeSheet Created Successfully!"
        else :
            msg = "Please Correct The Errors Below:"
    else:
        form = TimeSheetForm()

    return render(request, "manager/timesheet.html", {"msg" : msg, "form": form})


def employee_timesheet(request, employee_id, project, timesheet_date):
    msg = ""
    if request.method == 'POST':
        form = EmployeeTimeSheetForm(request.POST)
        if form.is_valid():
            tasks = form.cleaned_data.get("tasks")
            hours = form.cleaned_data.get("hours")
            comments = form.cleaned_data.get("comments")

            update_timesheet("employee", employee_id, project, tasks, hours, comments, timesheet_date, start_date="", end_date="")

            msg = "Employee TimeSheet Created Successfully!"
        else :
            msg = "Please Correct The Errors Below:"
    else:
        form = EmployeeTimeSheetForm()

    return {"msg" : msg, "form": form}


def update_timesheet(privilege, employee_id, start_date, end_date, project, tasks, hours, comments, timesheet_date) :
    """Add, update & delete timesheet details using JSONField data.
    """

    if privilege == "manager" :
        TimeSheetModel.objects.create(
            timesheet = dict(
                employee_id = employee_id,
                start_date = str(start_date),
                end_date = str(end_date),
                project = project
            )
        )
    elif privilege == "employee" :
        timesheet_record = TimeSheetModel.objects.all()
        for timesheet in timesheet_record :
            if timesheet["employee_id"] == employee_id and timesheet["project"] == project :
                timesheet["tasks"] = tasks
                timesheet["hours"] = hours
                timesheet["comments"] = comments
                timesheet["timesheet_date"] = timesheet_date


def update_teams() :
    """Add, update & delete teams details.

    JSONField data.

    Example:
    TeamModel.objects.create(data={
    'name': 'John',
    'cities': ['London', 'Cambridge'],
    'pets': {'dogs': ['Rufus', 'Meg']},
    })

    TeamModel.objects.filter(
    data__name='John',
    data__pets__has_key='dogs',
    data__cities__contains='London',
    ).delete()
    """

    TeamModel.objects.create(
        teams = dict(
            team_id         = 1,   ## Auto Increment
            team_name       = "Testchip",
            team_lead       = "Saksham",
            members         = [1, 2, 3, 4, 5],    ## Employe IDs
            team_cost       = 1000000,
            team_projects   = ["x321", "x333", "n555", "n608"]
        )
    )

    new = TeamModel.objects.all()
    for i in new :
        print(i.teams)


