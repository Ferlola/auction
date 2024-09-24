from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from src.articles.models import Article
from src.articles.models import get_article_id
from src.articles.models import get_image
from src.articles.models import get_logo
from src.articles.models import show_image
from src.articles.models import show_logo
from src.users.models import Unsubscribe
from src.users.models import superuser


# @staticmethod
def get_absolute_url(url):
    if settings.DEBUG:
        return f"http://127.0.0.1:8000{reverse(url)}"
    return None


def no_bids():
    """
    This function gets the articles without any bid,
    and the user of the article

     - This function gets the article id from the get_article_id function

    Returns:
        username(str): the user of the article
        email(str): the user email of the article

    Finally send an email to the user
    """

    today = timezone.now()
    articles_no_bids = Article.objects.filter(
        bidshistory__isnull=True,
        date_time__lte=today,
    ).values_list("article", flat=True)

    for article in articles_no_bids:
        user_id = Article.objects.filter(article=article).select_related("user")

        for data in user_id:
            username = data.user.username
            email = data.user.email

        if Article.objects.filter(article=article).filter(notification_no_bid=True):
            subject = "Your article has not had any bidders"
            template = get_template("articles/mails/finished_no_bid.html")
            article_id = get_article_id(article)
            logo = get_logo()

            content = template.render(
                {
                    "user": username,
                    "article": article,
                    "image": get_image(article_id),
                    "logo": logo,
                },
            )

            message = EmailMultiAlternatives(
                subject,
                "No bids",
                superuser(),
                [email],
            )

            message.mixed_subtype = "related"
            message.attach_alternative(content, "text/html")
            message.attach(show_image(article))
            message.attach(show_logo(logo))
            message.send()
            Article.objects.filter(article=article).filter(
                notification_no_bid=True,
            ).update(notification_no_bid=False)


def info_new_article(article):
    """
    This function gets new items for auction

    - first gets all registered users
    - then excludes the user from the item and users unsubscribed from newsletter

    Returns:
    user(str): user name
    email(str): user email

    - then sends an email to the users
    """

    user_id = Article.objects.filter(article=article).values_list("user")
    category_id = Article.objects.filter(article=article).select_related("category")

    for data in category_id:
        category = data.category.name

    get_users = (
        get_user_model()
        .objects.values_list("username", "email")
        .exclude(id__in=user_id)
        .exclude(id__in=Unsubscribe.objects.all())
        .order_by("id")
    )

    for data1 in get_users:
        username = data1[0]
        email = data1[1]
        subject = "New article auction"
        template = get_template("articles/mails/new_article.html")
        article_id = get_article_id(article)
        logo = get_logo()
        content = template.render(
            {
                "user": username,
                "article": article,
                "category": category,
                "image": get_image(article_id),
                "logo": logo,
                "next_url": get_absolute_url("users:unsubscribe"),
            },
        )

        message = EmailMultiAlternatives(
            subject,
            "New article",
            superuser(),
            [email],
        )

        message.mixed_subtype = "related"
        message.attach_alternative(content, "text/html")
        message.attach(show_image(article))
        message.attach(show_logo(logo))
        message.send()


def new_article_to_publish(article):
    """
    This function sends the site admin an email to notify
    that there is a new article to review and publish.
    """

    subject = "New article to review"
    template = get_template("articles/mails/to_publish.html")
    content = template.render(
        {
            "article": article,
        },
    )

    message = EmailMultiAlternatives(
        subject,
        "New article",
        superuser(),
        [superuser()],
    )

    message.attach_alternative(content, "text/html")
    message.send()
