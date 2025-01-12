from django.contrib import admin
from .models import Author, Blog, BlogChangeLog
from .workflows import BlogWorkflow
from viewflow.fsm import FlowAdminMixin

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user",
    )
    ordering = (
        "-id",
    )
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "content",
        "state",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "state",
    )
    list_filter = (
        "author",
        "state",
    )
    ordering = (
        "-created_at",
    )

@admin.register(BlogChangeLog)
class BlogChangeLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blog",
        "changed_by",
        "changed_at",
        "source",
        "target",
    )
    search_fields = (
        "source",
        "target",
    )
    list_filter = (
        "blog",
        "changed_by",
    )
    ordering = (
        "-id",
    )