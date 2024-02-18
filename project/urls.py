from django.contrib import admin
from django.urls import path, include
from posts.views import home_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('profiles.urls')),
    path('', home_page, name = 'home_page'),
    path('post/', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)