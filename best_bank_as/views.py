from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    """View for index"""



    

    return render(request, "best_bank_as/index.html")
