from apps.blog.models import Blog
from rest_framework import serializers

class BlogCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content is required.")
        return value