from django.contrib.sitemaps.views import sitemap
from django.urls import path

from src.articles import views
from src.articles.sitemap import ArticleSitemap

app_name = "articles"

urlpatterns = [
    path(
        "update_article/<int:pk>",
        views.UpdateDetailArticle.as_view(),
        name="update_article",
    ),
    path("update/<int:pk>", views.UpdateArticle.as_view(), name="update"),
    path("article/<slug:slug>", views.ArticleDetailView.as_view(), name="article"),
    path("pdf/<pk>", views.download_article, name="pdf"),
    path("create_article", views.create_article, name="create_article"),
    path("get_subcategory", views.get_subcategory, name="get_subcategory"),
    path("delete_image/<str:pk>", views.deleteimage, name="delete_image"),
    path("search/", views.ArticlesSearchView.as_view(), name="search"),
    path("list/", views.UpdateArticleView.as_view(), name="list"),
    path("info/", views.show, name="info"),  # check pdf html
    path("info/<slug:slug>", views.setted_bids, name="setted_bids"),
    path("get_like/", views.get_like, name="get_like"),
    path("get_dislike/", views.get_dislike, name="get_dislike"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"article": ArticleSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
