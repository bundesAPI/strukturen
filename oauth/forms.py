from django import forms

from oauth.models import UserProfile


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "language",
            "profile_setup_done",
        ]


class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "language",
            "profile_setup_done",
        ]
