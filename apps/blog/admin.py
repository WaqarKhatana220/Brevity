from django.contrib import admin
from .models import Author, Blog
from .workflows import BlogWorkflow
from viewflow.fsm import FlowAdminMixin

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
        "id",
        "author",
        "title",
        "content",
        "state",
    )
    search_fields = (
        "state",
    )
    list_filter = (
        "author",
        "state",
    )
    ordering = (
        "id",
    )

