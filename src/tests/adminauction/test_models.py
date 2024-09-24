import pytest

from src.adminauction.models import FeeArticle
from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission


@pytest.mark.django_db()
def test_feearticle(update_feearticle):
    assert isinstance(update_feearticle, FeeArticle)


@pytest.mark.django_db()
def test_userpermission(update_userpermisions):
    assert isinstance(update_userpermisions, UserPermission)


@pytest.mark.django_db()
def test_setbiarticle(create_setbidarticle):
    assert isinstance(create_setbidarticle, SetBidArticle)


@pytest.mark.django_db()
def test_model_setbidarticle(
    create_setbidarticle,
    create_article,
    create_category,
    create_subcategory,
):
    assert create_setbidarticle.name == create_article
    assert create_setbidarticle.set_bid == "1"
    assert create_setbidarticle.bid_amount == 10  # noqa:PLR2004
    assert create_setbidarticle.publish == False  # noqa:E712
    assert create_setbidarticle.category == create_category
    assert create_setbidarticle.subcategory == create_subcategory


@pytest.mark.django_db()
def test_model_feearticle(update_feearticle):
    assert update_feearticle.fee == 5.0  # noqa:PLR2004


@pytest.mark.django_db()
def test_model_userpermisions(update_userpermisions):
    assert update_userpermisions.article_update == False  # noqa:E712
    assert update_userpermisions.choose_date_time == False  # noqa:E712
    assert update_userpermisions.total_images == 3  # noqa:PLR2004
    assert update_userpermisions.theme == "D"
    assert update_userpermisions.site_name == "Auction site"
