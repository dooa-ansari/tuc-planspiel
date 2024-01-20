from django.urls import path
from .views import csv_rdf, upload_file, update_module, delete_module, insert_module, get_universities


urlpatterns= [
    path('api/csvToRdf', csv_rdf, name='csv-rdf'),
    path('api/upload', upload_file, name='upload-file'),
    path('api/universitieslist', get_universities, name="get-universities"),
    path('api/insert', insert_module, name='insert-module'),
    path('api/delete', delete_module, name='delete-module'),
    path('api/update', update_module, name='update-module'),
]