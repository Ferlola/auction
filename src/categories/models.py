from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "category"
        app_label = "categories"

    def __str__(self):
        return str(self.name)


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "subcategory"
        app_label = "categories"

    def __str__(self):
        return str(self.name)

    @property
    def has_category(self):
        return Subcategory.objects.filter(category__in=Category.objects.values("id"))
