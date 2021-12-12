from django import forms

from organisation.models import OrganisationEntity


class UpdateOrganisationEntityForm(forms.ModelForm):
    class Meta:
        model = OrganisationEntity
        fields = [
            "name",
            "short_name",
            "parent",
        ]


class CreateOrganisationEntityForm(forms.ModelForm):
    class Meta:
        model = OrganisationEntity
        fields = [
            "name",
            "short_name",
            "parent",
        ]
