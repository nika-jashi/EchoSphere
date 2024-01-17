from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.posts.forms import PostForm, DetailPostForm
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


class DetailPostView(View):
    template_name = 'posts/details.html'

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        return render(request, self.template_name, {'post': post})


class DeletePostView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('accounts:profile')


class AllPostsView(View):
    template_name = 'feed/news_feed.html'

    def get(self, request):
        news_feed_posts = get_all_posts()

        return render(request, self.template_name, {'news_feed_posts': news_feed_posts})


class EditPostsView(View):
    template_name = 'posts/edit.html'

    def get(self, request, pk, *args, **kwargs):
        instance = Post.objects.get(pk=pk)
        form = DetailPostForm(instance=instance)
        context = {
            'post': instance,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        post_instance = get_object_or_404(Post, pk=pk)
        form = DetailPostForm(request.POST, request.FILES, instance=post_instance)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', pk)

        return render(request, self.template_name, {'form': form})


def like_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        post.likes.add(request.user)
        post.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def unlike_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        post.likes.remove(request.user)
        post.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)
