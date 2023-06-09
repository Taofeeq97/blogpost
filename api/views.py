from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, CommentRepliesSerializer
from blogapp.models import Post, CommentReply, Comment, Category
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .serializers import WeatherRealtimeSerializer, WeatherForecastSerializer


class SingleCommentMixin:
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment_queryset = Comment.objects.filter(post=post)
        return comment_queryset

    def get_object(self):
        comment_queryset = self.get_queryset()
        single_comment = get_object_or_404(comment_queryset, pk=self.kwargs['comment_id'])
        return single_comment


class SingleCommentReplyMixin:
    def get_queryset(self):
        post_id = self.kwargs['pk']
        comment_id = self.kwargs['comment_id']
        comment_reply_queryset = CommentReply.objects.filter(comment__post_id=post_id, comment_id=comment_id)
        return comment_reply_queryset

    def get_object(self):
        comment_reply_queryset = self.get_queryset()
        reply = get_object_or_404(comment_reply_queryset, id=self.kwargs['reply_id'])
        return reply


class OwnerPostCreateMixin:
    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        serializer.save(owner=self.request.user, post=post)


class PostListView(generics.ListAPIView):
    queryset = Post
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post
    serializer_class = PostSerializer


class PostDetailUpdateView(generics.UpdateAPIView):
    queryset = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class PostDetailDeleteView(generics.DestroyAPIView):
    queryset = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class PostCreateView(generics.CreateAPIView):
    queryset = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return super().get_queryset().objects.filter(post__id=post_id)


class SingleCommentCreate(OwnerPostCreateMixin, SingleCommentMixin, generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


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
        category_id = self.kwargs['category_id']
        return super().get_queryset().objects.filter(category__id=category_id).order_by('-created')[:10]


class CommentRepliesView(generics.ListAPIView):
    serializer_class = CommentRepliesSerializer
    queryset = CommentReply

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        return super().get_queryset().objects.filter(comment=comment)


class SingleCommentReplyCreate(OwnerPostCreateMixin, SingleCommentReplyMixin, generics.CreateAPIView):
    serializer_class = CommentRepliesSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        serializer.save(comment=get_object_or_404(Comment, id=self.kwargs['comment_id']))


class SingleCommentReplyUpdateView(SingleCommentReplyMixin, generics.UpdateAPIView):
    serializer_class = CommentRepliesSerializer


class SingleCommentReplyDeleteView(SingleCommentReplyMixin, generics.DestroyAPIView):
    serializer_class = CommentRepliesSerializer


class PostSearchListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post

    def get_queryset(self):
        query = self.request.query_params.get('q')
        return super().get_queryset().objects.filter(Q(title__icontains=query))



class WeatherLocationSearchApiView(APIView):
    def get(self, request):
        weather_url = "https://weatherapi-com.p.rapidapi.com/current.json"

        location = self.request.query_params.get('location')
        url_query = {'q': location}

        headers = {
            "content-type": "application/octet-stream",
            "X-RapidAPI-Key": "7613a5777dmshc0a19d85c6372d7p197f98jsn2c004a89fa6d",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(url=weather_url, params=url_query, headers=headers)
        serializer = WeatherRealtimeSerializer(response.json())
        return Response(serializer.data)


class WeatherLocationForcastApiView(APIView):
    def get(self, request):
        location = self.request.query_params.get('location')
        date = self.request.query_params.get('date')
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        querystring = {"q": location, "dt": date}

        headers = {
            "content-type": "application/octet-stream",
            "X-RapidAPI-Key": "7613a5777dmshc0a19d85c6372d7p197f98jsn2c004a89fa6d",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
        serializer=WeatherForecastSerializer(response.json())
        return Response(serializer.data)