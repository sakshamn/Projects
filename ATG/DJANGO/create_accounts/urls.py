# Imports Begin #
from django.urls import path
from . import views
# Imports End #

app_name = "create_accounts"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup/", views.signup_form, name="signup"),
    path("login/", views.login_form, name="login"),
    path("logout/", views.logout_form, name="logout")
]

