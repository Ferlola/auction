import pytest

from src.winner.models import CheckoutDone


@pytest.mark.django_db()
def test_checkoutdone(create_checkout, create_user, create_article, create_bidswinner):
    assert create_checkout.user == create_user
    assert create_checkout.article == create_article.article
    assert create_checkout.bid == create_bidswinner.bids
    assert create_checkout.bid_fee == 0
    assert create_checkout.email == create_user.email
    assert create_checkout.payment_id == ""
    assert create_checkout.has_paid == False  # noqa:E712
    assert create_checkout.slug == create_article.slug
    assert create_checkout.paid_on == ""


@pytest.mark.django_db()
def test_create_checkout(create_checkout):
    assert isinstance(create_checkout, CheckoutDone)
