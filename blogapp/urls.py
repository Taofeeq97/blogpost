from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category_id>/post/<str:post_id>/', views.post_detail, name='detail'),
    path('create_post/',views.CreatePost.as_view(), name='create_post'),
    path('category/<str:category_id>/post/<int:pk>/update/', views.UpdatePost.as_view(), name='update_post'),
    path('category/<str:category_id>/post/<int:pk>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path('create_account/', views.CreateUserAccount, name='create_account'),
    path('comment/<int:pk>/delete', views.DeleteComment.as_view(), name='delete_comment'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('contact/', views.contact, name='contact'),

]
