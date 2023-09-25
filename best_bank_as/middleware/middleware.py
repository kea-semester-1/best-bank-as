from django.http import HttpResponseNotFound
from django.shortcuts import render


class NotFoundMiddleware:
    """Middleware to prevent standard error page."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return HttpResponseNotFound(
                render(request, "best_bank_as/error_pages/404_not_found.html")
            )
        return response
