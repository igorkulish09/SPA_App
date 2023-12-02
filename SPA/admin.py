from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'home_page', 'captcha', 'text', 'parent_comment', 'created_at')
    search_fields = ('user_name', 'email', 'text')
