from django.test import TestCase

from src.articles.models import Article
from src.bids.forms import BidForm
from src.bids.models import BidsHistory
from src.categories.models import Category
from src.categories.models import Subcategory
from src.users.models import User


class TestBidForm(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(
            name="test_user",
            password="test_password",  # noqa:S106
            username="test_user",
        )
        category = Category.objects.create(name="test_category")
        subcategory = Subcategory.objects.create(
            name="subcategory_test",
            category=category,
        )
        article = Article.objects.create(
            user=user,
            article="New article",
            description="New description",
            location="New location",
            category=category,
            subcategory=subcategory,
        )
        bid = BidsHistory.objects.create(
            user=user,
            article=article,
            bids=22,
        )
        data_bid = {"bids": bid.bids}
        form = BidForm(data=data_bid)
        assert form.is_valid(), form.errors
        assert isinstance(bid, BidsHistory)
        assert bid.__str__(), article.article
