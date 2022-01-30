# Imports Begin #
from django.urls import path
from . import views
# Imports End #

app_name = "create_accounts"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("create_accounts/signup/", views.signup_form, name="signup"),
    path("create_accounts/login/", views.login_form, name="login"),
    path("create_accounts/logout/", views.logout_form, name="logout")
]

