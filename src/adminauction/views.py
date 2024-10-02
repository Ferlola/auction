import datetime
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask

from src.adminauction.forms import AuctionForm
from src.adminauction.forms import CategoryForm
from src.adminauction.forms import CrontabDailyForm
from src.adminauction.forms import CrontabWeeklyForm
from src.adminauction.forms import FeeForm
from src.adminauction.forms import PermissionForm
from src.adminauction.forms import SetBidarticleForm
from src.adminauction.forms import SubcategoryForm
from src.adminauction.models import FeeArticle
from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission
from src.articles.mails import info_new_article
from src.articles.models import Article
from src.articles.models import ImageUpload
from src.bids.models import BidsHistory
from src.categories.models import Category
from src.categories.models import Subcategory
from src.users.models import Unsubscribe
from src.winner.models import CheckoutDone


class SuperuserRequiredMixin(PermissionRequiredMixin):
    permission_required = "is_superuser"


class UpdateArticle(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "account_login"
    model = Article
    form_class = AuctionForm
    template_name = "adminauction/form_article.html"
    success_message = "Updated article"

    def get_success_url(self):
        return reverse("adminauction:update_article", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Article review"
        return context


class CategoryView(SuperuserRequiredMixin, CreateView):
    login_url = "account_login"
    form_class = CategoryForm
    model = Category
    template_name = "adminauction/create_category.html"

    def get_success_url(self):
        return reverse("adminauction:create_category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["title"] = "Create category"
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return None


class SubcategoryView(SuperuserRequiredMixin, CreateView):
    login_url = "account_login"
    form_class = SubcategoryForm
    model = Subcategory
    template_name = "adminauction/create_subcategory.html"

    def get_success_url(self):
        return reverse("adminauction:create_subcategory")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subcategory"] = Subcategory.objects.all()
        context["category"] = Category.objects.all()
        context["title"] = "Create subcategory"
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return None


class FeeView(SuperuserRequiredMixin, CreateView):
    login_url = "account_login"
    form_class = FeeForm
    model = FeeArticle
    template_name = "adminauction/fee.html"

    def get_success_url(self):
        return reverse("adminauction:fee")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fee"] = FeeArticle.objects.all()
        context["title"] = "Set fee"
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            FeeArticle.objects.all().delete()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return None


class PermissionUpdateArticle(SuperuserRequiredMixin, CreateView):
    login_url = "account_login"
    form_class = PermissionForm
    template_name = "adminauction/settings.html"

    def get_success_url(self):
        return reverse("adminauction:setting")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_now"] = timezone.now()
        if not FeeArticle.objects.exists():
            FeeArticle.objects.create(
                fee=0.00,
                created=datetime.datetime.now(tz=datetime.UTC),
            )
        if not UserPermission.objects.exists():
            UserPermission.objects.create(
                article_update=False,
                choose_date_time=False,
                total_images=3,
                theme="L",
                site_name="Auction",
                domain="auction.com",
            )
        context["userpermission"] = UserPermission.objects.all()
        context["subcategories"] = Subcategory.objects.all()
        context["articles"] = Article.objects.all().order_by("-id")
        context["images"] = ImageUpload.objects.all()
        context["not_published"] = SetBidArticle.objects.filter(
            publish=False,
        ).values_list("name", flat=True)
        context["title"] = "Settings"
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            permisions = form.save(commit=False)
            UserPermission.objects.all().delete()
            site = Site.objects.get_current()
            site.name = permisions.site_name
            site.domain = permisions.domain
            site.save()
            permisions.save()
            msg = "Saved site settingd"
            messages.success(request, msg)
            return HttpResponseRedirect(self.get_success_url())
        return None


class BidArticle(SuperuserRequiredMixin, UpdateView):
    login_url = "account_login"
    model = SetBidArticle
    form_class = SetBidarticleForm
    template_name = "adminauction/set_bid_article.html"

    def get_object(self):
        if not SetBidArticle.objects.filter(pk=self.kwargs["pk"]).exists():
            return SetBidArticle.objects.create(pk=self.kwargs["pk"])
        return SetBidArticle.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self, **kwargs):
        return reverse("adminauction:article", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.get(pk=self.kwargs["pk"])
        if SetBidArticle.objects.exists():
            context["bidarticle"] = SetBidArticle.objects.get(pk=self.kwargs["pk"])
        else:
            context["bidarticle"] = SetBidArticle.objects.create(pk=self.kwargs["pk"])
        context["title"] = "Set bid article"
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if SetBidArticle.objects.exists():
            bidarticle = SetBidArticle.objects.get(pk=self.kwargs["pk"])
        else:
            bidarticle = SetBidArticle.objects.create(pk=self.kwargs["pk"])
        form = self.get_form()
        if form.is_valid():
            bidart = form.save(commit=False)
            article = Article.objects.get(id=self.kwargs["pk"])
            bidart.id = article
            bidart.name = article.article
            bidart.category = str(article.category)
            bidart.subcategory = str(article.subcategory)
            bidart.created = timezone.now()
            if bidart.publish:
                if Article.objects.filter(
                    id=self.kwargs["pk"],
                    from_date__isnull=True,
                    date_time__isnull=True,
                ):
                    msg = "Please go to edit article and choose date time \
                        start and date time finish before publishing"
                    messages.error(request, msg)
                else:
                    bidart = form.save()
                    update_publish = Article.objects.get(id=self.kwargs["pk"])
                    update_publish.publish = True
                    update_publish.save()
                    article = bidart.name
                    info_new_article(article)
                    messages.success(request, "Article published successfully")
            else:
                bidart = form.save()
            if not bidart.publish:
                update_publish = Article.objects.get(id=self.kwargs["pk"])
                update_publish.publish = False
                update_publish.save()
                messages.success(request, "Article unpublished successfully")
            return HttpResponseRedirect(self.get_success_url())
        return render(
            request,
            "adminauction/set_bid_article.html",
            {"form": form, "bidarticle": bidarticle},
        )


class BidsHistoryView(SuperuserRequiredMixin, ListView):
    login_url = "account_login"
    model = BidsHistory
    template_name = "adminauction/bidshistory_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from src.bids.models import BidsHistory as History

        context["order_user"] = History.objects.all().order_by("user_id")
        context["title"] = "Bids history"
        context["checkout"] = CheckoutDone.objects.all()
        return context


class DeleteUnsubscribedDB(SuperuserRequiredMixin, ListView):
    login_url = "account_login"
    model = Unsubscribe
    template_name = "adminauction/delete_unsubscribe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Unsubscribed"
        return context


@permission_required("is_superuser")
def delete_unsubcribed(request, pk):
    Unsubscribe.objects.filter(pk=pk).delete()
    messages.success(request, "User unsubscribed  Deleted Successfuly")
    return redirect("adminauction:delete_unsubcribe")


class UsersDb(SuperuserRequiredMixin, ListView):
    login_url = "account_login"
    model = get_user_model()
    template_name = "adminauction/users_db.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = get_user_model().objects.all().exclude(is_superuser=1)
        context["title"] = "Users"
        return context


class DeleteCheckoutDB(SuperuserRequiredMixin, ListView):
    login_url = "account_login"
    model = CheckoutDone
    template_name = "adminauction/delete_checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checkout"] = CheckoutDone.objects.all()
        context["title"] = "Checkout"
        return context


@permission_required("is_superuser")
def delete_checkoutdone_db(request, pk):
    CheckoutDone.objects.filter(pk=pk).delete()
    messages.success(request, " Checkout deleted Successfuly")
    return redirect("adminauction:delete_checkout")


@permission_required("is_superuser")
def delete_article(request, slug):
    article = Article.objects.get(slug=slug)
    if Article.objects.get(slug=slug):
        article = Article.objects.get(slug=slug)
        context = {"pk": article.slug}
        return render(request, "adminauction/delete_article.html", context)
    return None


@permission_required("is_superuser")
def delete_article_done(request, slug):
    article = Article.objects.get(slug=slug)
    if Article.objects.values("article").exists():
        article = Article.objects.get(slug=slug)
        if ImageUpload.objects.filter(article=article.pk).exists():
            image = ImageUpload.objects.filter(article=article.pk)
            for img in image:
                img1 = ImageUpload.objects.get(image=img)
                Path(img1.image.path).unlink()
            img1.delete()
        else:
            pass
        article = Article.objects.get(slug=article.slug).delete()  # type: ignore[assignment]
    messages.success(request, "Article Deleted Successfuly")
    return redirect("adminauction:setting")


@permission_required("is_superuser")
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    pk = category.name
    return render(request, "adminauction/delete_category.html", {"pk": pk})


@permission_required("is_superuser")
def delete_category_done(request, pk):
    Category.objects.filter(name=pk).delete()
    messages.success(request, "Category deleted Successfuly")
    return redirect("adminauction:create_category")


@permission_required("is_superuser")
def delete_subcategory(request, pk):
    subcategory = Subcategory.objects.get(pk=pk)
    pk = subcategory.name
    return render(request, "adminauction/delete_subcategory.html", {"pk": pk})


@permission_required("is_superuser")
def delete_subcategory_done(request, pk):
    Subcategory.objects.filter(name=pk).delete()
    messages.success(request, "Subcategory deleted Successfuly")
    return redirect("adminauction:create_subcategory")


@permission_required("is_superuser")
def delete_user(request, pk):
    user = get_user_model().objects.get(pk=pk)
    pk = user.name
    return render(request, "adminauction/delete_user.html", {"pk": pk})


@permission_required("is_superuser")
def delete_user_done(request, pk):
    user = get_user_model().objects.get(name=pk)

    if CheckoutDone.objects.filter(user=user.pk).exists():
        messages.error(
            request,
            f"Before delete {user.username} You must delete before his checkout record",
        )
        return None

    get_user_model().objects.filter(name=user.name).delete()
    messages.success(request, "User deleted Successfuly")
    return redirect("adminauction:users_db")


@permission_required("is_superuser")
def cron(request):
    schedule = CrontabSchedule.objects.all()
    periodic = PeriodicTask.objects.all()
    return render(
        request,
        "adminauction/cron.html",
        {"schedule": schedule, "periodic": periodic},
    )


@permission_required("is_superuser")
def set_weekly_report(request):
    form = CrontabWeeklyForm(request.POST)
    if request.method == "POST":
        form = CrontabWeeklyForm(request.POST)
        if form.is_valid():
            day_of_week = form.cleaned_data["day_of_week"]
            hour = form.cleaned_data["hour"]
            minute = form.cleaned_data["minute"]
            task_name = form.cleaned_data["task_name"]
            schedule, _ = CrontabSchedule.objects.get_or_create(
                day_of_week=day_of_week,
                hour=hour,
                minute=minute,
            )
            tasks = PeriodicTask.objects.all()
            if str(task_name) in str(tasks):
                PeriodicTask.objects.filter(name=task_name).delete()
            PeriodicTask.objects.create(
                name=task_name,
                task="tasks.send_weekly_report",
                crontab=schedule,
            )
            return HttpResponseRedirect("/adminauction/cron")
    return render(request, "adminauction/update_weekly.html", {"form": form})


@permission_required("is_superuser")
def set_daily_report(request):
    form = CrontabDailyForm(request.POST)
    if request.method == "POST":
        form = CrontabDailyForm(request.POST)
        if form.is_valid():
            hour = form.cleaned_data["hour"]
            minute = form.cleaned_data["minute"]
            task_name = form.cleaned_data["task_name"]
            schedule, _ = CrontabSchedule.objects.get_or_create(
                day_of_week="*",
                hour=hour,
                minute=minute,
            )
            tasks = PeriodicTask.objects.all()
            if str(task_name) in str(tasks):
                PeriodicTask.objects.filter(name=task_name).delete()
            PeriodicTask.objects.create(
                name=task_name,
                task="tasks.send_daily_report",
                crontab=schedule,
            )
            return HttpResponseRedirect("/adminauction/cron")
    return render(request, "adminauction/update_daily.html", {"form": form})


@permission_required("is_superuser")
def disable_periodic(request, pk):
    periodic = PeriodicTask.objects.get(id=pk)
    periodic.enabled = False
    periodic.save()
    return HttpResponseRedirect("/adminauction/cron/")


@permission_required("is_superuser")
def enable_periodic(request, pk):
    periodic = PeriodicTask.objects.get(id=pk)
    periodic.enabled = True
    periodic.save()
    return HttpResponseRedirect("/adminauction/cron/")


@permission_required("is_superuser")
def delete_periodic(request, pk):
    periodic = PeriodicTask.objects.get(id=pk)
    periodic.delete()
    return HttpResponseRedirect("/adminauction/cron/")


@permission_required("is_superuser")
def delete_crontab(request, pk):
    if CrontabSchedule.objects.get(id=pk):
        CrontabSchedule.objects.get(id=pk).delete()
    return HttpResponseRedirect("/adminauction/cron/")
