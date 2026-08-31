from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientRegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
import random


def register(request):

    if request.method == "POST":

        form = PatientRegistrationForm(request.POST)

        username = request.POST.get("username")

        # If a user with this username already exists but is inactive,
        # resend a verification code and redirect to the verification page.
        existing = None
        if username:
            existing = User.objects.filter(username=username).first()
            if existing and not existing.is_active:
                try:
                    patient = getattr(existing, "patient", None)
                    if not patient:
                        # If patient row missing, try to create it if form valid
                        if form.is_valid():
                            u = form.save(commit=False)
                            # do not overwrite existing user
                            Patient.objects.create(
                                user=existing,
                                birth_date=form.cleaned_data["birth_date"],
                                gender=form.cleaned_data["gender"],
                                phone=form.cleaned_data["phone"],
                                diabetes=form.cleaned_data.get("diabetes", False),
                                hypertension=form.cleaned_data.get("hypertension", False),
                                handicapped=form.cleaned_data.get("handicapped", False),
                            )

                    code = f"{random.randint(0,999999):06d}"
                    if patient:
                        patient.email_verification_code = code
                        patient.email_verified = False
                        patient.save()

                    subject = "Verify your Medical No-Show account"
                    message = f"Your verification code is: {code}\n\nEnter it in the app to verify your email address."
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [existing.email])
                    messages.info(request, "A verification code was sent to your email address.")
                except Exception:
                    messages.warning(request, "Could not send verification email.")

                return redirect("verify_email", username=existing.username)

        if form.is_valid():
            # Create the user but keep inactive until verification completes
            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.is_active = False
            user.save()

            # Create the patient row
            from appointments.models import Patient

            patient = Patient.objects.create(
                user=user,
                birth_date=form.cleaned_data["birth_date"],
                gender=form.cleaned_data["gender"],
                phone=form.cleaned_data["phone"],
                diabetes=form.cleaned_data.get("diabetes", False),
                hypertension=form.cleaned_data.get("hypertension", False),
                handicapped=form.cleaned_data.get("handicapped", False),
            )

            # Generate a verification code and send it
            try:
                code = f"{random.randint(0,999999):06d}"
                patient.email_verification_code = code
                patient.email_verified = False
                patient.save()

                subject = "Verify your Medical No-Show account"
                message = f"Your verification code is: {code}\n\nEnter it in the app to verify your email address."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            except Exception:
                messages.warning(request, "Account created but email verification could not be sent.")

            return redirect("verify_email", username=user.username)

    else:

        form = PatientRegistrationForm()

    return render(request, "registration/register.html",
        {
            "form": form
        }
    )


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def verify_email(request, username):
    user = User.objects.filter(username=username).first()
    if not user or not hasattr(user, "patient"):
        messages.error(request, "Invalid verification link.")
        return redirect("login")

    patient = user.patient

    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        if code and patient.email_verification_code and code == patient.email_verification_code:
            patient.email_verified = True
            patient.email_verification_code = None
            patient.save()
            # Activate user and log them in
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Email verified successfully.")
            return redirect("dashboard:redirect")
        else:
            messages.error(request, "Verification code is incorrect.")

    return render(request, "registration/verify_email.html", {"username": username})


def resend_code(request, username):
    user = User.objects.filter(username=username).first()
    if not user or not hasattr(user, "patient"):
        messages.error(request, "Invalid user for resending code.")
        return redirect("register")

    if user.is_active:
        messages.info(request, "Account already active.")
        return redirect("login")

    patient = user.patient
    try:
        code = f"{random.randint(0,999999):06d}"
        patient.email_verification_code = code
        patient.email_verified = False
        patient.save()

        subject = "Verify your Medical No-Show account"
        message = f"Your verification code is: {code}\n\nEnter it in the app to verify your email address."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        messages.success(request, "Verification code resent.")
    except Exception:
        messages.error(request, "Could not resend verification code.")

    return redirect("verify_email", username=username)