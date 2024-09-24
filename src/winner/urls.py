from django.urls import path

from src.winner import views

app_name = "winner"

urlpatterns = [
    path("winner/<str>", views.WinnerListView.as_view(), name="winner"),
    path("detail/<id>/", views.WinnerDetailView.as_view(), name="detail"),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("failed/", views.PaymentFailedView.as_view(), name="failed"),
    path(
        "api/checkout-session/<id>/",
        views.create_checkout_session,
        name="api_checkout_session",
    ),
    path("checkout/<id>/", views.checkout, name="checkout"),
    path("success_payment/", views.SucccessPayment.as_view(), name="succcess_payment"),
    path("execute_payment/<id>/", views.execute_payment, name="execute_payment"),
]
