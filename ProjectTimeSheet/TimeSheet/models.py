from django.db import models

## Create your models here.

class Credentials(models.Model) :
    """Table with login credentials for every employee.
    """
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    privilege = models.CharField(max_length=10, choices = [ ("manager", "Manager"), ("employee", "Employee") ], default = "employee")
    class Meta :
        db_table = "Credentials"


#class EmployeeProfile(models.Model) :
#    username = models.CharField(max_length=10)
#    name = models.CharField(max_length=30)
#    password = models.CharField(default="login123", max_length=10)
#    email = models.EmailField(max_length=30)
#    team = models.CharField(max_length=30)
#    project = models.TextField()
#    privilege = models.CharField(max_length=10, choices = [ ("manager", "Manager"), ("employee", "Employee") ], default = "employee")
#    class Meta :
#        db_table = "EmployeeProfile"



