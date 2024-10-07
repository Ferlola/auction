import sys
import uuid
from email.mime.image import MIMEImage
from io import BytesIO
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import ImageField
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.db.models import SlugField
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from meta.models import ModelMeta
from PIL import Image

from src.adminauction.models import SetBidArticle
from src.categories.models import Category
from src.categories.models import Subcategory


class Article(ModelMeta, models.Model):
    user = ForeignKey("users.User", on_delete=models.CASCADE)
    article = CharField(_("Article name"), max_length=100, blank=False, null=False)
    description = CharField(
        _("Article description"),
        max_length=255,
        blank=False,
        null=False,
    )
    location = CharField(_("Article location"), max_length=100, blank=False, null=False)
    category = models.ForeignKey(
        Category,
        max_length=25,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(
        Subcategory,
        max_length=25,
        on_delete=models.CASCADE,
    )
    reserved = IntegerField(default=0, blank=True, null=True)
    slug = SlugField(null=False, blank=False, unique=True)
    likes = ManyToManyField("users.User", related_name="user_like", blank=True)
    dislikes = ManyToManyField("users.User", related_name="user_dislike", blank=True)
    from_date = DateField(blank=True, null=True)
    date_time = DateTimeField(blank=True, null=True)
    notification_winner = BooleanField(default=True)
    notification_no_bid = BooleanField(default=True)
    publish = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)
        db_table = "Article"
        app_label = "articles"

    def __str__(self):
        return str(self.article)

    def get_absolute_url(self):
        return "/article/%i/" % self.id

    _metadata = {
        "title": "article",
        "description": "description",
    }

    @property
    def get_bid(self):
        bid_amount = 0
        if SetBidArticle.objects.filter(name=self.article).filter(set_bid=2):
            bid_amount_article = (
                SetBidArticle.objects.filter(name=self.article)
                .filter(set_bid=2)
                .values_list("bid_amount", flat=True)
            )

            bid_amount += int(str(bid_amount_article)[11:-2])
            return bid_amount
        return None

    def days_to_finish(self):
        days = str(self.date_time - timezone.now())
        return days.split(",", 1)[0]

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()


def set_slug(sender, instance, *args, **kwargs):
    if instance.article and not instance.slug:
        slug = slugify(f"{instance.article}-{str(uuid.uuid4())[:8]}")
        instance.slug = slug


pre_save.connect(set_slug, sender=Article)


class ImageUpload(models.Model):
    article = ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    image = ImageField(
        upload_to="images/",
        verbose_name="Image",
        blank=False,
        null=False,
    )

    class Meta:
        db_table = "ImageUpload"
        app_label = "articles"

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.resizeimage(self.image)
        super().save(*args, **kwargs)

    def resizeimage(self, image):
        imagetemproary = Image.open(image)
        imagetemproary = imagetemproary.convert("RGB")
        outputiostream = BytesIO()
        width, height = imagetemproary.size
        preferedwidth = 600
        if width > preferedwidth or width < preferedwidth:
            ratio = height / width
            newwidth = preferedwidth
            newheight = int(newwidth * ratio)
            imagetemproary = imagetemproary.resize(
                (newwidth, newheight),
                Image.Resampling.LANCZOS,
            )
        imagetemproary.save(outputiostream, format="JPEG", quality=60)
        outputiostream.seek(0)
        return InMemoryUploadedFile(
            outputiostream,
            "ImageField",
            f"{image.name.split('.')[0]}.jpg",
            "image/jpeg",
            sys.getsizeof(outputiostream),
            None,
        )

    @property
    def one_image(self):
        return (
            ImageUpload.objects.filter(article=self.article).values("image").count() > 1
        )

    def images_left(self):
        return ImageUpload.objects.all().count()


def get_image(article_id):
    image = str(
        ImageUpload.objects.filter(article__in=article_id).values_list("image").first(),
    )[2:-3]
    return "src/media/" + image


def get_article_id(article):
    return Article.objects.filter(article=article).values_list("id", flat=True)


def show_image(article):
    image = get_image(get_article_id(article))

    with Path(image).open("rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", f"{image}")
        img.add_header("Content-Disposition", "inline", filename=image)
        return img


def get_logo():
    logo = "logo.png"
    return "staticfiles/images/" + logo


def show_logo(get_logo):
    with Path(get_logo).open("rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", f"{get_logo}")
        img.add_header("Content-Disposition", "inline", filename=get_logo)
        return img
