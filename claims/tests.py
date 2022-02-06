import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from claims.models import ClaimType
from claims.services import ValueClaimService, ClaimServiceException
from organisation.services import OrganisationEntityService
from person.services import PersonService

import jsonschema.exceptions


VALIDATION_JSON = """{"name": null, "type": "object", "title": "Dial Code", "required": ["dialCode"], "properties": {"dialCode": {"type": "string", "title": "dialCode", "description": "Dial Code (e.g. 1312)"}}}"""


class TestValueClaimService(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_user("admin", "admin@test.com", "pass")
        self.adminuser.save()
        self.adminuser.is_superuser = True
        self.adminuser.save()
        self.person = PersonService.create_person(self.adminuser, "Dr. Test")
        self.test_claim_type = ClaimType(
            name="testclaim",
            code_name="testClaim",
            value_schema=json.loads(VALIDATION_JSON),
        )
        self.test_claim_type.save()
        self.test_claim_type.content_type.set(
            ContentType.objects.filter(app_label="person", model="person")
        )
        self.test_organization = OrganisationEntityService.create_organisation_entity(
            self.adminuser, "TestOrg"
        )

    def test_create_claim(self):
        claim_value = {"dialCode": "22222"}
        claim = ValueClaimService.create_value_claim(
            self.adminuser, self.person.pk, self.test_claim_type.pk, claim_value
        )
        self.assertEqual(claim.value, claim_value)

    def test_create_wrongly_formed_claim(self):
        claim_value = {"ac": "ab"}
        with self.assertRaisesMessage(
            jsonschema.exceptions.ValidationError, "'dialCode' is a required property"
        ):
            claim = ValueClaimService.create_value_claim(
                self.adminuser, self.person.pk, self.test_claim_type.pk, claim_value
            )

    def test_create_wrong_entity_type(self):
        claim_value = {"dialCode": "22222"}
        with self.assertRaisesMessage(
            ClaimServiceException,
            "Entity Type organisation | organisation entity is not supported by claim 'testclaim'(supported: person)",
        ):
            claim = ValueClaimService.create_value_claim(
                self.adminuser,
                self.test_organization.pk,
                self.test_claim_type.pk,
                claim_value,
            )
