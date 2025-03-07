import os
import uuid

from django.db import models

from apps.accounts.models import CustomAccount


def post_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'posts', filename)


class Post(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomAccount, related_name='liked_posts', blank=True)
    image = models.ImageField(upload_to=post_file_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Post ({self.created_at})"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE)
    content = models.TextField()
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.content}'
