from django.db import models


class SetBidArticle(models.Model):
    BID_CHOICES = [
        ("1", "Bidder increment"),
        ("2", "Auto increment"),
    ]
    name = models.CharField(max_length=50)
    id = models.OneToOneField(
        "articles.Article",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    set_bid = models.CharField(max_length=1, choices=BID_CHOICES, blank=True)

    bid_amount = models.IntegerField(null=True, blank=True)
    publish = models.BooleanField(default=False)
    category = models.CharField(max_length=50, null=False, blank=False)
    subcategory = models.CharField(max_length=50, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    @property
    def type_bid(self):
        if self.set_bid == "2":
            return self.bid_amount
        return None


class FeeArticle(models.Model):
    fee = models.DecimalField(max_digits=4, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.fee)


class UserPermission(models.Model):
    THEME_CHOICES = (
        ("L", "Light"),
        ("D", "Dark"),
    )
    article_update = models.BooleanField()
    choose_date_time = models.BooleanField()
    total_images = models.IntegerField()
    theme = models.CharField(choices=THEME_CHOICES, max_length=5)
    created = models.DateTimeField(auto_now_add=True)
    site_name = models.CharField(max_length=20)
    domain = models.CharField(max_length=35)

    def __str__(self):
        return str(self.site_name)

    @property
    def is_update_article(self):
        return self.article_update
