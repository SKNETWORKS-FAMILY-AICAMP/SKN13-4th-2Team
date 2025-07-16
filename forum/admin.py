from django.contrib import admin
from .models import Category, Thread, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username')
    list_filter = ('category', 'author')

class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at', 'updated_at')
    search_fields = ('thread__title', 'author__username')
    list_filter = ('thread', 'author')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)