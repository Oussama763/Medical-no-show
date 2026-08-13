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
            )

        return user