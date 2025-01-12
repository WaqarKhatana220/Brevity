from django.urls import path
from .views import BlogCreateView, BlogListView, BlogDeleteView

urlpatterns = [
    path('', BlogListView.as_view(), name='list_blogs'),
    path('create', BlogCreateView.as_view(), name='create_blog'),
    path('delete/<int:blog_id>', BlogDeleteView.as_view(), name='delete_blog'),
]