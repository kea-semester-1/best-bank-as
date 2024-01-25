from django.urls import path

from best_bank_as import views

app_name = "best_bank_as"


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("accounts/", views.account_list, name="account_list"),
    path("accounts/<int:pk>/", views.account_details, name="account_details"),
    path(
        "staff/accounts/<int:pk>",
        views.staff_account_list,
        name="staff_account_list",
    ),
    path("staff/", views.staff_page, name="staff_page"),
    path("staff/customers", views.staff_customer_list, name="staff_customer_list"),
    path(
        "staff/customers/approve",
        views.customers_approve_list,
        name="customers_approve_list",
    ),
    path(
        "staff/customers/approve/<int:pk>",
        views.customers_approve_details,
        name="customers_approve_details",
    ),
    # TODO: Figure if register, should just be customer path
    path("customers/register/", views.customer_list, name="customer_register"),
    path("customers/", views.customer_list, name="customer"),
    path("customers/<int:pk>/", views.customer_details, name="customer"),
    # Loan applications
    path(
        "loan-applications",
        views.loan_application_list,
        name="loan_application_list",
    ),
    path(
        "loan-applications/<int:pk>",
        views.loan_application_details,
        name="loan_application_details",
    ),
    path(
        "staff/loan-applications/<int:pk>",
        views.staff_loan_application_details,
        name="staff_loan_application_details",
    ),
    path(
        "staff/loan-applications/",
        views.staff_loan_applications_list,
        name="approve_loan_applications",
    ),
    # Transfers
    path("transfer/", views.transaction_list, name="transfer_money"),
    path("external-transfer/", views.external_transfer, name="external-transfer"),
    # Auth
    path("auth-token/", views.auth_token, name="api_token_auth"),
]
