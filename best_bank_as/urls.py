from django.urls import path

from best_bank_as.views_classes import customer_view
from best_bank_as import views

app_name = "best_bank_as"


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_page, name="profile_page"),
    path("accounts/<int:pk>", views.get_accounts, name="get_accounts"),
    path("accounts/details/<int:pk>", views.get_details, name="get_details"),
    path("staff/<str:username>", views.staff_page, name="staff_page"),
    path("staff/search/", views.search_customer, name="search_customer"),
    path(
        "register/", customer_view.CustomerCreateView.as_view(), name="create_customer"
    ),
    path("loans", views.loans_page, name="loans-page"),
    path(
        "loans/<int:pk>",
        views.delete_loan_application,
        name="delete-loan-application",
    ),
    path("transfer/", views.transfer_money, name="transfer_money"),
]
