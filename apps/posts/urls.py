from django.contrib.auth.decorators import login_required as l
from django.urls import path

from apps.posts.views import (
    CreatePostView,
    like_post,
    unlike_post,
    DetailPostView,
    DeletePostView,
    EditPostsView,
    AddCommentView
)

app_name = "posts"

urlpatterns = [
    path('create/', l(CreatePostView.as_view(), redirect_field_name='accounts:login'), name='create'),
    path('detail/<int:pk>/', l(DetailPostView.as_view(), redirect_field_name='accounts:login'), name='detail'),
    path('delete/<int:pk>/', l(DeletePostView.as_view(), redirect_field_name='accounts:login'), name='delete'),
    path('update/<int:pk>/', l(EditPostsView.as_view(), redirect_field_name='accounts:login'), name='update'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('unlike_post/<int:post_id>/', unlike_post, name='unlike_post'),
    path('add-comment/<int:post_id>/', AddCommentView.as_view(), name='add_comment'),
]
