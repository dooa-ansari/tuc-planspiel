from django.urls import path
from .views import get_similar_module_against_given_module_uri, list_similar_modules, get_modules_from_course_and_university

urlpatterns = [ 
    path('', get_modules_from_course_and_university, name='get-modules'),
    path('listSimilarModules', list_similar_modules, name='list-similar-modules'),
    path('similarModules', get_similar_module_against_given_module_uri, name='get-similar-modules'),
]