from django import forms
from appointments.models import Doctor
from appointments.models import TimeSlot
#from datetime import timedelta, datetime, time
from django.utils import timezone

class DoctorCreationForm(forms.Form):

    username = forms.CharField(max_length=150)

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    first_name = forms.CharField(max_length=150)

    last_name = forms.CharField(max_length=150)

    email = forms.EmailField()

    specialization = forms.CharField(max_length=100)

    appointment_duration = forms.IntegerField(
        min_value=5,
        max_value=180,
        initial=30,
        label="Appointment duration (minutes)"
    )



class DoctorUpdateForm(forms.Form):

    first_name = forms.CharField(max_length=150)

    last_name = forms.CharField(max_length=150)

    email = forms.EmailField()

    specialization = forms.CharField(max_length=100)

    appointment_duration = forms.IntegerField(
        min_value=5,
        max_value=180,
        initial=30,
        label="Appointment duration (minutes)"
    )




class TimeSlotForm(forms.ModelForm):

    class Meta:

        model = TimeSlot

        fields = (
            "doctor",
            "date",
            "start_time",
            "end_time",
        )

        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "start_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        doctor = cleaned_data.get("doctor")
        date = cleaned_data.get("date")
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")

        if not all([doctor, date, start, end]):
            return cleaned_data

        today = timezone.localdate()

        if start >= end:
            raise forms.ValidationError(
                "Start time must be before end time."
            )

        if date < today:
            raise forms.ValidationError(
                "You cannot create a time slot in the past."
            )


        overlapping = TimeSlot.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end,
            end_time__gt=start,
        )

        if self.instance.pk:
            overlapping = overlapping.exclude(
                pk=self.instance.pk
            )

        if overlapping.exists():
            raise forms.ValidationError(
                "This time slot overlaps with another slot for this doctor."
            )

        return cleaned_data





class TimeSlotGenerationForm(forms.Form):

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.select_related("user").all()
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    work_start = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    work_end = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    
    break_start = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    break_end = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    def clean(self):

        cleaned_data = super().clean()

        work_start = cleaned_data.get("work_start")
        work_end = cleaned_data.get("work_end")
        break_start = cleaned_data.get("break_start")
        break_end = cleaned_data.get("break_end")

        if work_start and work_end and work_start >= work_end:
            raise forms.ValidationError(
                "Working day must start before it ends."
            )

        # Either both break fields are filled or neither.
        if bool(break_start) != bool(break_end):
            raise forms.ValidationError(
                "Please specify both break start and break end."
            )

        if break_start and break_end:

            if break_start >= break_end:
                raise forms.ValidationError(
                    "Break must start before it ends."
                )

            if break_start < work_start:
                raise forms.ValidationError(
                    "Break cannot start before the working day."
                )

            if break_end > work_end:
                raise forms.ValidationError(
                    "Break cannot end after the working day."
                )

        return cleaned_data




class AppointmentBookingForm(forms.Form):

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )