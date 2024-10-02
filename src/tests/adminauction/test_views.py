from http import client as http_client

import pytest
from django.test.client import Client
from django.urls import reverse

client = Client()


@pytest.mark.django_db()
def test_updatearticle(create_article):
    resp = client.get(
        reverse("adminauction:update_article", kwargs={"pk": create_article.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/update_article/1"


@pytest.mark.django_db()
def test_categoryview():
    resp = client.get(reverse("adminauction:create_category"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/create_category/"


@pytest.mark.django_db()
def test_subcategoryview():
    resp = client.get(reverse("adminauction:create_subcategory"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/create_subcategory/"


@pytest.mark.django_db()
def test_feeview():
    resp = client.get(reverse("adminauction:fee"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/fee/"


@pytest.mark.django_db()
def test_permissionupdatearticle():
    resp = client.get(reverse("adminauction:setting"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/setting/"


@pytest.mark.django_db()
def test_bidarticle(create_article):
    resp = client.get(reverse("adminauction:article", kwargs={"pk": create_article.id}))
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/article/1/"


@pytest.mark.django_db()
def test_deleteunsubscribedb():
    resp = client.get(reverse("adminauction:delete_unsubcribe"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/delete_unsubscribe/"


@pytest.mark.django_db()
def test_deleteunsubscribe(create_user):
    resp = client.get(
        reverse("adminauction:delete_unsubscribed", kwargs={"pk": create_user.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert (
        resp["Location"] == "/accounts/login/?next=/adminauction/delete_unsubscribed/2"
    )


@pytest.mark.django_db()
def test_usersdb():
    resp = client.get(reverse("adminauction:users_db"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/users_db"


@pytest.mark.django_db()
def test_deletecheckoutdb():
    resp = client.get(reverse("adminauction:delete_checkout"))
    assert resp.status_code, http_client.OK
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/delete_checkout/"


@pytest.mark.django_db()
def test_deletecheckoutdonedb(create_checkout):
    resp = client.get(
        reverse("adminauction:delete_checkoutt", kwargs={"pk": create_checkout.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/delete_checkout/1"


@pytest.mark.django_db()
def test_deletecategory(create_category):
    resp = client.get(
        reverse("adminauction:delete_category", kwargs={"pk": create_category.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/delete_category/1/"


@pytest.mark.django_db()
def test_deletecategorydone(create_category):
    resp = client.get(
        reverse("adminauction:delete_category_done", kwargs={"pk": create_category.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert (
        resp["Location"]
        == "/accounts/login/?next=/adminauction/delete_category_done/1/"
    )


@pytest.mark.django_db()
def test_deletesubcategory(create_subcategory):
    resp = client.get(
        reverse(
            "adminauction:delete_subcategory",
            kwargs={"pk": create_subcategory.id},
        ),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert (
        resp["Location"] == "/accounts/login/?next=/adminauction/delete_subcategory/1/"
    )


@pytest.mark.django_db()
def test_deletesubcategorydone(create_subcategory):
    resp = client.get(
        reverse(
            "adminauction:delete_subcategory_done",
            kwargs={"pk": create_subcategory.id},
        ),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert (
        resp["Location"]
        == "/accounts/login/?next=/adminauction/delete_subcategory_done/1/"
    )


@pytest.mark.django_db()
def test_deleteuser(create_user):
    resp = client.get(
        reverse("adminauction:delete_user", kwargs={"pk": create_user.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/delete_user/2"


@pytest.mark.django_db()
def test_deleteuserdone(create_user):
    resp = client.get(
        reverse("adminauction:delete_user_done", kwargs={"pk": create_user.id}),
    )
    assert http_client.OK, resp.status_code
    assert resp.status_code == 302  # noqa:PLR2004
    assert resp["Location"] == "/accounts/login/?next=/adminauction/delete_user_done/2"


@pytest.mark.django_db()
def test_deletearticle(create_article):
    resp = client.get(
        reverse("adminauction:delete_article", kwargs={"slug": create_article.slug}),
    )
    assert http_client.OK, resp.status_code
    assert (
        resp["Location"]
        == "/accounts/login/?next=/adminauction/delete_article/article-test"
    )


@pytest.mark.django_db()
def test_deletearticledone(create_article):
    resp = client.get(
        reverse(
            "adminauction:delete_article_done",
            kwargs={"slug": create_article.slug},
        ),
    )
    assert http_client.OK, resp.status_code
    assert (
        resp["Location"]
        == "/accounts/login/?next=/adminauction/delete_article_done/article-test"
    )


@pytest.mark.django_db()
def test_bidshistory(create_bidshistory):
    resp = client.get(reverse("adminauction:bids_history"))
    assert http_client.OK, resp.status_code
    assert resp["Location"] == "/accounts/login/?next=/adminauction/bids_history"
