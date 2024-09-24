from django.urls import path

from src.contact.views import ask_seller
from src.contact.views import contact

app_name = "contact"
urlpatterns = [
    path("contact/", contact, name="contact"),
    path("ask_seller/<str:article>/", ask_seller, name="ask_seller"),
]
