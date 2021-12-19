from django.contrib import admin
from django_admin_json_editor import JSONEditorWidget
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin,
    PolymorphicChildModelFilter,
    StackedPolymorphicInline,
    PolymorphicInlineSupportMixin,
    GenericStackedPolymorphicInline,
)

from claims.models import ClaimType, ValueClaim, Claim, Entity, RelationshipClaim
from organisation.models import OrganisationEntity
from person.models import Person

admin.site.register(ClaimType)


class ClaimsInline(GenericStackedPolymorphicInline):
    class ValueClaimInline(GenericStackedPolymorphicInline.Child):
        model = ValueClaim

        def get_form(self, request, obj=None, **kwargs):
            if not obj:
                schema = {
                    "type": "array",
                    "title": "Please create the claim before editing the data",
                    "items": {},
                }
            else:
                schema = obj.claim_type.value_schema
            widget = JSONEditorWidget(schema, False)
            form = super().get_form(request, obj, widgets={"value": widget}, **kwargs)
            return form

    class RelationshipClaimInline(GenericStackedPolymorphicInline.Child):
        model = RelationshipClaim

    model = Claim
    child_inlines = (ValueClaimInline, RelationshipClaimInline)


@admin.register(OrganisationEntity)
class OrganisationEntityAdmin(
    PolymorphicInlineSupportMixin, PolymorphicChildModelAdmin
):
    show_in_index = True
    base_model = Entity
    inlines = [ClaimsInline]
    search_fields = ["name"]
    list_filter = ["parent"]
    autocomplete_fields = ["parent"]


@admin.register(Person)
class PersonAdmin(PolymorphicInlineSupportMixin, PolymorphicChildModelAdmin):
    show_in_index = True
    base_model = Entity
    inlines = [ClaimsInline]


@admin.register(Entity)
class EntityAdmin(PolymorphicInlineSupportMixin, PolymorphicParentModelAdmin):
    """The parent model admin"""

    base_model = Entity
    child_models = (OrganisationEntity, PersonAdmin)
    inlines = [ClaimsInline]
