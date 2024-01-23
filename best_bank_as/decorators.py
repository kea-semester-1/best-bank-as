# noqa

from functools import wraps
from typing import Any, Literal

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def group_required(*group_names: Literal["customer", "employee", "supervisor"]) -> Any:
    """Decorator to check if user is in a group."""

    def _decorator(view_func: Any) -> Any:  # Callable
        @wraps(view_func)
        @login_required
        def _wrapped_view(
            request: HttpRequest, *args: Any, **kwargs: Any
        ) -> HttpResponse:
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            groups = request.user.groups.all()

            if not any(group.name in group_names for group in groups):
                return render(
                    request,
                    "best_bank_as/error_pages/error_page.html",
                )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return _decorator
