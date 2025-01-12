from django.contrib import admin
from .models import Author, Blog

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
    )
    search_fields = (
        "user",
    )
    ordering = (
        "id",
    )
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "state",
        "content",
    )
    search_fields = (
        "author",
        "state",
    )
    list_filter = (
        "author",
        "state",
    )
    ordering = (
        "id",
    )