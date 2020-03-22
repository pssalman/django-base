__author__ = 'anton.salman@gmail.com'

import os

from importlib import import_module

from django.core.management.templates import TemplateCommand
from django.core.management.base import CommandError
from django.conf import settings

APP_TEMPLATE_URL = "https://github.com/pssalman/scripts/releases/download/v1.0/"


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def validate_name(self, name, name_or_dir='name'):
        if name is None:
            raise CommandError('you must provide {an} {app} name'.format(
                an=self.a_or_an,
                app=self.app_or_project,
            ))
        # Check it's a valid directory name.
        if not name.isidentifier():
            raise CommandError(
                "'{name}' is not a valid {app} {type}. Please make sure the "
                "{type} is a valid identifier.".format(
                    name=name,
                    app=self.app_or_project,
                    type=name_or_dir,
                )
            )
        # Check it cannot be imported.
        try:
            import_module(name, __name__)
        except ImportError:
            pass
        else:
            raise CommandError(
                "'{name}' conflicts with the name of an existing Python "
                "module and cannot be used as {an} {app} {type}. Please try "
                "another {type}.".format(
                    name=name,
                    an=self.a_or_an,
                    app=self.app_or_project,
                    type=name_or_dir,
                )
            )

    def handle(self, **options):
        app_name = options.pop('name')
        directory = options.pop('directory')

        if directory is None:
            directory = os.path.join(settings.APPS_ROOT, app_name)
        if os.path.exists(directory):
            raise CommandError(f"App with name {app_name} already exists")

        try:
            options["template"] = self.get_template()
            os.chdir(os.path.dirname(directory))
            super(Command, self).handle('app', name=app_name, target=None, **options)
        except CommandError as ex:
            raise ex

    @staticmethod
    def get_template():
        if "rest_framework" in settings.INSTALLED_APPS:
            filename = "startapp_drf.tar.gz"
        else:
            filename = "startapp.tar.gz"
        return APP_TEMPLATE_URL + filename
