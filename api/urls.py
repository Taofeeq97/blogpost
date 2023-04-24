from django.urls import path
from . import views


urlpatterns = [
    path('blogs/', views.PostListView.as_view()),
    path('blog/search', views.PostSearchListView.as_view()),
    path('blogs/<int:pk>/', views.PostDetailView.as_view()),
    path('blogs/create/', views.PostCreateView.as_view()),
    path('blogs/<int:pk>/update/', views.PostDetailUpdateView.as_view()),
    path('blogs/<int:pk>/delete/', views.PostDetailDeleteView.as_view()),
    path('blogs/category_posts/<int:category_id>/', views.CategoryLastTenPostView.as_view()),
    path('blogs/<int:post_id>/comments/', views.CommentView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/', views.SingleCommentView.as_view()),
    path('blogs/<int:pk>/comments/create/', views.SingleCommentCreate.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/update', views.SingleCommentUpdateView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/delete/', views.SingleCommentDeleteView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/reply/', views.CommentRepliesView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/reply/create/', views.SingleCommentReplyCreate.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/reply/<int:reply_id>/update', views.SingleCommentReplyUpdateView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/reply/<int:reply_id>/delete', views.SingleCommentReplyDeleteView.as_view()),


]