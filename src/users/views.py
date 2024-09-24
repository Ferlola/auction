from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from src.articles.models import Article
from src.categories.models import Category
from src.users.models import Unsubscribe
from src.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def badges(request):
    less_5 = static("img/badges/badge1.png")
    less_10 = static("img/badges/badge2.png")
    less_15 = static("img/badges/medal2.png")
    has_bids = static("img/badges/badge3.png")
    has_article = static("img/badges/badge14.png")
    has_won_auction = static("img/badges/medal1.png")
    title = "Badges"

    categories = Category.objects.annotate(items_count=Count("article"))
    num_articles = Article.objects.all().count()
    return render(
        request,
        "users/badges.html",
        {
            "categories": categories,
            "num_articles": num_articles,
            "title": title,
            "has_won_auction": has_won_auction,
            "less_5": less_5,
            "less_10": less_10,
            "less_15": less_15,
            "has_article": has_article,
            "has_bids": has_bids,
        },
    )


@login_required
def unsubscribe(request):
    Unsubscribe.objects.create(
        user=get_user_model().objects.get(username=request.user),
        set_unsubscribe=True,
    )

    messages.success(request, "Unsubscribed Successfuly")
    return redirect("index")
