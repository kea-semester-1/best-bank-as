from django.urls import path

from best_bank_as import views

app_name = "best_bank_as"


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_page, name="profile_page"),
    path("accounts/", views.get_accounts_list, name="get_accounts_list"),
    path("accounts/details/<int:pk>", views.get_account_details, name="get_details"),
    path(
        "staff/accounts/<int:pk>",
        views.get_accounts_for_user,
        name="get_accounts_for_user",
    ),
    path("staff/<str:username>", views.staff_page, name="staff_page"),
    path("staff/search/", views.search_customer, name="search_customer"),
    path(
        "staff/approve/customers",
        views.approve_customers_list,
        name="approve_customers",
    ),
    path(
        "staff/approve/customers/<int:pk>",
        views.approve_customers_details,
        name="approve_customers_details",
    ),
    path("register/", views.new_customer, name="create_customer"),
    path("loans", views.loans_page, name="loans-page"),
    path(
        "loans/<int:pk>",
        views.delete_loan_application,
        name="delete-loan-application",
    ),
    path("transfer/", views.transfer_money, name="transfer_money"),
]
