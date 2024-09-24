from django.contrib.sitemaps import Sitemap

from src.articles.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created
