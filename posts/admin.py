from django.contrib import admin
from .models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)