from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from src.articles.models import Article


class CheckoutDone(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    article = models.CharField(max_length=100, blank=False, null=False)
    bid = models.PositiveIntegerField(blank=False, null=False)
    bid_fee = models.DecimalField(max_digits=4, decimal_places=2)
    email = models.EmailField(null=False, blank=False)
    payment_id = models.CharField(max_length=200, blank=True)
    has_paid = models.BooleanField(default=False, verbose_name="Payment Status")
    slug = models.SlugField(null=False, blank=False, unique=True)
    paid_on = models.DateTimeField(auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article


def get_days(days):
    today = timezone.now()
    from_days = today - timedelta(days=days)
    new_articles = Article.objects.filter(created__gt=from_days)
    paid_articles = CheckoutDone.objects.filter(paid_on__gt=from_days)
    return new_articles, paid_articles
