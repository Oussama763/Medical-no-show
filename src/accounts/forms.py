from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from appointments.models import Patient


class PatientRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    gender = forms.ChoiceField(
        choices=Patient.GENDER_CHOICES
    )

    phone = forms.CharField(max_length=20)

    city = forms.CharField(max_length=100, required=False)
    neighborhood = forms.CharField(max_length=150, required=False)

    # Clinical flags
    diabetes = forms.BooleanField(required=False, initial=False, label="Do you have diabetes?")
    hypertension = forms.BooleanField(required=False, initial=False, label="Do you have hypertension?")
    handicapped = forms.BooleanField(required=False, initial=False, label="Are you handicapped?")

    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "birth_date",
            "gender",
            "phone",
            "diabetes",
            "hypertension",
            "handicapped",
            "city",
            "neighborhood",
        )

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            Patient.objects.create(
                user=user,
                birth_date=self.cleaned_data["birth_date"],
                gender=self.cleaned_data["gender"],
                phone=self.cleaned_data["phone"],
                diabetes=self.cleaned_data.get("diabetes", False),
                hypertension=self.cleaned_data.get("hypertension", False),
                handicapped=self.cleaned_data.get("handicapped", False),
                city=self.cleaned_data.get("city", ""),
                neighborhood=self.cleaned_data.get("neighborhood", ""),
            )

        return user