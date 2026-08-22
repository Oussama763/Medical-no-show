from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from appointments.models import Doctor
from .forms import (DoctorCreationForm, DoctorUpdateForm)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .decorators import admin_required
from appointments.models import TimeSlot
from .forms import TimeSlotForm
from datetime import datetime, timedelta
from .forms import TimeSlotGenerationForm
from django.core.exceptions import ValidationError


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
                appointment_duration=form.cleaned_data["appointment_duration"],
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
            doctor.appointment_duration = form.cleaned_data["appointment_duration"]
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




@admin_required
def slot_list(request):

    slots = (
        TimeSlot.objects
        .select_related("doctor__user")
        .order_by(
            "date",
            "start_time",
        )
    )

    return render(
        request,
        "dashboard/admin/slots.html",
        {
            "slots": slots,
        },
    )




@admin_required
def slot_create(request):

    if request.method == "POST":

        form = TimeSlotForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Time slot created successfully."
            )

            return redirect(
                "dashboard:slot_list"
            )

    else:

        form = TimeSlotForm()

    return render(
        request,
        "dashboard/admin/slot_form.html",
        {
            "form": form,
            "title": "Create Time Slot",
            "button_text": "Create Time Slot",
        },
    )




@admin_required
def slot_update(request, pk):

    slot = get_object_or_404(
        TimeSlot,
        pk=pk,
    )

    if request.method == "POST":

        form = TimeSlotForm(
            request.POST,
            instance=slot,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Time slot updated successfully."
            )

            return redirect(
                "dashboard:slot_list"
            )

    else:

        form = TimeSlotForm(
            instance=slot,
        )

    return render(
        request,
        "dashboard/admin/slot_form.html",
        {
            "form": form,
            "title": "Edit Time Slot",
            "button_text": "Save Changes",
        },
    )





@admin_required
def slot_delete(request, pk):

    slot = get_object_or_404(
        TimeSlot,
        pk=pk,
    )

    if request.method == "POST":

        slot.delete()

        messages.success(
            request,
            "Time slot deleted successfully."
        )

        return redirect(
            "dashboard:slot_list"
        )

    return render(
        request,
        "dashboard/admin/slot_confirm_delete.html",
        {
            "slot": slot,
        },
    )




@admin_required
def generate_slots(request):

    if request.method == "POST":

        form = TimeSlotGenerationForm(request.POST)

        if form.is_valid():

            doctor = form.cleaned_data["doctor"]
            date = form.cleaned_data["date"]
            work_start = form.cleaned_data["work_start"]
            work_end = form.cleaned_data["work_end"]
            duration = form.cleaned_data["duration"]
            break_start = form.cleaned_data["break_start"]
            break_end = form.cleaned_data["break_end"]

            current = datetime.combine(date, work_start)
            finish = datetime.combine(date, work_end)

            created = 0

            while current < finish:

                # Skip the break
                if break_start and break_end:

                    break_begin = datetime.combine(date, break_start)
                    break_finish = datetime.combine(date, break_end)

                    if break_begin <= current < break_finish:
                        current = break_finish
                        continue

                next_time = current + timedelta(minutes=duration)

                if next_time > finish:
                    break

                slot = TimeSlot(
                    doctor=doctor,
                    date=date,
                    start_time=current.time(),
                    end_time=next_time.time(),
                )

                try:

                    slot.full_clean()
                    slot.save()

                    created += 1

                except ValidationError:
                    pass

                current = next_time

            messages.success(
                request,
                f"{created} time slots generated successfully."
            )

            return redirect("dashboard:slot_list")

    else:

        form = TimeSlotGenerationForm()

    return render(
        request,
        "dashboard/admin/generate_slots.html",
        {
            "form": form,
        },
    )