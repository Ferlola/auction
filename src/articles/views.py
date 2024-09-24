import json
import threading
from pathlib import Path
from textwrap import wrap

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.db.models import Max
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.edit import FormMixin
from meta.views import MetadataMixin
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission
from src.articles.forms import AuctionForm
from src.articles.forms import UploadImageForm
from src.articles.mails import new_article_to_publish
from src.articles.mails import no_bids
from src.articles.models import Article
from src.articles.models import ImageUpload
from src.bids.forms import BidForm
from src.bids.mails import send_bid_information
from src.bids.mails import send_confirmation_bider
from src.bids.mails import send_info_bid_user_article
from src.bids.models import BidsHistory
from src.bids.models import BidsWinner
from src.categories.models import Category
from src.categories.models import Subcategory
from src.winner.views import get_winner


def get_subcategory(request):
    subcategory_id = request.GET.get("category")
    subcategory = Subcategory.objects.filter(category=subcategory_id).order_by("id")
    return render(request, "articles/snippets/data.html", {"subcategory": subcategory})


@login_required(login_url="account_login")
def create_article(request):
    countcategory = Category.objects.all().count()
    if countcategory == 0:
        messages.error(request, "Please add categories")
        return redirect("index")
    countsubcategory = Subcategory.objects.all().count()
    if countsubcategory == 0:
        messages.error(request, "Please add subcategories")
        return redirect("index")

    user = request.user
    num_articles = Article.objects.all().count()
    categories = Category.objects.annotate(items_count=Count("article"))
    if request.method == "POST":
        imageform = UploadImageForm(request.POST, request.FILES)
        articleform = AuctionForm(request.POST)

        if articleform.is_valid() and imageform.is_valid():
            article = articleform.save(commit=False)
            article.user = request.user
            if not article.category:
                for catego in Subcategory.objects.all():
                    if article.subcategory == catego:
                        article.category = catego.category

            article.save()
            SetBidArticle.objects.create(
                name=article.article,
                id_id=article.id,
                created=timezone.now(),
                category=article.category,
                subcategory=article.subcategory,
            )
            image = imageform.save(commit=False)
            image.article = article
            image.save()

            thread = threading.Thread(
                target=new_article_to_publish,
                args=(article.article,),
            )
            thread.start()
            return render(
                request,
                "articles/create_article.html",
                {
                    "categories": categories,
                    "num_articles": num_articles,
                },
            )
        """ else:
            print(AuctionForm.errors, UploadImageForm.errors) """
    else:
        imageform = UploadImageForm()
        articleform = AuctionForm()

    return render(
        request,
        "articles/post_article.html",
        {
            "imageForm": imageform,
            "articleForm": articleform,
            "user": user,
            "UploadImageForm": UploadImageForm,
            "categories": categories,
            "num_articles": num_articles,
            "title": "Post article",
        },
    )


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    paginate_by = 8

    def get_object(self):
        return Article.objects.get(id=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Article.objects.all().count() == 0:
            context["message"] = "empty"
        else:
            context["message"] = "Articles list"
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context["categories"] = Category.objects.annotate(items_count=Count("article"))
        context["title"] = "Articles List"
        context["time_now"] = timezone.now()
        context["article"] = Article.objects.all()
        context["day"] = timezone.localtime(timezone.now()).date()
        context["setbidarticle"] = SetBidArticle.objects.values("id")
        context["no_bids"] = no_bids()
        return context


def get_like(request):
    if request.POST.get("action") == "post":
        flag = None
        articleid = int(request.POST.get("article_id"))
        article_obj = get_object_or_404(Article, id=articleid)

        if article_obj.dislikes.filter(id=request.user.id).exists():
            article_obj.dislikes.remove(request.user)
            article_obj.save()
            flag = False

        article_obj.likes.add(request.user)
        article_obj.save()
        flag = True
        return JsonResponse(
            {
                "total_likes": article_obj.total_likes,
                "flag": flag,
                "total_dislikes": article_obj.total_dislikes,
            },
        )
    return HttpResponse("Error access denied")


def get_dislike(request):
    if request.POST.get("action") == "post1":
        flag1 = None
        articleid = int(request.POST.get("article_id"))
        article_obj1 = get_object_or_404(Article, id=articleid)

        if article_obj1.likes.filter(id=request.user.id).exists():
            article_obj1.likes.remove(request.user)
            article_obj1.save()
            flag1 = False

        article_obj1.dislikes.add(request.user)
        article_obj1.save()
        flag1 = True
        return JsonResponse(
            {
                "total_dislikes": article_obj1.total_dislikes,
                "flag1": flag1,
                "total_likes": article_obj1.total_likes,
            },
        )
    return HttpResponse("Error access denied")


class ArticleDetailView(MetadataMixin, FormMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    form_class = BidForm

    def get_meta_description(self, context=None):
        return super().get_meta_description(context)

    def get_meta_title(self, context=None):
        return super().get_meta_title(context)

    def get_success_url(self):
        return reverse("articles:article", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context["categories"] = Category.objects.annotate(items_count=Count("article"))
        context["message"] = "Article detail"
        context["title"] = context["object"]
        context["count"] = BidsHistory.objects.filter(article=context["object"]).count()
        context["actualBid"] = BidsHistory.objects.filter(
            article=context["object"],
        ).aggregate(Max("bids"))
        context["date_time"] = self.object.date_time
        context["day"] = timezone.localtime(timezone.now()).date()
        context["get_winner"] = get_winner()
        context["form"] = self.get_form()
        return context

    @method_decorator(login_required)
    def post(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        user = request.user
        if form.is_valid():
            bidss = form.save(commit=False)
            bidss.article = Article.objects.get(slug=slug)
            bidss.user = user
            args = (bidss.bids, bidss.article, bidss.user)

            if BidsHistory.objects.filter(article=bidss.article).exists():
                actualbid = BidsHistory.objects.filter(article=bidss.article).aggregate(
                    Max("bids"),
                )

                actualbid = list(actualbid.values())
                actualbid = str(actualbid).replace("[", "").replace("]", "")

                if bidss.bids <= int(actualbid):
                    messages.error(self.request, "No enough bid")
                    return self.form_invalid(form)

                bidss.save()
                messages.success(self.request, "Bid done")

                thread1 = threading.Thread(target=send_bid_information, args=args)
                thread1.start()
                thread2 = threading.Thread(target=send_info_bid_user_article, args=args)
                thread2.start()
                thread3 = threading.Thread(target=send_confirmation_bider, args=args)
                thread3.start()

                if BidsWinner.objects.filter(article=bidss.article).exists():
                    article_bid = BidsWinner.objects.get(article=bidss.article)
                    article_bid.bids = bidss.bids
                    article_bid.user = bidss.user
                    article_bid.save()

                else:
                    article_bid = BidsWinner.objects.create(
                        user=user,
                        article=bidss.article,
                        bids=bidss,
                    )

                return HttpResponseRedirect(self.get_success_url())

            if bidss.bids <= 0:
                messages.error(self.request, "No enough bid")
            else:
                thread4 = threading.Thread(target=send_info_bid_user_article, args=args)
                thread4.start()
                thread5 = threading.Thread(target=send_confirmation_bider, args=args)
                thread5.start()
                bidss.save()
                messages.success(self.request, "Bid done")
                if not BidsWinner.objects.filter(article=bidss.article).exists():
                    article_bid = BidsWinner.objects.create(
                        user=user,
                        article=bidss.article,
                        bids=bidss.bids,
                    )
                return HttpResponseRedirect(self.get_success_url())
        return None


@login_required(login_url="account_login")
def setted_bids(request, slug):
    total_amount = 0
    article = Article.objects.filter(slug=slug).values("id")
    bids = (
        BidsHistory.objects.filter(article__in=article)
        .values("bids")
        .aggregate(Max("bids"))
    )

    bids = str(bids)[14:-1]
    amount_article = SetBidArticle.objects.filter(id__in=article).values("bid_amount")

    amount_article = str(amount_article)[26:-3]

    if amount_article != "None":
        total_amount += int(amount_article)

    total = total_amount if bids == "None" else int(bids) + total_amount

    if not BidsWinner.objects.filter(article__in=article).exists():
        BidsWinner.objects.create(
            user=request.user,  # type: ignore[misc]
            article=article,
            bids=total,
        )
    else:
        article_bid = BidsWinner.objects.get(article__in=article)
        article_bid.bids = total
        article_bid.user = request.user
        article_bid.save()
    bids = total
    bidss, article, user = (
        bids,
        str(Article.objects.filter(slug=slug).values_list("article", flat=True))[12:-3],
        request.user,
    )

    thread1 = threading.Thread(target=send_bid_information, args=(bidss, article, user))
    thread1.start()
    thread2 = threading.Thread(
        target=send_info_bid_user_article,
        args=(bidss, article, user),
    )
    thread2.start()
    thread3 = threading.Thread(
        target=send_confirmation_bider,
        args=(bidss, article, user),
    )
    thread3.start()
    messages.success(request, "Bid done")
    return redirect("articles:article", slug=slug)


def date_time(request, pk):
    date_time = Article.objects.filter(pk=pk).values("date_time")
    return json.dumps(date_time)


def download_article(request, pk):
    article = Article.objects.get(id=pk)
    images = ImageUpload.objects.filter(article=article.id).values_list(
        "image",
        flat=True,
    )
    response = HttpResponse(content_type="application/pdf")
    my_canvas = canvas.Canvas(response, pagesize=letter)
    my_canvas.setTitle(article.article + ".pdf")
    textobject = my_canvas.beginText()
    textobject.setFont("Helvetica", 12)
    textobject.setTextOrigin(40, 700)
    my_canvas.drawString(30, 770, "Article:")
    my_canvas.setFont("Helvetica", 16)
    my_canvas.setFillColor(colors.blue)
    my_canvas.drawString(40, 750, article.article)
    my_canvas.setFont("Helvetica", 12)
    my_canvas.setFillColor(colors.black)
    my_canvas.drawString(30, 720, "Description:")
    wraped_text = "\n".join(wrap(article.description, width=70))
    textobject.setFillColor(colors.blue)
    textobject.setFont("Helvetica", 16)
    textobject.textLines(wraped_text)
    total_images = len(images)
    if len(images) > 1:
        images2 = images[0:1]
        images2 = str(images2)[9:-2]
        image_path = "src/media/images/" + images2
        my_canvas.drawImage(image_path, 0, 0)
        my_canvas.drawText(textobject)
        my_canvas.showPage()
        for image in images[1:total_images]:
            image_path1 = "src/media/" + image
            my_canvas.drawImage(image_path1, 0, 0)
            my_canvas.showPage()
    else:
        images1 = images
        images1 = str(images1)[12:-3]
        image_path = "src/media/" + images1
        my_canvas.drawImage(image_path, 0, 0)
        my_canvas.drawText(textobject)
        my_canvas.showPage()
    my_canvas.save()
    return response


def show(request):
    images = ImageUpload.objects.all()
    return render(request, "articles/snippets/info.html", {"images": images})


class ArticlesSearchView(ListView):
    template_name = "articles/search.html"

    def get_queryset(self):
        filters = (
            Q(article__icontains=self.query())
            | Q(category__name__icontains=self.query())
            | Q(subcategory__name__icontains=self.query())
        )
        return Article.objects.filter(filters)

    def query(self):
        return self.request.GET.get("q")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context["categories"] = Category.objects.annotate(items_count=Count("article"))
        context["query"] = self.query()
        context["count"] = context["article_list"].count()
        context["message"] = context["query"]
        context["title"] = self.query()
        context["time_now"] = timezone.now()
        context["day"] = timezone.localtime(timezone.now()).date()
        return context


class UpdateArticleView(LoginRequiredMixin, FormMixin, ListView):
    login_url = "account_login"
    model = Article
    form_class = UploadImageForm
    template_name = "articles/list_article.html"

    def get_success_url(self):
        return reverse("articles:list")

    def get_queryset(self):
        today = timezone.now()
        return Article.objects.filter(user=self.request.user, date_time__gte=today)  # type: ignore[misc]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context["categories"] = Category.objects.annotate(items_count=Count("article"))
        context["message"] = "Articles list"
        context["title"] = "Articles List"
        context["userpermission"] = UserPermission.objects.all()
        context["user"] = self.request.user
        return context


class UpdateDetailArticle(LoginRequiredMixin, FormMixin, DetailView):
    login_url = "account_login"
    model = Article
    form_class = UploadImageForm
    template_name = "articles/update_user_article.html"

    def get_success_url(self):
        return reverse("articles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context["categories"] = Category.objects.annotate(items_count=Count("article"))
        context["message"] = "Article detail"
        context["userpermission"] = UserPermission.objects.all()
        context["images"] = ImageUpload.objects.filter(article=context["object"])
        context["title"] = context["object"]
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            image = form.save(commit=False)
            image.article = self.object
            image.save()
            messages.success(self.request, "Image uploaded")
            return HttpResponseRedirect(self.get_success_url())

        messages.error(self.request, "An error has occurred, try again")
        return None


class UpdateArticle(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "account_login"
    model = Article
    form_class = AuctionForm
    template_name = "articles/update_article.html"
    success_message = "Updated article"

    def get_success_url(self):
        return reverse("articles:article", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context["categories"] = Category.objects.annotate(items_count=Count("article"))
        return context


@login_required(login_url="account_login")
def deleteimage(request, pk):
    image = ImageUpload.objects.get(id=pk)
    if ImageUpload.objects.values("image").exists():
        Path(image.image.path).unlink()
    image.delete()
    messages.success(request, "Image Deleted Successfuly")
    return redirect("articles:list")
