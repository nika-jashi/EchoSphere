from apps.posts.models import Post


def get_all_posts():
    return Post.objects.all().order_by('-created_at')


def get_users_posts(user):
    return Post.objects.filter(user=user).order_by('-created_at')