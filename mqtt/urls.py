from . import views
from django.urls import path, include

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("", views.index, name="index"),
]
