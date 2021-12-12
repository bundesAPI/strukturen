from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.conf import settings

from serious_django_permissions.management.commands import (
    create_groups,
    create_permissions,
)

from oauth.services import UserProfileService


class UserProfileServiceTest(TestCase):
    def setUp(self):
        create_permissions.Command().handle()
        create_groups.Command().handle()
        self.test_user = get_user_model().objects.create_user(
            username="tester", password="refefe"
        )

    def test_update_profile_basic_information(self):
        user = UserProfileService.update_user_basic_information(
            self.test_user, first_name="Bernd", last_name="Lauert", language="de-DE"
        )
        self.assertEqual(user.first_name, "Bernd")
        self.assertEqual(user.last_name, "Lauert")
        self.assertEqual(user.profile.language, "de-DE")

    def test_get_available_languages(self):
        languages = UserProfileService.get_available_language(self.test_user)
        self.assertEqual(len(languages), len(settings.LANGUAGES))
