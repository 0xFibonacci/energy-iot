from django.core.management.base import BaseCommand
from PriceEmissionUpdater import api_handler
from sustainable_power.models import Region


class Command(BaseCommand):
    args = ''
    help = 'Makes the initial population of the database.'

    def _populate_db(self):
        # self.populate_price_emissions()
        self.populate_regions()

    '''
    def populate_price_emissions(self):
        api_handler.update_prices()
        api_handler.update_emissions()
        api_handler.update_prognosed_emissions()
    '''

    def populate_regions(self):
        for region_name in Region.Regions:
            region = Region(name=region_name)
            region.save()

    def handle(self, *args, **options):
        self._populate_db()
