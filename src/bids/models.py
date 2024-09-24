from django.contrib.auth import get_user_model
from django.db import models

from src.articles.models import Article


class BidsHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    bids = models.PositiveIntegerField(blank=False, null=False, default=1)
    bid_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "BidsHistory"
        app_label = "bids"

    def __str__(self):
        return str(self.article)


class BidsWinner(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    bids = models.PositiveIntegerField(blank=False, null=False, default=1)
    bid_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "BidsWinner"
        app_label = "bids"

    def __str__(self):
        return str(self.article)
