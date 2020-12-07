from django.contrib import admin
from TimeSheet.models import CredentialsModel

## Register your models here.

## Register admin with the CredentialsModel table.
#admin.site.register(CredentialsModel)

class CredentialsAdmin(admin.ModelAdmin) :
    """Class to make customisations to the admin website.

    To change the order in which the rows are displayed in list of recorded data
    at the admin site.
    """
    ## This shall show filters at right side with the following fields to filter.
    list_filter = ("privilege",)


## Register class CredentialsAdmin with table CredentialsModel.
admin.site.register(CredentialsModel, CredentialsAdmin)

