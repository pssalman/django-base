__author__ = 'anton.salman@gmail.com'

import getpass
import shlex
from subprocess import PIPE  # nosec

from django.core.management.base import BaseCommand
from django.utils.autoreload import run_with_reloader

import psutil


def restart_celery():
    for proc in psutil.process_iter():
        # skip processes not owned by user
        if proc.username() != getpass.getuser():
            continue
        if proc.name() != 'celery':
            continue
        # SIGTERM should only be sent to parent process,
        # never to children processes
        # see: https://github.com/celery/celery/issues/2700#issuecomment-259716123
        if not proc.children():
            continue
        celery_proc = proc  # found parent celery process
        celery_proc.terminate()
        break
    cmd = "celery worker -A conf -l INFO"
    psutil.Popen(shlex.split(cmd), stdout=PIPE)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Starting celery worker with autoreload')
        run_with_reloader(restart_celery)
