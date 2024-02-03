from django.urls import path

from . import views
from .views import extract_text_from_pdf

urlpatterns = [
    path('', extract_text_from_pdf, name="exportPDFToRDF"),
]