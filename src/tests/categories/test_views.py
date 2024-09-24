from http import client as http_client

from django.urls import reverse


def test_categoryview():
    resp = reverse("categories:category")
    assert http_client.OK, resp
