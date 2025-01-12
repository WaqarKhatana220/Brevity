from django.urls import path
from .views import BlogCreateView, BlogListView, BlogDeleteView, BlogPublishView, BlogEditView, BlogArchiveView

urlpatterns = [
    path('', BlogListView.as_view(), name='list_blogs'),
    path('create', BlogCreateView.as_view(), name='create_blog'),
    path('delete/<int:blog_id>', BlogDeleteView.as_view(), name='delete_blog'),
    path('publish/<int:blog_id>', BlogPublishView.as_view(), name='publish_blog'),
    path('edit/<int:blog_id>', BlogEditView.as_view(), name='edit_blog'),
    path('archive/<int:blog_id>', BlogArchiveView.as_view(), name='archive_blog'),
]