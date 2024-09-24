from django.contrib import admin

from src.articles.models import Article
from src.articles.models import ImageUpload


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("article", "slug")


admin.site.register(ImageUpload)
