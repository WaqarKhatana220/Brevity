from django.contrib import admin
from .models import Subscribers

# Register your models here.
@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'author', 'subscribed_at')
    search_fields = ('subscriber', 'author')
    list_filter = ('subscriber', 'author')