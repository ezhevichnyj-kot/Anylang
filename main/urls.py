from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.page, name='main_page'),
    path('loadpage', views.loadpage, name='load_page'),
    path('pdfpage/<int:file_id>', views.pdfpage, name='pdf_page'),
]