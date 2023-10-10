from django.urls import path

from best_bank_as import views

app_name = "best_bank_as"


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_page, name="profile_page"),
    path("accounts/<int:pk>", views.get_accounts, name="get_accounts"),
    path("accounts/details/<int:pk>", views.get_details, name="get_details"),
    path("transfer/", views.transfer_money, name="transfer_money"),
]
