from django import forms
from .models import Post
from django.contrib.auth.models import User


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('is_featured', 'no_of_views')

