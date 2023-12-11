from django.urls import path

from . import views

urlpatterns = [
    path("getData/", views.index, name="index"),
    path('api/register/', views.register_user, name='register_user'),
    path('google/signin', views.process_login, name='google_login'),
]