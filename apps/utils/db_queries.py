from apps.posts.models import Post


def get_all_posts():
    return Post.objects.all().order_by('-created_at')