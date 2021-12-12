from django import forms

from person.models import Person


class UpdatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "position",
            "name",
        ]


class CreatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "position",
        ]
