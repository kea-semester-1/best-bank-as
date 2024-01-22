import datetime
from collections.abc import Callable

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import render


class NotFoundMiddleware:
    """Prevents the standard error page when visiting invalid URL."""

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        if response.status_code == 404:
            return HttpResponseNotFound(
                render(request, "best_bank_as/error_pages/404_not_found.html")
            )
        return response


class RequestMethodDictionaryMiddleware:
    """Middleware for handling PUT requests."""

    def __init__(self, get_response: HttpResponse) -> None:
        """Init method."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> None:
        """Handles the PUT request."""
        if request.method == "PUT":
            request.PUT = QueryDict(request.body)

        response = self.get_response(request)
        return response


class SessionTimeoutMiddleware:
    """Middleware for session timeout."""

    def __init__(self, get_response):  # type : ignore
        """Init method for session timeout middleware."""
        self.get_response = get_response

    def __call__(self, request):  # type : ignore
        """Call method for session timeout middleware."""
        if request.user.is_authenticated:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_activity = request.session.get("last_activity", None)
            if last_activity:
                last_activity = datetime.datetime.strptime(
                    last_activity, "%Y-%m-%d %H:%M:%S"
                )
                if (datetime.datetime.now() - last_activity).seconds > 300:  # 5 minutes
                    logout(request)
            request.session["last_activity"] = current_time
        response = self.get_response(request)
        return response
