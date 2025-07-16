from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(('home.urls', 'home'), namespace='home')),
    path('admin/', admin.site.urls),
    path('chatbot/', include(('chatbot.urls', 'chatbot'), namespace='chatbot')),
    path('mypage/', include(('mypage.urls', 'mypage'), namespace='mypage')),
    path('forum/', include(('forum.urls', 'forum'), namespace='forum')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
