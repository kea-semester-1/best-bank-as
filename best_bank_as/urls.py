from django.urls import path

from best_bank_as import views

app_name = "best_bank_as"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_page, name="profile_page"),
    path("accounts/", views.get_accounts_list, name="get_accounts_list"),
    path(
        "accounts/<int:pk>/", views.get_accounts_list, name="get_accounts_list_with_pk"
    ),
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
    # TODO: Figure if register, should just be customer path
    path("register/", views.customer_list, name="create_customer"),
    path("customers/", views.customer_list, name="customer"),
    path("customers/<int:pk>/", views.customer_details, name="customer"),
    # Loan applications
    path(
        "loan-applications",
        views.loan_application_list,
        name="loan_application_list",
    ),
    path(
        "loan-applications/details/<int:pk>",
        views.loan_application_details,
        name="loan_application_details",
    ),
    path(
        "staff/loan-applications/details/<int:pk>",
        views.staff_loan_application_details,
        name="staff_loan_application_details",
    ),
    path(
        "staff/loan-applications/",
        views.staff_loan_applications_page,
        name="approve_loan_applications",
    ),
    # Transfers
    path("transfer/", views.transaction_list, name="transfer_money"),
     path('external-transfer/', views.external_transfer, name='external-transfer'),
]
