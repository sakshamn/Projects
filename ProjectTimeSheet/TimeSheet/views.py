from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.urls import reverse

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
TODAY = date.today().strftime("%Y-%m-%d")
DEBUG_LOG = open("debug.log", "w")

## Dicts that shall initialise dicts inside function for the first time.
TEAM_DETAILS = dict(
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

## User Global Data Class
class GlobalData() :
    def __init__(self) :
        self.date = TODAY
        self.username = ""

global_data = GlobalData()


## Create your views here.

def redirect_parameters(base_url, parameter) :
    """Use redirect with parameters to be passed to the page you are redirecting to."""
    base_url = reverse(base_url)    ## /base_url/
    parameter = urlencode(parameter)    ## parameter=value
    url = "{}?{}".format(base_url, parameter)   ## /base_url/?parameter=value
    return url


#@login_required
@csrf_exempt
def home(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    _record = CredentialsModel.objects.filter(username=username)

    if (user := authenticate(username=username, password=password)) is None :
        msg = "Invalid Credentials! Try Again or Contact IT Support!"
        return render(request, "registration/login.html", {"login_msg" : msg})
    else :
        login(request, user)

    global_data.username = username

    privilege = _record[0].privilege
    if privilege == "manager" :
        return redirect("/manager/")
    else :
        return redirect("/employee/")
        #return redirect(redirect_parameters("employee", {"username" : username}))


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

    params_dict = {
        "teams" : [],
        "members" : []
    }
    if (selected_team := request.GET.get("select_team")) is None :   ## Default
        params_dict["selected_team"] = "SELECT TEAM"
    else :
        params_dict["selected_team"] = selected_team

    _teams_record = TeamModel.objects.all()
    if len(_teams_record) > 0 :
        for _record in _teams_record :
            params_dict["teams"].append(_record.teams["team_name"])
            if _record.teams["team_name"] == selected_team :
                params_dict["members"] = _record.teams["members"]

    if (remove_team := request.GET.get("remove_team")) is not None :   ## Default
        update_teams(action="delete", team_name=remove_team)

    if (html_page := request.POST.get("html_page")) is None :   ## Default
        html_page = "manager/members.html"
    elif (html_page := request.POST.get("html_page")) == "members" :
        html_page = "manager/members.html"

    return render(request, html_page, params_dict)


@login_required
@csrf_exempt
def employee(request) :
    """Employee main page when a employee logins.
    """

    ## Dict to pass variables to employee.html
    employee_timesheet_dict = {}

    if (timesheet_date := request.GET.get("timesheet_date")) is None :
        timesheet_date = global_data.date

    global_data.date = timesheet_date
    employee_timesheet_dict["timesheet_date"] = timesheet_date
    employee_timesheet_dict["timesheet_msg"] = "Pending Timesheet Dates:"

    #username = request.GET.get("username")

    employee_timesheet_dict = employee_timesheet(request, employee_timesheet_dict)

    return render(request, "employee/employee.html", employee_timesheet_dict)


@xframe_options_sameorigin
def dashboard(request) :
    """
    """
    return render(request, "manager/dashboard.html")


@csrf_exempt
@xframe_options_sameorigin
def timesheets(request) :
    """
    """
    ## Dict to pass variables to timesheets.html
    manager_timesheet_dict = {}

    if (timesheet_date := request.GET.get("timesheet_date")) is None :
        timesheet_date = global_data.date

    manager_timesheet_dict["timesheet_action"] = "none"
    if (timesheet_action := request.POST.get("approved")) is not None :
        manager_timesheet_dict["timesheet_action"] = timesheet_action   ## Get username & project names.
    elif (timesheet_action := request.POST.get("rejected")) is not None :
        manager_timesheet_dict["timesheet_action"] = timesheet_action   ## Get username & project names.

    manager_timesheet_dict["timesheet_reminder"] = "none"
    if (timesheet_reminder := request.POST.get("timesheet_reminder")) is not None :
        manager_timesheet_dict["timesheet_reminder"] = timesheet_reminder   ## Get username & project names.

    global_data.date = timesheet_date
    manager_timesheet_dict["timesheet_date"] = timesheet_date
    manager_timesheet_dict["form"] = EmployeeTimeSheetForm()

    #username = request.GET.get("username")

    manager_timesheet_dict = manager_timesheet(request, manager_timesheet_dict)

    return render(request, "manager/timesheets.html", manager_timesheet_dict)


def manager_timesheet(request, manager_timesheet_dict):
    """
    """
    manager_timesheet_dict["submitted"] = {}
    manager_timesheet_dict["approved"] = {}
    manager_timesheet_dict["rejected"] = {}
    manager_timesheet_dict["pending"] = {}

    ## Local Variables
    _timesheet_date = manager_timesheet_dict["timesheet_date"]

    _timesheet_record = TimeSheetModel.objects.all()
    if len(_timesheet_record) > 0 :
        for _record in _timesheet_record :

            ## Append all projects for the particular date & employee id
            if _record.timesheet["start_date"] <= _timesheet_date <= _record.timesheet["end_date"] :
                _username = _record.timesheet["username"]
                _project_or_activity = _record.timesheet["project_or_activity"]

                ## Is timesheet already submitted for this date by the employee?
                if _timesheet_date in _record.timesheet :

                    ## Check whether the timesheet status is submitted or already approved.
                    if _record.timesheet[_timesheet_date]["timesheet_status"] == "submitted" :
                        ## TODO : store data correctly
                        manager_timesheet_dict["submitted"].setdefault(_username, {})
                        manager_timesheet_dict["submitted"][_username].setdefault(_project_or_activity, _record.timesheet[_timesheet_date])
                        if manager_timesheet_dict["timesheet_action"] != "none" :
                            _user, _project, _status = manager_timesheet_dict["timesheet_action"].split(":")
                            if _record.timesheet["username"] == _user and _record.timesheet["project_or_activity"] == _project :
                                _record.timesheet[_timesheet_date]["timesheet_status"] = _status
                        _record.save()
                    elif _record.timesheet[_timesheet_date]["timesheet_status"] == "approved" :
                        manager_timesheet_dict["approved"].setdefault(_username, {})
                        manager_timesheet_dict["approved"][_username].setdefault(_project_or_activity, _record.timesheet[_timesheet_date])

                    elif _record.timesheet[_timesheet_date]["timesheet_status"] == "rejected" :
                        manager_timesheet_dict["rejected"].setdefault(_username, {})
                        manager_timesheet_dict["rejected"][_username].setdefault(_project_or_activity, _record.timesheet[_timesheet_date])

                else :  ## Employee did not submit the timesheet for the date - timesheet_date
                    manager_timesheet_dict["pending"].setdefault(_username, [])
                    manager_timesheet_dict["pending"][_username].append(_record.timesheet["project_or_activity"])
                    if manager_timesheet_dict["timesheet_reminder"] != "none" :
                        _user, _project_list = manager_timesheet_dict["timesheet_reminder"].split(":")
                        if _record.timesheet["username"] == _user and _record.timesheet["project_or_activity"] in _project_list :
                            ## Create only unique list elements. Add all the dates for a 
                            ## particular user & project record on which timesheet was not
                            ## submitted.
                            _record.timesheet.setdefault("timesheet_reminder", [])
                            if _timesheet_date not in _record.timesheet["timesheet_reminder"] :
                                _record.timesheet["timesheet_reminder"].append(_timesheet_date)
                            _record.save()

    return manager_timesheet_dict


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

            obj = CredentialsModel(username = username, password = password, firstname = firstname, lastname = lastname, email = email, team = team, employee_id = employee_id, employee_ctc = employee_ctc, privilege = privilege)
            obj.save()  ## Save the data

            ## We are using same variables for different purposes here to add a member to team
            ## If a team doesn't exist, it shall be created.
            update_teams(action="add", team_name=team, team_lead=privilege, members={username : [firstname, lastname, email, employee_id, employee_ctc, privilege]}, team_cost=employee_ctc, team_projects=[])

            msg = "Signup Done Successfully!"
        else :
            msg = "Please Correct The Errors Below:"
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"msg" : msg, "form": form})


@xframe_options_sameorigin
@csrf_exempt
def create_timesheet(request):
    msg = ""
    if request.method == 'POST':
        form = TimeSheetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            project_or_activity = form.cleaned_data.get("project_or_activity")

            update_timesheet("manager", username, project_or_activity, start_date=start_date, end_date=end_date)

            msg = "Employee TimeSheet Created Successfully!"
        else :
            msg = "Please Correct The Errors Below:"
    else:
        form = TimeSheetForm()

    return render(request, "manager/create_timesheet.html", {"msg" : msg, "form": form})


def employee_timesheet(request, employee_timesheet_dict):
    """

    Timesheet Date shall be between start_date & end_date. We shall not perform this check
    here because it shall be taken care while displaying the Timesheet form to the employee.
    """
    employee_timesheet_dict["projects_or_activities"] = {
        "submitted" : {},
        "pending" : []
    }

    ## Local Variables
    msg = ""
    _post_dict = dict(request.POST)  ## Get the form responses into a dict. request.POST doesn't work exactly like a dict.

    _timesheet_record = TimeSheetModel.objects.filter(timesheet__username=global_data.username)
    if len(_timesheet_record) > 0 :
        for _record in _timesheet_record :

            ## Append all projects for the particular date & employee id
            if _record.timesheet["start_date"] <= employee_timesheet_dict["timesheet_date"] <= _record.timesheet["end_date"] :

                ## Is timesheet already submitted for this date by the user - username?
                if employee_timesheet_dict["timesheet_date"] in _record.timesheet :
                    ## Take this as list because its easy to iterate over lists in html
                    employee_timesheet_dict["projects_or_activities"]["submitted"][_record.timesheet["project_or_activity"]] = _record.timesheet[employee_timesheet_dict["timesheet_date"]]
                    if employee_timesheet_dict["timesheet_date"] in _record.timesheet["timesheet_reminder"] :
                        _record.timesheet["timesheet_reminder"].remove(employee_timesheet_dict["timesheet_date"])
                    _record.save()
                else :
                    employee_timesheet_dict["projects_or_activities"]["pending"].append(_record.timesheet["project_or_activity"])

        for _date in _record.timesheet["timesheet_reminder"] :
            if _date not in employee_timesheet_dict["timesheet_msg"] :
                employee_timesheet_dict["timesheet_msg"] += f" '{_date}' "


    if request.method == 'POST':
        form = EmployeeTimeSheetForm(request.POST)  ## Get the filled form response
        if form.is_valid(): ## Check for form field errors
            for project_or_activity in employee_timesheet_dict["projects_or_activities"]["pending"] :

                ## Each project_or_activity shall have their own field values separately
                ## pop works correctly because the order of the elements in the lists on both
                ## sides is same - project wise
                tasks = _post_dict["tasks"].pop(0)
                hours = _post_dict["hours"].pop(0)
                comments = _post_dict["comments"].pop(0)

                update_timesheet("employee", global_data.username, project_or_activity, tasks=tasks, hours=hours, comments=comments, timesheet_date=employee_timesheet_dict["timesheet_date"])

            msg = "Employee TimeSheet Created Successfully!"
        else :
            msg = "Please Correct The Errors Below:"
    else:
        ## If form is not submitted, it must be the first time we are displaying the form
        ## Check for the database about the project_or_activity details to be displayed in
        ## HTML table.

        form = EmployeeTimeSheetForm()

    employee_timesheet_dict["msg"] = msg
    employee_timesheet_dict["form"] = EmployeeTimeSheetForm()   ## For printing form with its fields

    return employee_timesheet_dict


def update_timesheet(privilege, username, project_or_activity, start_date="", end_date="", tasks="", hours=0, comments="", timesheet_date="") :
    """Add, update & delete timesheet details using JSONField data.
    """

    if privilege == "manager" :
        TimeSheetModel.objects.create(
            timesheet = dict(
                username = username,
                start_date = str(start_date),
                end_date = str(end_date),
                project_or_activity = project_or_activity,
                timesheet_reminder = []
            )
        )
    elif privilege == "employee" :
        _timesheet_record = TimeSheetModel.objects.filter(timesheet__username=username)
        if len(_timesheet_record) > 0 :
            for _record in _timesheet_record :
                if _record.timesheet["project_or_activity"] == project_or_activity :
                    ## Create a new dict as per the timesheet_date for a particular employee
                    ## and projectwise separately
                    _record.timesheet[timesheet_date] = {}
                    _record.timesheet[timesheet_date]["tasks"] = tasks
                    _record.timesheet[timesheet_date]["hours"] = hours
                    _record.timesheet[timesheet_date]["comments"] = comments
                    _record.timesheet[timesheet_date]["timesheet_status"] = "submitted"

                    _record.save()


def update_teams(action="none", team_name="", team_lead="", members={}, team_cost=0, team_projects=[]) :
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

    if action == "add" :  ## Add only 1 member at a time
        _username, _user_details = list(members.items())[0]
        _teams_record = TeamModel.objects.filter(teams__team_name=team_name)
        if len(_teams_record) > 0 :
            for _record in _teams_record :
                _record.teams["members"][_username] = _user_details ## No check required of user already exists.
                _record.teams["team_cost"] += team_cost ## No check required of user already exists.
                _record.teams["team_lead"] = _username if team_lead == "manager" else _record.teams["team_lead"] ## No check required of user already exists.
            _record.save()
        else :  ## User's Team doesn't exist
            TeamModel.objects.create(
                teams = dict(
                    team_name       = team_name,
                    team_lead       = _username if team_lead == "manager" else "",
                    members         = members,
                    team_cost       = team_cost,
                    team_projects   = team_projects ## TBD : Logic to be added.
                )
            )
    elif action == "update" :
        pass
    elif action == "delete" :
        TeamModel.objects.filter(teams__team_name=team_name).delete()
        print("TEAM Removed:", team_name, file=DEBUG_LOG)


