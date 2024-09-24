from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.adminauction.models import FeeArticle
from src.articles.models import Article
from src.bids.models import BidsHistory
from src.categories.models import Category
from src.winner.models import CheckoutDone


def bids_history(request):
    user_history = BidsHistory.objects.filter(user_id=request.user.id)
    num_articles = Article.objects.all().count()
    categories = Category.objects.annotate(items_count=Count("article"))
    title = "Bids History"
    return render(
        request,
        "bids/history.html",
        {
            "user_history": user_history,
            "categories": categories,
            "num_articles": num_articles,
            "title": title,
        },
    )


def invoice_pdf(request, article_pdf):
    checkout_data = CheckoutDone.objects.filter(article=article_pdf).values(
        "user",
        "bid",
        "has_paid",
        "created_at",
        "id",
        "paid_on",
    )
    for data in checkout_data:
        data["user"]
        data["bid"]
        data["has_paid"]
        data["created_at"]
        data["id"]
        data["paid_on"]

    fee = FeeArticle.objects.values_list("fee", flat=True)
    user = (
        get_user_model()
        .objects.filter(id=data["user"])
        .values_list("username", flat=True)
    )
    bids = str(data["bid"])
    fee = str(fee)
    fee = fee[20:-5]
    total = str(((float(fee) * float(bids)) / 100) + float(bids))
    user = str(user)[12:-3]
    has_paid = str(data["has_paid"])
    created = str(data["created_at"])[2:-16]
    created = created.replace(",", "/", 2)
    created = created.replace(",", "   Time ", 1)
    created = created.replace(",", ":", 2)
    paid_on = str(data["paid_on"])[2:-16]
    paid_on = paid_on.replace(",", "/", 2)
    paid_on = paid_on.replace(",", "   Time ", 1)
    paid_on = paid_on.replace(",", ":", 2)
    response = HttpResponse(content_type="application/pdf")
    my_canvas = canvas.Canvas(response, pagesize=letter)
    my_canvas.setFillColorRGB(0.4, 0.6, 0.8)
    my_canvas.setLineWidth(0.3)
    my_canvas.setFont("Helvetica", 22)
    my_canvas.drawString(250, 720, "INVOICE")
    my_canvas.line(30, 666, 30, 505)
    my_canvas.line(580, 666, 580, 505)
    my_canvas.setFont("Helvetica", 12)
    my_canvas.line(30, 666, 580, 666)
    my_canvas.drawString(40, 650, "Client:")
    my_canvas.drawString(500, 650, user)
    my_canvas.line(30, 645, 580, 645)
    my_canvas.drawString(40, 630, "Created:")
    my_canvas.drawString(470, 630, created)
    my_canvas.line(30, 625, 580, 625)
    my_canvas.drawString(40, 610, "Article")
    my_canvas.drawString(500, 610, article_pdf)
    my_canvas.line(30, 605, 580, 605)
    my_canvas.drawString(40, 590, "Bids:")
    my_canvas.drawString(500, 590, bids + " €")
    my_canvas.line(30, 585, 580, 585)
    my_canvas.drawString(40, 570, "Fee:")
    my_canvas.drawString(500, 570, fee + "  %")
    my_canvas.line(30, 565, 580, 565)
    my_canvas.drawString(40, 550, "Total:")
    my_canvas.drawString(500, 550, total + " €")
    my_canvas.line(30, 545, 580, 545)
    my_canvas.drawString(40, 530, "Has paid:")
    my_canvas.drawString(500, 530, has_paid)
    my_canvas.line(30, 525, 580, 525)
    my_canvas.drawString(40, 510, "Paid on:")
    my_canvas.drawString(470, 510, paid_on)
    my_canvas.line(30, 505, 580, 505)
    my_canvas.save()
    return response
