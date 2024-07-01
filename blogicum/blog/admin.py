from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostInLine(admin.TabularInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = (
        'title',
        'description',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'text',
        'author',
        'is_published',
    )
    list_editable = ('is_published',)
    list_filter = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('id', 'title', 'author', 'text', 'category',
                    'pub_date', 'location', 'is_published', 'created_at')
    list_display_links = ('title',)
    list_editable = ('category', 'is_published', 'location')
    list_filter = ('created_at',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
