from django.contrib import admin
from .models import BlogPost, Category

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_draft')
    search_fields = ('title', 'author__username')
    list_filter = ('is_draft', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category, CategoryAdmin)
