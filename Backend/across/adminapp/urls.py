from django.urls import path

from .views import upload_file, update_module


urlpatterns= [
    path('api/upload/', upload_file, name='upload_file'),
    path('api/updateModule/', update_module, name='update_module'),
]