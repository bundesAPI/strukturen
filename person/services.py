import reversion
from django.contrib.auth.models import AbstractUser
from serious_django_services import Service, NotPassed, CRUDMixin

from person.forms import UpdatePersonForm, CreatePersonForm
from person.models import Person
from person.permissions import CanUpdatePersonPermission, CanCreatePersonPermission


class PersonServiceException(Exception):
    pass


class PersonService(Service, CRUDMixin):
    update_form = UpdatePersonForm
    create_form = CreatePersonForm

    service_exceptions = ()
    model = Person

    @classmethod
    def retrieve_person(cls, id: int) -> Person:
        """
        get a person by id
        :param id: id of the person
        :return: the person object
        """
        try:
            person = cls.model.objects.get(pk=id)
        except cls.model.DoesNotExist:
            raise PersonServiceException("Person not found.")

        return person

    @classmethod
    def create_person(
        cls, user: AbstractUser, name: str, position: id = NotPassed
    ) -> Person:
        """create a new person
        :param user: the user calling the service
        :last_name: - Last name
        :first_name: - First name (Optional)
        :returns: the newly created person instance
        """

        if not user.has_perm(CanCreatePersonPermission):
            raise PermissionError("You are not allowed to create a person.")

        with reversion.create_revision():
            person = cls._create({"name": name, "position": position})
            reversion.set_user(user)

        return person

    @classmethod
    def update_person(
        cls,
        user: AbstractUser,
        person_id: int,
        name: str = NotPassed,
        position: id = NotPassed,
    ) -> Person:
        """create a new person
        :param user: the user calling the service
        :param person_id: - ID of the exsisting entity that should be updated
        :param name: -  name
        :param position: - position
        :return: the updated person instance
        """

        person = cls.retrieve_person(person_id)

        if not user.has_perm(CanUpdatePersonPermission, person):
            raise PermissionError("You are not allowed to update this person.")

        with reversion.create_revision():
            person = cls._update(
                person_id,
                {"name": name, "position": position},
            )
            reversion.set_user(user)
            reversion.set_comment(f"update via service by {user}")

        person.refresh_from_db()
        return person
