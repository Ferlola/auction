from django.urls import path

from src.adminauction import views

app_name = "adminauction"

urlpatterns = [
    path("setting/", views.PermissionUpdateArticle.as_view(), name="setting"),
    path("update_article/<pk>", views.UpdateArticle.as_view(), name="update_article"),
    # path("dates_times/<pk>", views.DateTimeView.as_view(),
    #      name="dates_times"),
    path("article/<pk>/", views.BidArticle.as_view(), name="article"),
    path("fee/", views.FeeView.as_view(), name="fee"),
    path("create_category/", views.CategoryView.as_view(), name="create_category"),
    path(
        "create_subcategory/",
        views.SubcategoryView.as_view(),
        name="create_subcategory",
    ),
    path("delete_checkout/", views.DeleteCheckoutDB.as_view(), name="delete_checkout"),
    path("delete_checkout/<pk>", views.delete_checkoutdone_db, name="delete_checkoutt"),
    path(
        "delete_unsubscribe/",
        views.DeleteUnsubscribedDB.as_view(),
        name="delete_unsubcribe",
    ),
    path(
        "delete_unsubscribed/<pk>",
        views.delete_unsubcribed,
        name="delete_unsubscribed",
    ),
    path("delete_category/<pk>/", views.delete_category, name="delete_category"),
    path(
        "delete_category_done/<pk>/",
        views.delete_category_done,
        name="delete_category_done",
    ),
    path(
        "delete_subcategory/<pk>/",
        views.delete_subcategory,
        name="delete_subcategory",
    ),
    path(
        "delete_subcategory_done/<pk>/",
        views.delete_subcategory_done,
        name="delete_subcategory_done",
    ),
    path("delete_article/<slug>", views.delete_article, name="delete_article"),
    path(
        "delete_article_done/<slug>",
        views.delete_article_done,
        name="delete_article_done",
    ),
    path("users_db", views.UsersDb.as_view(), name="users_db"),
    path("delete_user/<pk>", views.delete_user, name="delete_user"),
    path("delete_user_done/<pk>", views.delete_user_done, name="delete_user_done"),
    path("bids_history", views.BidsHistoryView.as_view(), name="bids_history"),
    path("cron/", views.cron, name="cron"),
    path("set_weekly_report", views.set_weekly_report, name="set_weekly_report"),
    path("set_daily_report", views.set_daily_report, name="set_daily_report"),
    path("disable_periodic/<int:pk>", views.disable_periodic, name="disable_periodic"),
    path("enable_periodic/<int:pk>", views.enable_periodic, name="enable_periodic"),
    path("delete_crontab/<int:pk>", views.delete_crontab, name="delete_crontab"),
    path("delete_periodic/<int:pk>", views.delete_periodic, name="delete_periodic"),
]
