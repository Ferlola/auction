import pytest
from django import urls
from django.test import TestCase

from src.articles.forms import AuctionForm
from src.articles.models import Article
from src.categories.models import Category
from src.categories.models import Subcategory
from src.users.models import User


@pytest.mark.django_db()
def test_url_login(client, create_user):
    client.force_login(create_user, create_user.password)
    form_url = urls.reverse("account_login")
    resp = client.post(form_url)
    assert resp.status_code == 200  # noqa:PLR2004


@pytest.mark.django_db()
def test_redirect_login(client, create_article_url):
    form_url = urls.reverse("articles:create_article")
    resp = client.post(form_url, data=create_article_url)
    assert resp.status_code == 302  # noqa:PLR2004


class TestArticleForm(TestCase):
    @pytest.mark.django_db()
    def test_valid_form(self):
        user = User.objects.create(
            name="user_test",
            email="user_test@example.com",
            password="7@p5ekret",  # noqa:S106
        )
        category = Category.objects.create(name="category_test")
        subcategory = Subcategory.objects.create(
            name="subcategory_test",
            category=category,
        )
        article = Article.objects.create(
            article="New article",
            description="New description",
            location="New location",
            category=category,
            subcategory=subcategory,
            user=user,
        )
        data = {
            "article": article.article,
            "description": article.description,
            "location": article.location,
            "category": category,
            "subcategory": subcategory,
            "user": user,
        }

        form = AuctionForm(data=data)
        assert form.is_valid()
        assert isinstance(article, Article)
        assert article.__str__(), article.article
