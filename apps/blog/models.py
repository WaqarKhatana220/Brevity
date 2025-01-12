from django.db import models

from .workflows import BlogWorkflow

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Author(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='authors')

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        
class Blog(BaseModel, BlogWorkflow):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    def __str__(self):
        return f'{self.author} - {self.title[:25]}'