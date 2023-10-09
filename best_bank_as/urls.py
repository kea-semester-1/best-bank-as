from django.urls import path

from best_bank_as import views

app_name = "best_bank_as"


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile_page, name="profile_page"),
    path("accounts/<int:pk>", views.get_accounts, name="get_accounts"),
    path("accounts/details/<int:pk>", views.get_details, name="get_details"),
    path("loans", views.loans_page, name="loans-page"),
    path(
        "loans/<int:pk>",
        views.delete_loan_application,
        name="delete-loan-application",
    ),
]
