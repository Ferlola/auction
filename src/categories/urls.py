from django.urls import path

from src.categories import views

app_name = "categories"

urlpatterns = [
    path("category/", views.CategoryView.as_view(), name="category"),
]
