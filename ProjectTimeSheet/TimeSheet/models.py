from django.db import models

## Create your models here.

class CredentialsModel(models.Model) :
    """Table with login credentials & details for every employee.
    """
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    team = models.CharField(max_length=30)
    employee_id = models.IntegerField()
    employee_ctc = models.IntegerField()
    privilege = models.CharField(max_length=10, choices = [ ("manager", "Manager"), ("employee", "Employee") ], default = "employee")
    class Meta :
        db_table = "CredentialsModel"


class TeamModel(models.Model) :
    """Create a model for storing Team names."""
    teams = models.JSONField()


class ProjectModel(models.Model) :
    """Create a model for storing Project names."""
    projects = models.JSONField()


class TimeSheetModel(models.Model) :
    """Create a model for storing TimeSheets."""
    timesheet = models.JSONField()


