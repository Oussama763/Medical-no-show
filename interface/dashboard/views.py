from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from appointments.models import Doctor
from .forms import DoctorCreationForm


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


@login_required
def doctor_list(request):

    doctors = Doctor.objects.select_related("user").all()

    return render(
        request,
        "dashboard/admin/doctors.html",
        {
            "doctors": doctors,
        },
    )




@login_required
def doctor_create(request):

    if request.method == "POST":

        form = DoctorCreationForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
            )

            Doctor.objects.create(
                user=user,
                specialization=form.cleaned_data["specialization"],
            )

            return redirect("dashboard:doctor_list")

    else:

        form = DoctorCreationForm()

    return render(
        request,
        "dashboard/admin/doctor_form.html",
        {
            "form": form,
        },
    )