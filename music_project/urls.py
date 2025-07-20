from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(('home.urls', 'home'), namespace='home')),
    path('admin/', admin.site.urls),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('mypage/', include(('mypage.urls', 'mypage'), namespace='mypage')),
    path('forum/', include(('forum.urls', 'forum'), namespace='forum')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('faq/', include('faq.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # 소셜 로그인 URL 추가
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)