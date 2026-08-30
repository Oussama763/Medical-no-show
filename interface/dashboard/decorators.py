from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if not request.user.is_superuser:
            messages.error(
                request,
                "You do not have permission to access this page."
            )
            return redirect("dashboard:redirect")

        return view_func(request, *args, **kwargs)

    return wrapper 

# this shouldn't show up in the main branch