from django.urls import path

from src.users import views
from src.users.views import user_detail_view
from src.users.views import user_redirect_view
from src.users.views import user_update_view

app_name = "users"

urlpatterns = [
    path("badges/", views.badges, name="badges"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
