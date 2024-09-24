from http import client as http_client

import pytest
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from src.articles.models import Article
from src.users.models import User

client = Client()


class IndexPageTests(TestCase):
    def setUp(self):
        url = reverse("index")
        self.response = self.client.get(url)

    def test_index_template(self):
        self.assertTemplateUsed(self.response, "articles/list.html")


@pytest.mark.django_db()
def test_user(create_user):
    assert isinstance(create_user, User)


@pytest.mark.django_db()
def test_article(create_article):
    assert isinstance(create_article, Article)


@pytest.mark.django_db()
def test_article_list_view():
    response = client.get(reverse("index"))
    assert response.status_code, 200
    assert response, "article test"


@pytest.mark.django_db()
def test_article_detail(create_article):
    resp = client.get(reverse("articles:article", kwargs={"slug": create_article.slug}))
    assert http_client.OK, resp.status_code
    assert resp.status_code == 200  # noqa:PLR2004


@pytest.mark.django_db()
def test_article_update(create_article):
    resp = client.get(
        reverse("articles:update_article", kwargs={"pk": create_article.pk}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp.templates == "/accounts/login/?next=/articles/update_article/1"


@pytest.mark.django_db()
def test_update(create_article):
    resp = client.get(reverse("articles:update", kwargs={"pk": create_article.pk}))
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp.templates == "/accounts/login/?next=/articles/update/1"


def test_search():
    resp = reverse("articles:search")
    assert http_client.OK, resp


@pytest.mark.django_db()
def test_redirect_to_login(client):
    resp = client.get(reverse("articles:create_article"))
    assert resp.status_code == 302  # noqa:PLR2004
    assert http_client.OK, resp.status_code
    assert resp.templates == "/accounts/login/?next=/articles/create_article"


@pytest.mark.django_db()
def test_login():
    client = Client()
    resp = client.post(
        path=reverse("account_login"),
        data={
            "email": "testuserh@testuser.com",
            "password": "passwordtestuser",
        },
    )
    assert resp.status_code == 200  # noqa:PLR2004
    assert resp.status_code == http_client.OK


@pytest.mark.django_db()
def test_download_article(create_article):
    resp = reverse("articles:pdf", kwargs={"pk": create_article.id})
    assert resp == "/articles/pdf/1"


@pytest.mark.django_db()
def test_delete_image(create_image):
    client = Client()
    resp = client.get(reverse("articles:delete_image", kwargs={"pk": create_image.pk}))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp.templates == "/accounts/login/?next=/articles/delete_image/1"
