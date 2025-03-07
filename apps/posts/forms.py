from django import forms

from apps.posts.models import Post, Comment


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


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write a comment...',
        'rows': 2,
        'style': 'resize: none;',
    }))

    class Meta:
        model = Comment
        fields = ['content']
