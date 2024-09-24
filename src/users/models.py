from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import OneToOneField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Cookie Auction.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    login_amount = IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def has_article(self):
        return self.article_set.filter(article__isnull=False)

    @property
    def is_winner(self):
        return self.checkoutdone_set.filter(user__isnull=False)

    @property
    def has_bids(self):
        return self.bidshistory_set.filter(user__isnull=False)

    @property
    def has_checkout(self):
        return self.checkoutdone_set.filter(user__isnull=False)

    @property
    def not_has_paid(self):
        return self.checkoutdone_set.filter(user__isnull=False).filter(has_paid=False)

    @property
    def not_paid(self):
        return (
            self.checkoutdone_set.filter(user__isnull=False)
            .filter(has_paid=False)
            .values("article", "bid")
        )

    @property
    def has_won_auction(self):
        return self.checkoutdone_set.filter(user__isnull=False)


@receiver(pre_save, sender=User)
def set_slug(sender, instance, *args, **kwargs):
    if User.objects.filter(username=instance):
        user = User.objects.get(username=instance)
        if user.login_amount is None:
            user.login_amount = 1
            User.objects.filter(username=user).update(login_amount=user.login_amount)
        else:
            user.login_amount += 1
            User.objects.filter(username=user).update(login_amount=user.login_amount)
    else:
        pass


def superuser():
    return str(User.objects.filter(is_superuser=True).values_list("email", flat=True))[
        12:-3
    ]


class Unsubscribe(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    set_unsubscribe = BooleanField(default=False)

    def __str__(self):
        return self.user
