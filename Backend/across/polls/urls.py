from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("translator/", views.translator, name="translator")
]