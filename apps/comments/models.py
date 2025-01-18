from django.db import models
from ..models import BaseModel

# Create your models here.
class Comment(BaseModel):
    blog = models.ForeignKey('blog.Blog', on_delete=models.CASCADE)
    writer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return f'{self.writer.last_name}: {self.text[:20]}'
    
    class Meta:
        ordering = ['-created_at']
        
    def is_writer(self, user):
        return self.writer == user