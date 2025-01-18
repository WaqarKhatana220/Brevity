from django.db import models
from .workflows import BlogWorkflow
from ..models import BaseModel

# Create your models here.
        
class Author(BaseModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='authors')
    bio = models.TextField(blank=True)
    linkedin_handle = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        
    def __str__(self):
        return f'{self.user}'
    
    def total_blogs(self):
        return self.blogs.count()
    
    def get_drafted_blogs(self):
        return self.blogs.filter(state=BlogWorkflow.STATE_DRAFT)
    
    def get_published_blogs(self):
        return self.blogs.filter(state=BlogWorkflow.STATE_PUBLISHED)
    
    def get_edited_blogs(self):
        return self.blogs.filter(state=BlogWorkflow.STATE_EDITED)
    
    def get_archived_blogs(self):
        return self.blogs.filter(state=BlogWorkflow.STATE_ARCHIVED)
    
    def is_subscribed_by(self, user):
        return self.subscribers.filter(subscriber=user).exists()
    
    def get_subscribers(self):
        return self.subscribers.all()
    
    def get_subscribers_count(self):
        return self.subscribers.count()

        
class Blog(BaseModel, BlogWorkflow):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
    
    def is_author(self, author):
        return self.author == author
    
class BlogChangeLog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='change_logs')
    changed_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='change_logs')
    changed_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Blog Change Log'
        verbose_name_plural = 'Blog Change Logs'
        
    def __str__(self):
        return f'{self.changed_by}-{self.blog.title[:10]}'