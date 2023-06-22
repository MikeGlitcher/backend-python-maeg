from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import registration_view, GoLogin, GoSignUp, ProfileView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", GoLogin.as_view(), name="login"),
    path("register2/", registration_view),
    path("register/", GoSignUp.as_view(), name="signup"),
]