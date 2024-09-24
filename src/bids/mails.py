from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models import Max
from django.template.loader import get_template

from src.articles.models import Article
from src.articles.models import get_article_id
from src.articles.models import get_image
from src.articles.models import get_logo
from src.articles.models import show_image
from src.articles.models import show_logo
from src.bids.models import BidsHistory
from src.users.models import superuser


def send_bid_information(bidss, article, user):
    """
    This function gets the users who have placed a bid on the same article.

    Parameters:
    bidss(int): article bid
    article(str): article name
    user(str): user who placed the bid

     - First it gets the users who have placed a bid on the same article,
     excluding the last user who placed the bid
     - Then it gets the users emails
    Returns:
    username(str): user names
    emails(str): user emails
    bidss(int): bid placed
    article(str): article name

    Then it sends an email to the users
    """

    if BidsHistory.objects.filter(
        article__in=Article.objects.filter(article=article),
    ).values("id"):
        count = (
            BidsHistory.objects.filter(
                article__in=Article.objects.filter(article=article),
            )
            .values_list("user", flat=True)
            .order_by()
            .annotate(max_id=Max("id"))
            .exclude(user_id=user.id)
            .count()
        )

        if count == 0:
            pass
        else:
            users = (
                BidsHistory.objects.filter(
                    article__in=Article.objects.filter(article=article),
                )
                .values_list("user", flat=True)
                .order_by()
                .annotate(max_id=Max("id"))
                .exclude(user_id=user.id)
            )

            article_id = get_article_id(article)
            logo = get_logo()

            for user in users:
                emails = str(
                    get_user_model()
                    .objects.filter(id=user)
                    .values_list("email", flat=True),
                )[12:-3]

                username = (
                    get_user_model()
                    .objects.filter(id=user)
                    .values_list("username", flat=True)
                )

                subject = "A user has placed an auction bid"
                template = get_template("bids/mails/information_bid.html")
                message = EmailMultiAlternatives(
                    subject,
                    "New bid",
                    superuser(),
                    [emails],
                )

                content = template.render(
                    {
                        "user": username,
                        "bidss": bidss,
                        "article": article,
                        "image": get_image(article_id),
                        "logo": logo,
                    },
                )

                message.mixed_subtype = "related"
                message.attach_alternative(content, "text/html")
                message.attach(show_image(article))
                message.attach(show_logo(logo))
                message.send()


def send_info_bid_user_article(bidss, article, user):
    """
    This function sends an email to the user of the article
    """

    user_id = Article.objects.filter(article=article).select_related("user")

    for data in user_id:
        username = data.user.username
        email = data.user.email

    subject = "A user has placed an auction bid on your item"
    template = get_template("bids/mails/user_article_bid.html")
    message = EmailMultiAlternatives(
        subject,
        "New bid",
        superuser(),
        [email],
    )

    article_id = get_article_id(article)
    logo = get_logo()

    content = template.render(
        {
            "user": user,
            "bidss": bidss,
            "article": article,
            "user_article_name": username,
            "image": get_image(article_id),
            "logo": logo,
        },
    )

    message.mixed_subtype = "related"
    message.attach_alternative(content, "text/html")
    message.attach(show_image(article))
    message.attach(show_logo(logo))
    message.send()


def send_confirmation_bider(bidss, article, user):
    """
    This function sends an email confirming to the user that the offer is made.

    Returns:
    email(str): The email of the user

    then sends an email to the user
    """

    get_email_bider = str(
        get_user_model().objects.filter(username=user).values_list("email", flat=True),
    )[12:-3]

    subject = "Bid confirmation"
    template = get_template("bids/mails/bider_confirmation.html")
    message = EmailMultiAlternatives(
        subject,
        "Bid confirmation",
        superuser(),
        [get_email_bider],
    )

    article_id = get_article_id(article)
    logo = get_logo()

    content = template.render(
        {
            "user": user,
            "bidss": bidss,
            "article": article,
            "image": get_image(article_id),
            "logo": logo,
        },
    )

    message.mixed_subtype = "related"
    message.attach_alternative(content, "text/html")
    message.attach(show_image(article))
    message.attach(show_logo(logo))
    message.send()
