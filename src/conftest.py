from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client

from src.adminauction.models import FeeArticle
from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission
from src.articles.models import Article
from src.articles.models import ImageUpload
from src.bids.models import BidsHistory
from src.bids.models import BidsWinner
from src.categories.models import Category
from src.categories.models import Subcategory
from src.tests.users.factories import UserFactory
from src.users.models import User
from src.winner.models import CheckoutDone

client = Client()


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def create_user():
    user = User.objects.create_user(
        id=2,
        name="testuser",
        username="testuser",
        email="testuserh@testuser.com",
        password="passwordtestuser",  # noqa:S106
    )
    user.save()
    return user


@pytest.fixture()
def create_category():
    return Category.objects.create(id=1, name="Newcategory")


@pytest.fixture()
def create_subcategory(create_category):
    return Subcategory.objects.create(
        id=1,
        name="Newsubcategory",
        category=create_category,
    )


@pytest.fixture()
def create_article(create_user, create_category, create_subcategory):
    return Article.objects.create(
        id=1,
        user=create_user,
        article="article_test",
        description="description_test",
        location="location_test",
        category=create_category,
        subcategory=create_subcategory,
        slug="article-test",
        from_date="2024-07-10",
        date_time=("2024-07-18T13:20:30+03:00"),
        notification_winner=True,
        notification_no_bid=True,
        publish=False,
    )


@pytest.fixture()
def create_article_url(create_category, create_subcategory):
    return {
        "article": "New article",
        "description": "New description",
        "location": "New location",
        "category": create_category,
        "subcategory": create_subcategory,
    }


@pytest.fixture()
def create_image():
    images = "src/static/images/logo.png"
    return ImageUpload.objects.create(
        id=1,
        image=SimpleUploadedFile(
            name="logo.png",
            content=Path(images).open("rb").read(),  # noqa:SIM115
            content_type="image/png",
        ),
        # article = create_article)
    )


@pytest.fixture()
def create_bidshistory(create_user, create_article):
    return BidsHistory.objects.create(
        user=create_user,
        article=create_article,
        bids=22,
        bid_date=("2024-07-19T13:20:30+03:00"),
    )


@pytest.fixture()
def create_bidswinner(create_user, create_article):
    winner = BidsWinner.objects.create(
        user=create_user,
        article=create_article,
        bids=22,
        bid_date=("2024-07-19T13:20:30+03:00"),
    )
    winner.save()
    return winner


@pytest.fixture()
def create_checkout(create_user, create_article, create_bidswinner):
    return CheckoutDone(
        id=1,
        user=create_user,
        article=create_article.article,
        bid=create_bidswinner.bids,
        bid_fee=0,
        email=create_user.email,
        payment_id="",
        has_paid=False,
        slug=create_article.slug,
        paid_on="",
    )


@pytest.fixture()
def create_login(create_user):
    return client.login(email=create_user.email, password=create_user.password)


@pytest.fixture()
def create_setbidarticle(create_article, create_category, create_subcategory):
    return SetBidArticle(
        name=create_article,
        set_bid="1",
        bid_amount=10,
        publish=False,
        category=create_category,
        subcategory=create_subcategory,
    )


@pytest.fixture()
def update_userpermisions():
    return UserPermission(
        article_update=False,
        choose_date_time=False,
        total_images=3,
        theme="D",
        site_name="Auction site",
    )


@pytest.fixture()
def update_feearticle():
    return FeeArticle(fee=5.0)
