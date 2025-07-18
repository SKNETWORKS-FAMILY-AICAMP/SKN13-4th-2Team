# # faq/views.py
# from django.shortcuts import render
# from .models import FAQ

# def faq_page(request):
#     faqs = FAQ.objects.all()
#     return render(request, 'faq.html', {'faqs': faqs})
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import FAQ
from django.contrib.auth.decorators import login_required

@login_required
def faq_page(request):
    faq_list = FAQ.objects.all()
    paginator = Paginator(faq_list, 5)  # ✅ 페이지당 5개씩

    page_number = request.GET.get('page')  # ?page=2 같은 URL 처리
    page_obj = paginator.get_page(page_number)

    return render(request, 'faq/faq.html', {'page_obj': page_obj})