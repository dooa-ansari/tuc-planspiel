from django.urls import path

from .views import  get_universities
from .views import upload_file, update_module, delete_module, insert_module, clean_up_upload_folder


urlpatterns= [
    path('api/upload', upload_file, name='upload_file'),
    path('api/delete/', clean_up_upload_folder, name='clean_directory'),
    path('universitieslist/', get_universities, name="get_universities"),
    path('api/insert/', insert_module, name='insert_module'),
    path('api/delete/', delete_module, name='delete_module'),
    path('api/update/', update_module, name='update_module'),

]