__author__ = 'anton.salman@gmail.com'

import time

from django.db import connection, connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that waits for database to be available"""

    help = 'Wait for database connection'

    def handle(self, *args, **options):
        """Handle the wait_for_db command"""

        #if connection.connection is not None:
        #    connection.close()

        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(
                    'Database unavailable, waiting 1 second...'
                )
                time.sleep(1)
        #while True:
        #    try:
        #        connection.ensure_connection()
        #        #db_conn = True
        #    except OperationalError:
        #        self.stdout.write(
        #            'Database unavailable, waiting 1 second...'
        #        )
        #        time.sleep(1)
        #    else:
        #        # Connection made, now close it.
        #        connection.close()
        #        break

        self.stdout.write(self.style.SUCCESS('Database available!'))
