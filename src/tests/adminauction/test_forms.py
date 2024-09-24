from django.test import TestCase

from src.adminauction.forms import CategoryForm
from src.adminauction.forms import FeeForm
from src.adminauction.forms import PermissionForm
from src.adminauction.forms import SetBidarticleForm
from src.adminauction.forms import SubcategoryForm
from src.adminauction.models import FeeArticle
from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission
from src.articles.models import Article
from src.categories.models import Category
from src.categories.models import Subcategory
from src.users.models import User


class TestCategoryForm(TestCase):
    def test_valid_form(self):
        category = Category.objects.create(name="category_test")
        data = {"name": category.name}
        form = CategoryForm(data=data)
        form.save()
        assert form.is_valid()
        assert form.cleaned_data
        assert isinstance(category, Category)
        assert category.__str__(), category.name


class TestSubcategoryForm(TestCase):
    def test_valid_form(self):
        category = Category.objects.create(name="category_test")
        subcategory = Subcategory.objects.create(
            name="subcategory_test",
            category=category,
        )
        data = {"name": subcategory.name, "category": subcategory.category}
        form = SubcategoryForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data
        assert isinstance(subcategory, Subcategory)
        assert subcategory.__str__(), subcategory.name


class TestFeeForm(TestCase):
    def test_valid_form(self):
        feearticle = FeeArticle.objects.create(fee=10.0)
        data = {"fee": feearticle}
        form = FeeForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data
        assert isinstance(feearticle, FeeArticle)
        assert feearticle.__str__(), str(feearticle.fee)


class TestSetBidarticleForm(TestCase):
    def test_valid_form(self):
        user = User.objects.create(
            name="user_test",
            email="user@example",
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

        setbidarticle = SetBidArticle.objects.create(
            name="test_article",
            id=article,
            set_bid="1",
            bid_amount=15,
            publish=False,
            category="category_test",
            subcategory="subcategory_test",
        )

        data = {
            "name": setbidarticle.name,
            "id": setbidarticle.id,
            "set_bid": setbidarticle.set_bid,
            "bid_amount": setbidarticle.bid_amount,
            "publish": setbidarticle.publish,
            "category": setbidarticle.category,
            "subcategory": setbidarticle.subcategory,
        }
        form = SetBidarticleForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data
        assert isinstance(setbidarticle, SetBidArticle)
        assert setbidarticle.__str__(), str(setbidarticle.name)


class TestUserPermisionForm(TestCase):
    def test_valid_form(self):
        userpermision = UserPermission.objects.create(
            article_update=False,
            choose_date_time=False,
            total_images=5,
            theme="D",
            site_name="Auction",
            domain="www.auction.com",
        )

        data = {
            "article_update": userpermision.article_update,
            "choose_date_time": userpermision.choose_date_time,
            "total_images": userpermision.total_images,
            "theme": userpermision.theme,
            "site_name": userpermision.site_name,
            "domain": userpermision.domain,
        }

        form = PermissionForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data
        assert isinstance(userpermision, UserPermission)
        assert userpermision.__str__(), userpermision.site_name
