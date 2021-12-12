import reversion
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from polymorphic.models import PolymorphicModel

@reversion.register()
class Entity(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    claims = GenericRelation('Claim', content_type_field='content_type', object_id_field='object_id')
    reverse_claims = GenericRelation('RelationshipClaim', content_type_field='target_content_type', object_id_field='target_entity_id')

@reversion.register()
class ClaimType(models.Model):
    name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    content_type = models.ManyToManyField(ContentType)
    value_schema = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

@reversion.register()
class Claim(PolymorphicModel):
    claim_type = models.ForeignKey(ClaimType, on_delete=models.CASCADE, related_name="claims")
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')
    value = models.JSONField(null=True, blank=True)


    def __str__(self):
        return "Claim"

@reversion.register()
class ValueClaim(Claim):
    def __str__(self):
        return f"{self.claim_type} | {self.entity}"

@reversion.register()
class RelationshipClaim(Claim):
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_entity_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_entity_id')
    def __str__(self):
        return f"{self.claim_type} | {self.entity} -> {self.target}"

@reversion.register()
class ClaimSource(models.Model):
    claim = models.ForeignKey(Claim, related_name="sources", on_delete=models.CASCADE)
    url = models.URLField()
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ClaimSource"
