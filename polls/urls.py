from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    about,
    LikeView
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/new', CommentCreateView.as_view(), name='post-comment'),




    path('like/<int:pk>', LikeView, name="like_post"),
]