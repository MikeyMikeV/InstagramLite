from django.urls import re_path
from .consumers import PostDetailConsumer, HomePageConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/post/(?P<post_id>\w+)/$', PostDetailConsumer.as_asgi()
    ),
    re_path(
        r'ws/homepage/(?P<profile_id>\w+)/$',HomePageConsumer.as_asgi()
    )
]