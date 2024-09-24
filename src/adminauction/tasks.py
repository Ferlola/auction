from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from config.celery_app import app
from src.articles.models import get_logo
from src.articles.models import show_logo
from src.users.models import superuser
from src.winner.models import get_days


@app.task(name="tasks.send_weekly_report")
def send_weekly_report():
    from_email = superuser()
    to_email = superuser()
    logo = get_logo()
    subject = "News weekly articles"
    template = get_template("adminauction/mails/weekly_report.html")
    content = template.render(
        {
            "new_articles": get_days(7)[0],
            "paid_articles": get_days(7)[1],
            "logo": logo,
        },
    )

    message = EmailMultiAlternatives(
        subject,
        "Weekly report",
        from_email,
        [to_email],
    )

    message.mixed_subtype = "related"
    message.attach_alternative(content, "text/html")
    message.attach(show_logo(logo))
    message.send()


@app.task(name="tasks.send_daily_report")
def send_daily_report():
    from_email = superuser()
    to_email = superuser()
    logo = get_logo()
    subject = "News daily report"
    template = get_template("adminauction/mails/daily_report.html")
    content = template.render(
        {
            "new_articles": get_days(1)[0],
            "paid_articles": get_days(1)[1],
            "logo": logo,
        },
    )

    message = EmailMultiAlternatives(
        subject,
        "Daily report",
        from_email,
        [to_email],
    )

    message.mixed_subtype = "related"
    message.attach_alternative(content, "text/html")
    message.attach(show_logo(logo))
    message.send()
