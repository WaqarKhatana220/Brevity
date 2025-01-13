from django.db import models

# Create your models here.
class Subscribers(models.Model):
    subscriber = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='subscribed_authors')
    author = models.ForeignKey('blog.Author', on_delete=models.CASCADE, related_name='subscribers')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'author')
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.subscriber.username} follows {self.author.username}"