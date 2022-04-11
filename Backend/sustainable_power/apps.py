from django.apps import AppConfig


class SustainablePowerConfig(AppConfig):
    name = 'sustainable_power'

    def ready(self):
        from PriceEmissionUpdater import updater
        updater.start_price_updater()
        updater.start_emission_updater()
        updater.start_prognosed_emission_updater()
