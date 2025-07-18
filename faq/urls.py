# faq/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.faq_page, name='faq'), # ✅ name='faq' 꼭 있어야 함
]