from functools import wraps
from datetime import date, datetime, timedelta
import calendar

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from appointments.models import Appointment, Doctor, Patient, TimeSlot
from appointments.models import ModelTrainingHistory
from django.db.models import Count, Q
from .decorators import admin_required
from .forms import (
    DoctorCreationForm,
    DoctorUpdateForm,
    TimeSlotForm,
    TimeSlotGenerationForm,
)
from django.db.models import Avg

def patient_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        patient = getattr(request.user, "patient", None)
        if patient is None:
            messages.error(request, "You need a patient account to access the booking area.")
            return redirect("dashboard:redirect")

        return view_func(request, patient, *args, **kwargs)

    return wrapper


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

    doctor = getattr(request.user, "doctor", None)
    if doctor is None:
        messages.error(request, "You need a doctor account to access this page.")
        return redirect("dashboard:redirect")

    # Get distinct dates where this doctor has any timeslots
    dates = (
        TimeSlot.objects.filter(doctor=doctor)
        .values_list("date", flat=True)
        .distinct()
        .order_by("date")
    )

    return render(
        request,
        "dashboard/doctor/dashboard.html",
        {"doctor": doctor, "dates": dates},
    )


@login_required
def doctor_day(request, date):
    doctor = getattr(request.user, "doctor", None)
    if doctor is None:
        messages.error(request, "You need a doctor account to access this page.")
        return redirect("dashboard:redirect")

    # parse date string (expected YYYY-MM-DD)
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except Exception:
        messages.error(request, "Invalid date format.")
        return redirect("dashboard:doctor")

    slots = (
        TimeSlot.objects.filter(doctor=doctor, date=selected_date)
        .select_related("doctor__user")
        .order_by("start_time")
    )

    # gather appointment per slot if exists
    slot_info = []
    for slot in slots:
        appointment = None
        try:
            appointment = slot.appointment
        except Exception:
            appointment = None
        slot_info.append({"slot": slot, "appointment": appointment})

    return render(
        request,
        "dashboard/doctor/day.html",
        {"doctor": doctor, "date": selected_date, "slot_info": slot_info},
    )


@login_required
def predict_appointment_view(request, pk):
    # Allow doctors to trigger prediction for appointments they own, or admins
    appointment = get_object_or_404(Appointment, pk=pk)

    if not (request.user.is_superuser or hasattr(request.user, 'doctor')):
        messages.error(request, 'Permission denied')
        return redirect('dashboard:doctor')

    if hasattr(request.user, 'doctor') and not request.user.is_superuser:
        if appointment.slot.doctor != request.user.doctor:
            messages.error(request, 'Permission denied')
            return redirect('dashboard:doctor')

    # Compute prediction
    try:
        from no_show_ML.predict import predict_appointment_no_show

        prob = predict_appointment_no_show(appointment)
        if prob is not None:
            appointment.predicted_no_show = prob
            appointment.save(update_fields=['predicted_no_show'])
            messages.success(request, f'Predicted no-show probability: {prob:.2f}')
        else:
            messages.error(request, 'Prediction model not available')
    except Exception:
        messages.error(request, 'Prediction failed')

    return redirect(request.META.get('HTTP_REFERER', 'dashboard:doctor'))


@login_required
def doctor_patient_detail(request, pk):
    doctor = getattr(request.user, "doctor", None)
    if doctor is None and not request.user.is_superuser:
        messages.error(request, "You need a doctor account to access this page.")
        return redirect("dashboard:redirect")

    patient = get_object_or_404(Patient, pk=pk)

    # Optional: ensure the doctor has at least one appointment with this patient
    if not request.user.is_superuser:
        has_appointment = Appointment.objects.filter(patient=patient, slot__doctor=doctor).exists()
        if not has_appointment:
            messages.error(request, "You do not have permission to view this patient's details.")
            return redirect("dashboard:doctor")

    return render(
        request,
        "dashboard/doctor/patient_detail.html",
        {"patient": patient},
    )


@login_required
@patient_required
def patient_dashboard(request, patient):
    today = date.today()
    upcoming = (
        Appointment.objects.filter(patient=patient, slot__date__gte=today)
        .select_related("slot__doctor__user")
        .order_by("slot__date", "slot__start_time")
    )
    recent = (
        Appointment.objects.filter(patient=patient)
        .select_related("slot__doctor__user")
        .order_by("-slot__date", "-slot__start_time")[:5]
    )

    return render(
        request,
        "dashboard/patient/dashboard.html",
        {
            "patient": patient,
            "upcoming": upcoming,
            "recent": recent,
            "total_appointments": Appointment.objects.filter(patient=patient).count(),
            "upcoming_count": upcoming.count(),
            "missed_count": Appointment.objects.filter(patient=patient, status=Appointment.NO_SHOW).count(),
        },
    )


@login_required
@patient_required
def patient_appointments(request, patient):
    appointments = (
        Appointment.objects.filter(patient=patient)
        .select_related("slot__doctor__user")
        .order_by("slot__date", "slot__start_time")
    )

    return render(
        request,
        "dashboard/patient/appointments.html",
        {"appointments": appointments},
    )


@login_required
def update_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    # Only allow doctors (for their own appointments) or admins to record attendance
    if not (request.user.is_superuser or hasattr(request.user, "doctor")):
        messages.error(request, "Only doctors or administrators can update appointment attendance.")
        return redirect("dashboard:patient_appointments")

    # If doctor, ensure they are updating their own appointment
    if hasattr(request.user, "doctor") and not request.user.is_superuser:
        if appointment.slot.doctor != request.user.doctor:
            messages.error(request, "You do not have permission to modify this appointment.")
            return redirect("dashboard:doctor")

    if request.method == "POST":
        outcome = request.POST.get("outcome", "")
        appointment.record_attendance(outcome)
        messages.success(request, f"Appointment status updated to {appointment.get_status_display()}.")
        # Redirect doctors to their dashboard, admins to patient view, keep patients on their page
        if request.user.is_superuser:
            return redirect("dashboard:patient_appointments")
        return redirect("dashboard:doctor")

    return redirect("dashboard:patient_appointments")


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
def admin_patients(request):
    # List patients with their latest predicted no-show (if any)
    patients = (
        Patient.objects.all()
        .select_related('user')
    )

    # Build list of (patient, latest_appointment) to avoid complex template calls
    patients_with_latest = []
    for p in patients:
        appt = p.appointments.order_by('-slot__date').first()
        patients_with_latest.append((p, appt))

    return render(request, 'dashboard/admin/patients.html', {'patients_with_latest': patients_with_latest})


@admin_required
def admin_analytics(request):
    # Daily no-show percentage for last 30 days
    today = datetime.utcnow().date()
    start = today - timedelta(days=30)

    stats_qs = (
        Appointment.objects.filter(slot__date__gte=start)
        .values('slot__date')
        .annotate(total=Count('id'), no_shows=Count('id', filter=Q(status=Appointment.NO_SHOW)))
        .order_by('slot__date')
    )

    stats = []
    for row in stats_qs:
        pct = 0.0
        if row['total']:
            pct = 100.0 * row['no_shows'] / row['total']
        stats.append({'date': row['slot__date'], 'total': row['total'], 'no_shows': row['no_shows'], 'pct': pct})

    # Model training history
    history = ModelTrainingHistory.objects.all().order_by('-run_at')[:50]

    return render(request, 'dashboard/admin/analytics.html', {'stats': stats, 'history': history})




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
                "appointment_duration": doctor.appointment_duration,
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
            duration = doctor.appointment_duration
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




@login_required
@patient_required
def booking_calendar(request, patient):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    month_calendar = calendar.monthcalendar(year, month)
    calendar_data = []

    for week in month_calendar:
        week_data = []

        for day in week:
            if day == 0:
                week_data.append(None)
                continue

            current_date = date(year, month, day)
            available = TimeSlot.objects.filter(date=current_date, is_available=True).count()
            is_past = current_date < today

            if is_past:
                color = "secondary"
            elif available == 0:
                color = "danger"
            elif available <= 3:
                color = "warning"
            else:
                color = "success"

            week_data.append({
                "day": day,
                "date": current_date,
                "available": available,
                "color": color,
                "is_past": is_past,
            })

        calendar_data.append(week_data)

    return render(
        request,
        "dashboard/patient/calendar.html",
        {
            "calendar": calendar_data,
            "month": calendar.month_name[month],
            "year": year,
            "previous_month": previous_month,
            "previous_year": previous_year,
            "next_month": next_month,
            "next_year": next_year,
        },
    )


@login_required
@patient_required
def book_appointment(request, patient, selected_date):
    try:
        target_date = date.fromisoformat(selected_date)
    except ValueError:
        messages.error(request, "The date is invalid.")
        return redirect("dashboard:booking_calendar")

    slots = (
        TimeSlot.objects.filter(date=target_date, is_available=True)
        .select_related("doctor__user")
        .order_by("start_time")
    )

    if request.method == "POST":
        slot_id = request.POST.get("slot")
        slot = get_object_or_404(TimeSlot, pk=slot_id, date=target_date, is_available=True)

        try:
            if Appointment.objects.filter(slot=slot).exists():
                messages.error(request, "This slot has already been booked.")
                return redirect("dashboard:booking_calendar")

            Appointment.objects.create(patient=patient, slot=slot)
            slot.is_available = False
            slot.save(update_fields=["is_available"])
            messages.success(request, f"Appointment booked for {slot.doctor} on {slot.date} at {slot.start_time}.")
            return redirect("dashboard:patient_appointments")
        except IntegrityError:
            messages.error(request, "This slot is no longer available.")
            return redirect("dashboard:booking_calendar")

    return render(
        request,
        "dashboard/patient/book_appointment.html",
        {"selected_date": target_date, "slots": slots},
    )