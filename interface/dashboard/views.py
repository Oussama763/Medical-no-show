from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from appointments.models import Doctor
from .forms import (DoctorCreationForm, DoctorUpdateForm)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .decorators import admin_required


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


@admin_required
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


@admin_required
def doctor_list(request):

    doctors = Doctor.objects.select_related("user").all()

    return render(
        request,
        "dashboard/admin/doctors.html",
        {
            "doctors": doctors,
        },
    )




@admin_required
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

            messages.success(
                request,
                "Doctor created successfully."
            )

            return redirect("dashboard:doctor_list")

    else:

        form = DoctorCreationForm()

    return render(
        request,
        "dashboard/admin/doctor_form.html",
        {
            "form": form,
            "title": "Create Doctor",
            "button_text": "Create Doctor",
        },
    )



@admin_required
def doctor_update(request, pk):

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
    )

    if request.method == "POST":

        form = DoctorUpdateForm(request.POST)

        if form.is_valid():

            doctor.user.first_name = form.cleaned_data["first_name"]
            doctor.user.last_name = form.cleaned_data["last_name"]
            doctor.user.email = form.cleaned_data["email"]

            doctor.user.save()

            doctor.specialization = form.cleaned_data["specialization"]

            doctor.save()

            messages.success(
                request,
                "Doctor updated successfully."
            )

            return redirect("dashboard:doctor_list")

    else:

        form = DoctorUpdateForm(
            initial={
                "first_name": doctor.user.first_name,
                "last_name": doctor.user.last_name,
                "email": doctor.user.email,
                "specialization": doctor.specialization,
            }
        )

    return render(
        request,
        "dashboard/admin/doctor_form.html",
        {
            "form": form,
            "title": "Edit Doctor",
            "button_text": "Save Changes",
        },
    )





@admin_required
def doctor_delete(request, pk):

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
    )

    if request.method == "POST":

        doctor.user.delete()

        return redirect("dashboard:doctor_list")

    return render(
        request,
        "dashboard/admin/doctor_confirm_delete.html",
        {
            "doctor": doctor,
        },
    )