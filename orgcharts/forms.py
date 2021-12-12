from django import forms

from orgcharts.models import OrgChartURL


class UpdateOrgChartURLForm(forms.ModelForm):
    class Meta:
        model = OrgChartURL
        fields = [
            "organisation_entity",
            "url",
        ]


class CreateOrgChartURLForm(forms.ModelForm):
    class Meta:
        model = OrgChartURL
        fields = [
            "organisation_entity",
            "url",
        ]
