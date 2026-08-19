from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def redirect_dashboard(request):

    user = request.user

    if user.is_superuser:
        return redirect("dashboard:admin")

    elif hasattr(user, "doctor"):
        return redirect("dashboard:doctor")

    elif hasattr(user, "patient"):
        return redirect("dashboard:patient")

    return redirect("login")


@login_required
def admin_dashboard(request):

    return render(
        request,
        "dashboard/admin/dashboard.html",
    )


@login_required
def doctor_dashboard(request):

    return render(
        request,
        "dashboard/doctor/dashboard.html",
    )


@login_required
def patient_dashboard(request):

    return render(
        request,
        "dashboard/patient/dashboard.html",
    )