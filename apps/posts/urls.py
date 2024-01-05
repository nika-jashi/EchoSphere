from django.contrib.auth.decorators import login_required as l
from django.urls import path

from apps.posts.views import CreatePostView, AllPostsView

app_name = "posts"

urlpatterns = [
    path('create/', l(CreatePostView.as_view(), redirect_field_name='accounts:login'), name='create'),
]
