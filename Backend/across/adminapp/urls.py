from django.urls import path

from .views import upload_file, get_universities


urlpatterns= [
    path('api/upload/', upload_file, name='upload_file'),
    path('universitieslist/', get_universities, name="get-universities"),
]