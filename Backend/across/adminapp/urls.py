from django.urls import path

from .views import upload_file, update_module, delete_module


urlpatterns= [
    path('api/upload/', upload_file, name='upload_file'),
    path('api/insert/', update_module, name='update_module'),
    path('api/delete/', delete_module, name='delete_module'),
]