from django.contrib import admin

from src.categories.models import Category
from src.categories.models import Subcategory


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
