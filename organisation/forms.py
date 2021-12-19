from django import forms

from organisation.models import OrganisationEntity, OrganisationAddress


class UpdateOrganisationEntityForm(forms.ModelForm):
    class Meta:
        model = OrganisationEntity
        fields = [
            "name",
            "short_name",
            "parent",
            "locations"
        ]


class CreateOrganisationEntityForm(forms.ModelForm):
    class Meta:
        model = OrganisationEntity
        fields = [
            "name",
            "short_name",
            "parent",
            "locations"
        ]


class UpdateOrganisationAddressForm(forms.ModelForm):
    class Meta:
        model = OrganisationAddress
        fields = [
            "name",
            "street",
            "city",
            "postal_code",
            "country",
        ]


class CreateOrganisationAddressForm(forms.ModelForm):
    class Meta:
        model = OrganisationAddress
        fields = [
            "name",
            "street",
            "city",
            "postal_code",
            "country",
        ]
