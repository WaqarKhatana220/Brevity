from rest_framework import serializers
from .models import Subscribers

class SubscribersSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    subscribed_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscribers
        fields = ['username', 'full_name', 'subscribed_at']
        
    def get_username(self, obj):
        return obj.subscriber.username
    
    def get_full_name(self, obj):
        return obj.subscriber.name
    
    def get_subscribed_at(self, obj):
        return obj.subscribed_at
    
class SubscribedAuthorsSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    linkedin = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscribers
        fields = ['username', 'full_name']
        
    def get_username(self, obj):
        return obj.author.user.username
    
    def get_full_name(self, obj):
        return obj.author.user.name
    
    def get_bio(self, obj):
        return obj.author.bio
    
    def get_linkedin(self, obj):
        return obj.author.linkedin_handle