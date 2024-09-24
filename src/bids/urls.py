from django.urls import path

from src.bids import views

app_name = "bids"

urlpatterns = [
    path("pdf/<str:article_pdf>/", views.invoice_pdf, name="pdf"),
    path("history", views.bids_history, name="history"),
]
