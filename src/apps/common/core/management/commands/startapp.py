__author__ = 'anton.salman@gmail.com'

import os
import shutil

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands import startapp


DS_BE_APP_TEMPLATE = "https://github.com/pssalman/scripts/releases/download/v1.0/startapp{extensions}.tar.gz"
# "https://be.skeletons.djangostars.com/djangostars_app_template__django{extensions}.tar.gz"


class Command(startapp.Command):
    def handle(self, **options):
        app_name = options.pop("name")

        if options["directory"] is None:
            directory = os.path.join(settings.APPS_ROOT, app_name)
        else:
            directory = options["directory"]
        if os.path.exists(directory):
            raise CommandError(f"App with name {app_name} already exists")        
        try:
            os.mkdir(directory)
        except Exception as err:
            raise err

        options["template"] = self.get_template()
        options["directory"] = directory
        options["project_name"] = settings.SITE_NAME
        # options["project_name"] = settings.ROOT_URLCONF.split(".", 1)[0]

        try:
            super(Command, self).handle(name=app_name, **options)
        except CommandError as ex:
            shutil.rmtree(directory)
            raise ex

    @staticmethod
    def get_template():
        extensions = []
        if "rest_framework" in settings.INSTALLED_APPS:
            extensions.append("drf")

        return DS_BE_APP_TEMPLATE.format(extensions="_{}".format(
            "_".join(extensions)) if len(extensions) > 0 else "")
