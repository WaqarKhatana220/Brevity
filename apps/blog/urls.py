from django.urls import path
from .views import BlogCreateView

urlpatterns = [
    path('create', BlogCreateView.as_view(), name='create_blog'),
]