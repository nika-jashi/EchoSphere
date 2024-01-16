from django import forms

from apps.posts.models import Post


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image']


class NewsFeedForm(forms.Form):
    class Meta:
        model = Post
        fields = ['__all__']


class DetailPostForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image', 'created_at', 'updated_at', 'likes']
        exclude = ['created_at', 'updated_at']
