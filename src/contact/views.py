from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import loader

from src.articles.models import Article
from src.categories.models import Subcategory
from src.contact.forms import AskSellerForm
from src.contact.forms import ContactForm


def contact(request):
    categories = Subcategory.objects.all()
    user = request.user
    category = ""
    message = ""

    superuser_email = (
        get_user_model()
        .objects.filter(is_superuser=True)
        .values_list("email", flat=True)
    )
    superuser_email = str(superuser_email)[12:-3]

    user_email = (
        get_user_model()
        .objects.filter(username=request.user)
        .values_list("email", flat=True)
    )
    user_email = str(user_email)[12:-3]

    form_class = ContactForm
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            user = request.user
            user = str(user)
            category = request.POST.get("category", "")
            message = request.POST.get("message", "")
            html_message = loader.render_to_string(
                "contact/mails/contact.html",
                {
                    "user": user,
                    "message": message,
                    "category": category,
                },
            )

            send_mail(
                category,
                message,
                user_email,
                [superuser_email],
                html_message=html_message,
            )
            messages.success(request, "Mail sent successfully")

            return render(
                request,
                "contact/contact.html",
                {
                    "form": form,
                    "user": user,
                    "categories": categories,
                    "title": "Contact form",
                },
            )

        context = {"form": form, "user": user, "categories": categories}
        return render(request, "contact/contact.html", context)

    categories = Subcategory.objects.all()

    return render(
        request,
        "contact/contact.html",
        {
            "form": form_class,
            "user": user,
            "categories": categories,
            "title": "Contact form",
        },
    )


def ask_seller(request, article):
    user = request.user
    user = str(user)
    message = ""
    article_user_id = Article.objects.filter(article=article).values_list(
        "user",
        flat=True,
    )

    email_article = (
        get_user_model().objects.filter(id__in=article_user_id).values_list("email")
    )
    email_article = str(email_article)[13:-5]

    user_email = get_user_model().objects.filter(username=user).values_list("email")
    user_email = str(user_email)[13:-5]

    form_class = AskSellerForm
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            message = request.POST.get("message", "")
            html_message = loader.render_to_string(
                "contact/mails/ask.html",
                {
                    "user": user,
                    "message": message,
                    "article": article,
                },
            )

            send_mail(
                "Bidder question ",
                message,
                user_email,
                [email_article],
                html_message=html_message,
            )
            messages.success(request, "Mail sent successfully")
            return render(
                request,
                "contact/ask_seller.html",
                {
                    "article": article,
                    "user": user,
                    "title": "Ask the seller",
                },
            )

        context = {"form": form, "article": article, "user": user}
        return render(request, "contact/ask_seller.html", context)

    return render(
        request,
        "contact/ask_seller.html",
        {
            "form": form_class,
            "article": article,
            "user": user,
            "title": "Ask the seller",
        },
    )
