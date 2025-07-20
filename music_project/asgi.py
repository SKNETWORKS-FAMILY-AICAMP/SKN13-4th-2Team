import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import search.routing
import home.routing # home 앱의 routing 임포트

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            search.routing.websocket_urlpatterns + # 기존 검색 라우팅
            home.routing.websocket_urlpatterns     # 홈 챗봇 라우팅 추가
        )
    ),
})