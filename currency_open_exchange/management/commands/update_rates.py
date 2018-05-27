from django.core.management.base import BaseCommand, CommandError

from ...backends import RateBackend


class Command(BaseCommand):
    help = 'Update rates'

    def handle(self, *args, **options):
        try:
            RateBackend().update_rates()
        except Exception as e:
            raise CommandError("Error during rate update: %s" % e)

        self.stdout.write('Successfully updated rates')
