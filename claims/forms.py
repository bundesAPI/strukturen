from django import forms

from claims.models import ValueClaim
from organisation.models import OrganisationEntity


class UpdateValueClaimForm(forms.ModelForm):
    class Meta:
        model = ValueClaim
        fields = [
            "value",
        ]


class CreateValueClaimForm(forms.ModelForm):
    class Meta:
        model = ValueClaim
        fields = [
            "value",
        ]
