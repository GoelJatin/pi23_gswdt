from django.urls import path

from pi23_gswdt.organisations.views import current_datetime

app_name = "organisations"
urlpatterns = [
    path("", view=current_datetime, name="index"),
]
