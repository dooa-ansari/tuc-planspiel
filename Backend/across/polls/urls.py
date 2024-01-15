from django.urls import path

from . import views
from .views import google_logout, user_profile, authenticate_user_login, get_courses_from_university, get_modules_from_course_and_university, get_similar_module_against_given_module_uri, save_completed_modules_by_user, get_completed_modules_by_user, select_university_after_signup, get_universities

urlpatterns = [
    path("", views.index, name="index"),
    path("listsimilarmodules", views.listsimilarmodules, name="listsimilarmodules"),
    path("getData", views.index, name="index"),
    path('register', views.register_user, name='register_user'),
    path('google/signin', views.google_login, name='google_login'),
    path('google/logout', google_logout, name='google-logout'),
    path('user/profile', user_profile, name='user_profile'),
    path('login', authenticate_user_login, name="user_login"),
    path('courses/', get_courses_from_university, name="get-courses"),
    path('modules/', get_modules_from_course_and_university, name="get-modules"),
    path('similarModules/', get_similar_module_against_given_module_uri, name="get-similar-modules"),
    path('completedModulesofUser', save_completed_modules_by_user, name="save-completed-modules-by-user"),
    path('getcompletedModulesofUser', get_completed_modules_by_user, name="get-completed-modules-by-user"),
    path('selectUniversity', select_university_after_signup, name="select-university"),
    path('getUniversities', get_universities, name="get-universities"),

]