from django.urls import path

from . import views
from .views import google_logout, user_profile

urlpatterns = [
    path("", views.index, name="index"),
    path("listsimilarmodules/", views.listsimilarmodules, name="listsimilarmodules"),
    path("translator/", views.translator, name="translator"),
    path("getData/", views.index, name="index"),
    path('api/register/', views.register_user, name='register_user'),
    path('google/signin', views.google_login, name='google_login'),
    path('google/logout/', google_logout, name='google-logout'),
    path('user/profile/', user_profile, name='user_profile'),
]