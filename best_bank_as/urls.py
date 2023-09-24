from django.urls import path

from best_bank_as import views

app_name = "best_bank_as"

urlpatterns = [
    path("", views.index, name="index"),
]
