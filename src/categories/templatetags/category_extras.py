from django import template

from src.articles.models import Article
from src.categories.models import Category
from src.categories.models import Subcategory

register = template.Library()


@register.filter()
def countsubcategory(value):
    value = Subcategory.objects.filter(name=value).values_list("id", flat=True)
    return Article.objects.filter(subcategory__in=value, publish=True).count()


@register.filter()
def countcategory(value):
    value = Category.objects.filter(name=value).values_list("id", flat=True)
    return Article.objects.filter(category__in=value, publish=True).count()
