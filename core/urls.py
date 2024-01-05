from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.posts.views import AllPostsView
from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('posts/', include('apps.posts.urls')),
    path('news-feed/', AllPostsView.as_view(), name='news-feed'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
