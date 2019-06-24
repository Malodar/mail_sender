# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import upload_csv, send_bulk_emails, index


urlpatterns = [
    # path('', TemplateView.as_view(template_name='main_app/index.html'), name='home'),
    path('', index, name='home'),
    path('upload/csv/', upload_csv, name='upload_csv'),
    path('send_bulk_emails/', send_bulk_emails, name='email_sending'),
    path('sent_emails/', TemplateView.as_view(template_name='main_app/sent_mails.html'), name='sent'),
]
