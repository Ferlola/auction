import pytest

from src.categories.models import Category
from src.categories.models import Subcategory


@pytest.mark.django_db()
def test_category(create_category):
    assert isinstance(create_category, Category)


@pytest.mark.django_db()
def test_subcategory(create_subcategory):
    assert isinstance(create_subcategory, Subcategory)


@pytest.mark.django_db()
def test_model_category(create_category):
    assert create_category.name == "Newcategory"


@pytest.mark.django_db()
def test_model_subcategory(create_category, create_subcategory):
    assert create_subcategory.name == "Newsubcategory"
    assert create_subcategory.category == create_category
