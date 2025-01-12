from django.urls import path
from .views import BlogCreateView, BlogListView

urlpatterns = [
    path('', BlogListView.as_view(), name='list_blogs'),
    path('create', BlogCreateView.as_view(), name='create_blog'),
]