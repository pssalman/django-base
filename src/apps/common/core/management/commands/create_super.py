__author__ = 'anton.salman@gmail.com'

import os

from django.core.management.base import CommandError
from django.core.management.base import (
    BaseCommand,
    no_translations
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    """Django command that creates super admin user"""

    help = 'Creates super user account at runtime'

    def add_arguments(self, parser):
        """ Accept command line arguments"""

        parser.add_argument('-u', '--username', type=str, help='Define super user username')
        parser.add_argument('-e', '--email', type=str, help='Define a super user email')
        parser.add_argument('-p', '--password', type=str, help='Define super user password')

    @staticmethod
    def validate_auth_data(**kwargs):
        """ Verify super user info data"""

        #if (settings.env.str("APP_ADMIN_USER", "") != ""
        #        and settings.env.str("APP_ADMIN_PASS", "") != ""
        #        and settings.env.str("APP_ADMIN_EMAIL", "") != ""):
        #    username = settings.env.str("APP_ADMIN_USER")
        #    email = settings.env.str("APP_ADMIN_EMAIL")
        #    password = settings.env.str("APP_ADMIN_PASS")
        if kwargs["username"] and kwargs["email"] and kwargs["password"]:
            username = kwargs["username"]
            email = kwargs["email"]
            password = kwargs["password"]
        elif settings.ADMINS is None or settings.ADMINS == []:
            username = os.environ.get('ADMIN_USER', None)
            email = os.environ.get('ADMIN_EMAIL', None)
            password = os.environ.get('ADMIN_PASSWORD', None)
        elif settings.ADMINS is not None or settings.ADMINS != []:
            user = settings.ADMINS[0]
            username = user[0].replace(' ', '')
            email = user[1]
            password = os.environ.get('ADMIN_PASSWORD', '12345678')
        else:
            raise CommandError(
                "Username, email, or password is missing "
                "Please try to have them preconfigured in your application "
                "either using the settings file or environment file "
                "even you may pass them as environment variable"
            )
        if username is not None and password is not None and email is not None:
            try:
                validate_email(email)
            except ValidationError as err:
                raise (
                    "Email value is not correctly configured "
                    f"{err}"
                )
        else:
            raise ValueError
        return {"username": username, "email": email, "password": password}

    @no_translations
    def handle(self, *args, **kwargs):
        """Handles the create_super command"""

        # User = get_user_model()
        if get_user_model().objects.count() == 0:
            data = self.validate_auth_data(**kwargs)
            username = data["username"]
            email = data["email"]
            password = data["password"]

            self.stdout.write(
                self.style.NOTICE(
                    f'Creating account for {username} - {email}'
                )
            )
            try:
                admin = get_user_model().objects.create_superuser(
                    email=email, username=username,
                    password=password
                )
                admin.save()
            except CommandError as ex:
                raise ex
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully created super user account'
                    )
                )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    """Super user account can only be
                    initialized if no Account exists"""
                )
            )
