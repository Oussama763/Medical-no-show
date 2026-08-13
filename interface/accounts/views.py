from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientRegistrationForm
from django.contrib.auth.decorators import login_required


def register(request):

    if request.method == "POST":

        form = PatientRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

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