# posts/forms.py

from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']  # ✅ Only edit message, not name
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Update your comment...',
                'style': 'width:100%;border-radius:8px;padding:10px;'
            })
        }
