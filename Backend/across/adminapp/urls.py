from django.urls import path

from .views import  get_universities
from .views import upload_file, update_module, delete_module, insert_module, clean_up_upload_folder , csv_rdf, upload_file, update_module, delete_module, insert_module

urlpatterns= [
    path('api/csvToRdf', csv_rdf, name='csv_rdf'),
    path('api/upload/', upload_file, name='upload_file'),
    path('universitieslist/', get_universities, name="get-universities"),
    path('api/insert/', insert_module, name='insert_module'),
    path('api/delete/', delete_module, name='delete_module'),
    path('api/update/', update_module, name='update_module'),
    path('api/deleteclean/', clean_up_upload_folder, name='clean_directory'),

]