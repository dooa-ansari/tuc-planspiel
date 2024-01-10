from django.urls import path

from .views import  get_universities
from .views import csv_rdf, upload_file, update_module, delete_module


urlpatterns= [
    path('api/csvToRdf', csv_rdf, name='csv_rdf'),
    path('api/upload/', upload_file, name='upload_file'),
    path('universitieslist/', get_universities, name="get-universities"),
    path('api/insert/', update_module, name='update_module'),
    path('api/delete/', delete_module, name='delete_module'),
]