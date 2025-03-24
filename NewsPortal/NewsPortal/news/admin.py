from django.contrib import admin
from .models import Author, Category, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user__username',)
    search_fields = ('user__username',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subscribers__username')
    list_filter = ('subscribers',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('header', 'type', 'rating')
    list_filter = ('author__user', 'type', 'categories__name')
    search_fields = ('header',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'rating')
    list_filter = ('user__username',)
    search_fields = ('content',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
