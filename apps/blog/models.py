from django.db import models

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