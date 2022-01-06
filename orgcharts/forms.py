from django import forms

from orgcharts.models import OrgChartURL, OrgChartError, OrgChart


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


class CreateOrgChartErrorForm(forms.ModelForm):
    class Meta:
        model = OrgChartError
        fields = [
            "org_chart_url",
            "message",
        ]


class UpdateOrgChartErrorForm(forms.ModelForm):
    class Meta:
        model = OrgChartError
        fields = [
            "status",
        ]


class CreateOrgChartForm(forms.ModelForm):
    class Meta:
        model = OrgChart
        fields = [
            "org_chart_url",
            "document",
            "document_hash",
        ]


class UpdateOrgChartForm(forms.ModelForm):
    class Meta:
        model = OrgChart
        fields = [
            "raw_source",
            "status",
        ]
