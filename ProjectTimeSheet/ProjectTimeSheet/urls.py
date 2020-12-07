"""ProjectTimeSheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from TimeSheet.views import home, signup, manager, employee, dashboard, teams, timesheet, timesheets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    path('signup/', signup, name='signup'),
    path('manager/', manager),
    path('employee/', employee, name="employee"),
    path('manager/dashboard.html', dashboard),
    path('manager/timesheets.html', timesheets, name="timesheets"),
    path('manager/teams.html', teams),
    path('teams/', teams),
    path('timesheet/', timesheet, name="timesheet"),
]

