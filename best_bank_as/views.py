from django.shortcuts import render


def index(request):
    return render(request, "best_bank_as/index.html")
