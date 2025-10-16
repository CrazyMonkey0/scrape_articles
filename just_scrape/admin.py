from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'url')
    search_fields = ('title', 'content')
    list_filter = ('published_date',)
    fields = ('title', 'content', 'content_html', 'url', 'published_date')