from django.contrib.auth import get_user_model
from django.templatetags.static import static


def show_badges(request):
    user_badges = ""
    if (
        get_user_model()
        .objects.filter(username=request.user)
        .filter(login_amount__gte=5)
    ):
        user_badges = static("img/badges/badge1.png")

    if (
        get_user_model()
        .objects.filter(username=request.user)
        .filter(login_amount__gte=10)
    ):
        user_badges = static("img/badges/badge2.png")

    if (
        get_user_model()
        .objects.filter(username=request.user)
        .filter(login_amount__gte=15)
    ):
        user_badges = static("img/badges/medal2.png")

    else:
        pass
    has_bids = static("img/badges/badge3.png")
    has_article = static("img/badges/badge14.png")
    has_won_auction = static("img/badges/medal1.png")
    return {
        "user_badges": user_badges,
        "has_bids": has_bids,
        "has_article": has_article,
        "has_paid_badge": has_won_auction,
    }
