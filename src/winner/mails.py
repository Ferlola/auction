from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from src.articles.models import Article
from src.articles.models import get_article_id
from src.articles.models import get_image
from src.articles.models import get_logo
from src.articles.models import show_image
from src.articles.models import show_logo
from src.users.models import superuser


def send_winner(bid, article, user_id, email, slug):
    if Article.objects.filter(slug=slug).filter(notification_winner=True):
        user = (
            get_user_model()
            .objects.filter(id=user_id)
            .values_list("username", flat=True)
        )
        username = str(user)[12:-3]

        article_id = get_article_id(article)
        logo = get_logo()

        subject = "Winner Confirmation"
        template = get_template("winner/mails/winner_confirmation.html")
        content = template.render(
            {
                "user": username,
                "bids": bid,
                "article": article,
                "image": get_image(article_id),
                "logo": logo,
            },
        )

        message = EmailMultiAlternatives(
            subject,
            "Winner Confirmation",
            superuser(),
            [email],
        )
        message.mixed_subtype = "related"
        message.attach_alternative(content, "text/html")
        message.attach(show_image(article))
        message.attach(show_logo(logo))
        message.send()
        Article.objects.filter(slug=slug).filter(notification_winner=True).update(
            notification_winner=False,
        )
