from collections.abc import Callable
from datetime import datetime

from django.contrib.auth import logout
from django.core.cache import cache
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    QueryDict,
)
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

        current_time = datetime.now()
        last_activity = request.session.get("last_activity", None)

        request.session["last_activity"] = current_time.strftime(
            constants.DATETIME_FORMAT
        )

        if not last_activity:
            return response

        dt = current_time - datetime.strptime(last_activity, constants.DATETIME_FORMAT)
        session_expired = dt.seconds > constants.SESSION_TIMEOUT_SECONDS

        if session_expired:
            print("********** SESSION EXPIRED **********")
            logout(request)

        return response


class IdempotencyMiddleware:
    """Middleware for idempotent behavior."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST" and request.path in [
            "/external-transfer/",
            "/transfer/",
        ]:
            idempotency_key = request.headers.get("Idempotency-Key")

            if not idempotency_key:
                # Render the error page for missing idempotency key
                response_content = render(
                    request, "best_bank_as/error_pages/idempotency_key_missing.html"
                ).content
                return HttpResponseBadRequest(
                    response_content, content_type="text/html"
                )

            if cache.get(idempotency_key):
                # Render the error page for request already processed
                response_content = render(
                    request, "best_bank_as/error_pages/request_already_processed.html"
                ).content
                print(response_content)
                return HttpResponseBadRequest(
                    response_content, content_type="text/html"
                )

            cache.set(idempotency_key, "processed", 86400)  # 24 hours

        response = self.get_response(request)
        return response
