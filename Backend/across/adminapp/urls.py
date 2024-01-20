from django.urls import path
from .views import csv_rdf, upload_file, update_module, delete_module, insert_module, get_universities


urlpatterns= [
    path('csvToRdf', csv_rdf, name='csv-rdf'),
    path('upload', upload_file, name='upload-file'),
    path('universitieslist', get_universities, name="get-universities"),
    path('insertModule', insert_module, name='insert-module'),
    path('deleteModule', delete_module, name='delete-module'),
    path('updateModule', update_module, name='update-module'),
]