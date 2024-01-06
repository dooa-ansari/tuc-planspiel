from django.urls import path

from .views import upload_file, get_universities, add_module
from .views import upload_file, update_module


urlpatterns= [
    path('api/upload/', upload_file, name='upload_file'),
    path('universitieslist/', get_universities, name="get-universities"),
    path('addmodule/', add_module, name="add-module"),
    path('api/insert/', update_module, name='update_module'),
]