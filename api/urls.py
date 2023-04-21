from django.urls import path
from . import views


urlpatterns = [
    path('blogs/', views.PostListView.as_view()),
    path('blogs/<int:pk>/', views.PostDetailView.as_view()),
    path('blogs/create/', views.CreatePost.as_view()),
    path('blogs/<int:pk>/update/', views.PostDetailUpdateView.as_view()),
    path('blogs/<int:pk>/delete/', views.PostDetailDeleteView.as_view()),
    path('blogs/category_posts/<int:category_id>/', views.CategoryLastTenPostView.as_view()),
    path('blogs/<int:post_id>/comments/', views.CommentView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/', views.SingleCommentView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/update/', views.SingleCommentUpdateView.as_view()),
    path('blogs/<int:pk>/comments/<int:comment_id>/delete/', views.SingleCommentDeleteView.as_view()),

]