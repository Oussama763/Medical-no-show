from django import forms

class DoctorCreationForm(forms.Form):

    username = forms.CharField(max_length=150)

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    first_name = forms.CharField(max_length=150)

    last_name = forms.CharField(max_length=150)

    email = forms.EmailField()

    specialization = forms.CharField(max_length=100)




class DoctorUpdateForm(forms.Form):

    first_name = forms.CharField(max_length=150)

    last_name = forms.CharField(max_length=150)

    email = forms.EmailField()

    specialization = forms.CharField(max_length=100)