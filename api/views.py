from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer
from blogapp.models import Post, CommentReply, Comment, Category
from django.shortcuts import get_object_or_404
from rest_framework import permissions


class SingleCommentMixin:
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        queryset = Comment.objects.filter(post=post)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['comment_id'])
        return obj


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class PostDetailDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class CreatePost(generics.CreateAPIView):
    queryset = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return super().get_queryset().objects.filter(post__id=post_id)


class SingleCommentView(SingleCommentMixin, generics.RetrieveAPIView):
    serializer_class = CommentSerializer


class SingleCommentUpdateView(SingleCommentMixin, generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


class SingleCommentDeleteView(SingleCommentMixin, generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryLastTenPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post

    def get_queryset(self):
        category_id=self.kwargs['category_id']
        return super().get_queryset().objects.filter(category__id=category_id)[:10]
