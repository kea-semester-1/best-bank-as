from collections.abc import Callable
from datetime import datetime

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import render

from best_bank_as import constants


class NotFoundMiddleware:
    """Prevents the standard error page when visiting invalid URL."""

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        if response is None:
            return HttpResponseNotFound(
                render(request, "best_bank_as/error_pages/404_not_found.html")
            )
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

    def __init__(self, get_response: HttpResponse):  # type : ignore
        """Init method for session timeout middleware."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Call method for session timeout middleware."""

        response = self.get_response(request)
        if not request.user.is_authenticated:
            return response

        last_activity = request.session.get("last_activity", None)

        if not last_activity:
            return response

        current_time = datetime.now()
        request.session["last_activity"] = current_time.strftime(
            constants.DATETIME_FORMAT
        )

        dt = current_time - datetime.strptime(last_activity, constants.DATETIME_FORMAT)
        session_expired = dt.seconds > constants.SESSION_TIMEOUT_SECONDS

        if session_expired:
            print("********** SESSION EXPIRED **********")
            logout(request)

        return response
