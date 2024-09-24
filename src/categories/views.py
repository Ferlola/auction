from django.db.models import Count
from django.utils import timezone
from django.views.generic import ListView

from src.articles.models import Article
from src.articles.views import date_time
from src.categories.models import Category


class CategoryView(ListView):
    model = Category
    paginate_by = 8
    template_name = "categories/category.html"

    def get_queryset(self):
        return Article.objects.filter(subcategory__name__icontains=self.queryset())

    def queryset(self):
        return self.request.GET.get("q")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queryset"] = self.queryset()
        context["num_articles"] = Article.objects.filter(publish=True).count()
        context.update(
            {"categories": Category.objects.annotate(items_count=Count("article"))},
        )
        context["message"] = context["queryset"]
        context["title"] = context["queryset"]
        context["day"] = timezone.localtime(timezone.now()).date()
        context["date_time"] = date_time
        context["time_now"] = timezone.now()
        return context
