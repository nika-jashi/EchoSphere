from django.contrib.auth.decorators import login_required as l
from django.urls import path

from apps.posts.views import CreatePostView, AllPostsView, like_post, unlike_post

app_name = "posts"

urlpatterns = [
    path('create/', l(CreatePostView.as_view(), redirect_field_name='accounts:login'), name='create'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('unlike_post/<int:post_id>/', unlike_post, name='unlike_post'),
]
