"""Forms module."""

from django import forms


class CreateStudentForm(forms.Form):
    """Form to create student."""

    username = forms.CharField(min_length=1, max_length=150, required=True)
    first_name = forms.CharField(min_length=1, max_length=150, required=True)
    last_name = forms.CharField(min_length=1, max_length=150, required=True)
    password = forms.CharField(
        min_length=1,
        max_length=150,
        widget=forms.PasswordInput(),
        required=True,
    )
    group = forms.CharField(min_length=1, max_length=8, required=True)
    telegram_id = forms.IntegerField(max_value=None, min_value=0, required=True)
    settings = forms.JSONField(required=False)


class EditStudentForm(forms.Form):
    """Form to edit student."""

    username = forms.CharField(min_length=1, max_length=150, required=True)
    first_name = forms.CharField(min_length=1, max_length=150, required=True)
    last_name = forms.CharField(min_length=1, max_length=150, required=True)
    group = forms.CharField(min_length=1, max_length=8, required=True)
    telegram_id = forms.IntegerField(max_value=None, min_value=0, required=True)
    settings = forms.JSONField(required=False)
