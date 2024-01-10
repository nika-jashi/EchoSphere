from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from apps.posts.forms import PostForm
from apps.posts.models import Post
from apps.utils.db_queries import get_all_posts


class CreatePostView(View):
    template_name = 'posts/create.html'

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('accounts:profile')

        return render(request, self.template_name, {'form': form})


class AllPostsView(View):
    template_name = 'feed/news_feed.html'

    def get(self, request):
        news_feed_posts = get_all_posts()

        return render(request, self.template_name, {'news_feed_posts': news_feed_posts})


def like_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        post.likes.add(request.user)
        post.save()
        return redirect('news-feed')
    return HttpResponse(status=400)


def unlike_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        post.likes.remove(request.user)
        post.save()
        return redirect('news-feed')
    return HttpResponse(status=400)
