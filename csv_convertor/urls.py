from django.urls import path

from . import views

urlpatterns = [
    path("csv", views.GenerateCSV.as_view(), name="csv")
]
