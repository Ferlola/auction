import paypalrestsdk
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseNotFound
from django.http.response import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from paypalrestsdk import Payment

from src.adminauction.models import FeeArticle
from src.articles.models import Article
from src.bids.models import BidsHistory
from src.bids.models import BidsWinner
from src.users.models import User
from src.winner.mails import send_winner
from src.winner.models import CheckoutDone


def get_winner():
    """
    This function gets the winner when the auction has ended,
    send an email to the winner user and saves database CheckoutDone.

     - First it checks if any auction has ended,
     if so it saves the items id in the variable id_article.
     - Then it checks if there was any bid,
     if there was, it saves the item in the variable id_ar.
     - Then it checks if it had a reserved price and if it has been exceeded,
     if so it saves it in the variable data_bid
     - Then it gets the user, the bid, the email, the item, the slug.

    Returns:
        article(str): article name
        slug(str): article slug
        user_id(int): user id
        email(str): user email address
        bid(int): article bid

    Then it sends an email to the winner.
    Then it saves in the CheckoutDone database.
    """

    today = timezone.now()
    if Article.objects.filter(date_time__lte=today).exists():
        id_articles = Article.objects.filter(date_time__lte=today).values_list("id")

        if BidsWinner.objects.filter(article__in=id_articles).exists():
            for id_a in id_articles:
                id_ar = id_a[0]

                reserved = Article.objects.filter(id=id_ar).values_list("reserved")
                if (
                    BidsWinner.objects.filter(article=id_ar)
                    .filter(bids__gte=reserved)
                    .exists()
                ):
                    data_bid = (
                        BidsWinner.objects.filter(article=id_ar)
                        .filter(bids__gte=reserved)
                        .values("bids", "user")
                    )
                    for data1 in data_bid:
                        bid = data1["bids"]

                    data_user = (
                        get_user_model()
                        .objects.filter(id=data1["user"])
                        .values("email", "id")
                    )
                    for data2 in data_user:
                        email = data2["email"]
                        user_id = data2["id"]

                    data_article = Article.objects.filter(id=id_ar).values(
                        "article",
                        "slug",
                    )
                    for data3 in data_article:
                        article = data3["article"]
                        slug = data3["slug"]

                    send_winner(bid, article, user_id, email, slug)

                    if not CheckoutDone.objects.filter(slug=slug).exists():
                        bid_fee = FeeArticle.objects.values_list("fee", flat=True)
                        bid_fee = float(str(bid_fee)[20:-4])
                        CheckoutDone.objects.create(
                            article=article,
                            bid=bid,
                            bid_fee=bid_fee,
                            email=email,
                            user_id=user_id,
                            slug=slug,
                        )


def buy_now(request, pk):
    article = Article.objects.get(id=pk)
    user = request.user
    email = user.email
    user_id = user.id
    slug = article.slug
    bid = article.reserved
    if not CheckoutDone.objects.filter(slug=slug).exists():
        bid_fee = FeeArticle.objects.values_list("fee", flat=True)
        bid_fee = float(str(bid_fee)[20:-4])
        CheckoutDone.objects.create(
            article=article,
            bid=bid,
            bid_fee=bid_fee,
            email=email,
            user_id=user_id,
            slug=slug,
        )
    BidsHistory.objects.create(bids=bid, article_id=article.id, user=user)
    messages.success(request, "Bid done")
    send_winner(bid, article, user_id, email, slug)
    return redirect("articles:article", slug=slug)


class WinnerListView(ListView):
    model = CheckoutDone
    template_name = "winner/winner_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["created"] = CheckoutDone.objects.values("created_at")
        if isinstance(self.request.user, User):
            context["object"] = CheckoutDone.objects.filter(user=self.request.user)
        context["fee"] = FeeArticle.objects.values_list("fee", flat=True)
        return context


class WinnerDetailView(DetailView):
    model = CheckoutDone
    template_name = "winner/winner_detail.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fee"] = FeeArticle.objects.values_list("fee", flat=True)
        context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        return context


def get_fee(request):
    fee = FeeArticle.objects.values_list("fee", flat=True)
    fee = str(fee)
    fee = fee[20:-4]
    return float(fee)


####### stripe start #####
@sensitive_post_parameters()
@csrf_exempt
def create_checkout_session(request, id):  # noqa:A002
    checkout = get_object_or_404(CheckoutDone, pk=id)
    fee = get_fee(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=checkout.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": checkout.article,
                    },
                    "unit_amount": int((fee * checkout.bid) + (checkout.bid * 100)),
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("winner:success"),
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("winner:failed")),
    )

    if CheckoutDone.objects.filter(slug=checkout.slug).exists():
        ch = CheckoutDone.objects.get(slug=checkout.slug)
        ch.payment_id = checkout_session["id"]
        ch.save()

    return JsonResponse({"sessionId": checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "winner/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        checkoutdone = get_object_or_404(CheckoutDone, payment_id=session.id)
        checkoutdone.paid_on = timezone.now()
        checkoutdone.has_paid = True
        checkoutdone.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = "winner/payment_failed.html"


###### stripe end ######


###### paypal start #####

paypalrestsdk.configure(
    {
        "mode": "sandbox",
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_SECRET_ID,
    },
)


@sensitive_post_parameters()
def checkout(request, id):  # noqa:A002
    fee = get_fee(request)
    checkout = get_object_or_404(CheckoutDone, pk=id)

    payment = Payment(
        {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(
                    reverse("winner:execute_payment", kwargs={"id": id}),
                ),
                "cancel_url": "http://localhost:8000/winner/failed/",
            },
            "transactions": [
                {
                    "item_list": {
                        "items": [
                            {
                                "name": checkout.article,
                                "sku": "Article",
                                "price": ((fee * checkout.bid) / 100 + (checkout.bid)),
                                "currency": "EUR",
                                "quantity": 1,
                            },
                        ],
                    },
                    "amount": {
                        "total": ((fee * checkout.bid) / 100 + (checkout.bid)),
                        "currency": "EUR",
                    },
                    "description": "Descripcion del Pago",
                },
            ],
        },
    )

    if payment.create():
        for link in payment.links:  # noqa:RET503
            if link.rel == "approval_url":
                aproval_url = link.href
                return HttpResponseRedirect(aproval_url)
    else:
        return payment.error


@sensitive_post_parameters()
def execute_payment(request, pk):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        checkout = get_object_or_404(CheckoutDone, pk=pk)
        if CheckoutDone.objects.filter(slug=checkout.slug).exists():
            ch = CheckoutDone.objects.get(slug=checkout.slug)
            ch.paid_on = timezone.now()
            ch.has_paid = True
            ch.payment_id = payment["id"]
            ch.save()
        return render(request, "winner/succcess_payment.html")
    return render(request, "winner/payment_failed.html")


class SucccessPayment(TemplateView):
    template_name = "winner/succcess_payment.html"
