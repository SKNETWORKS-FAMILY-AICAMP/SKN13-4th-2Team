# faq/views.py
from django.shortcuts import render
from .models import FAQ

def faq_page(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})