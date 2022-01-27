from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import PersonPosition, PositionAbbreviation


class PositionAbbreviationInline(admin.TabularInline):
    model = PositionAbbreviation


@admin.register(PersonPosition)
class PersonPositionAdmin(VersionAdmin):
    inlines = [
        PositionAbbreviationInline,
    ]
