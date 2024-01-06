from django.urls import path

from . import views
from .views import google_logout, user_profile, authenticate_user_login, get_courses_from_university, get_modules_from_course_and_university

urlpatterns = [
    path("", views.index, name="index"),
    path("listsimilarmodules/", views.listsimilarmodules, name="listsimilarmodules"),
    path("getData/", views.index, name="index"),
    path('api/register/', views.register_user, name='register_user'),
    path('google/signin', views.google_login, name='google_login'),
    path('google/logout/', google_logout, name='google-logout'),
    path('user/profile/', user_profile, name='user_profile'),
    path('login', authenticate_user_login, name="user_login"),
    path('courses/', get_courses_from_university, name="get-courses"),
    path('modules/', get_modules_from_course_and_university, name="get-modules"),

]