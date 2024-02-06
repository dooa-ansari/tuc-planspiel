from django.urls import path

from . import views
from .views import pdfToRdf

urlpatterns = [
    path('api/pdfToRdf', pdfToRdf, name='pdfToRdf'),
]