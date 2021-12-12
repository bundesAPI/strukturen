from django.utils.crypto import get_random_string

from django.conf import settings

from serious_django_services import Service, CRUDMixin

from oauth.forms import UpdateUserProfileForm, CreateUserProfileForm
from oauth.models import UserProfile


class UserProfileService(Service, CRUDMixin):
    service_exceptions = (ValueError,)

    update_form = UpdateUserProfileForm
    create_form = CreateUserProfileForm

    model = UserProfile

    @classmethod
    def update_user_basic_information(
        cls, user, first_name=None, last_name=None, language=None
    ):
        """
        Update user basic information like name, … for the current user
        :param language: iso language code like en, de, …
        :param user:
        :param first_name: new first name of the user
        :param last_name: new last name of the user
        :return: updated user object
        """
        if first_name is not None:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        cls._update(user.profile.pk, {"language": language, "profile_setup_done": True})
        user.profile.refresh_from_db()

        user.save()
        return user

    @classmethod
    def upload_profile_picture(cls, user, picture):
        """
        Upload user profile picture for the current user
        :param user: current user
        :param picture: the new user profile picture
        :return: updated user object
        """
        # https://docs.djangoproject.com/en/2.2/howto/custom-file-storage/#django.core.files.storage.get_valid_name
        file_name, file_extension = picture.name.rsplit(".", 1)
        random_suffix = get_random_string(14)
        picture.name = f"{random_suffix}.{file_extension}"

        user.profile.profile_picture = picture
        user.profile.save()
        return user

    @classmethod
    def get_available_language(cls, user):
        """
        :param user: the user you want to retrieve the informations for
        :return: a list of available languages
        """
        languages = []
        for language in settings.LANGUAGES:
            languages.append({"language": language[1], "iso_code": language[0]})

        return languages
