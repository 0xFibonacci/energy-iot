import requests
from django.db.utils import IntegrityError

from sustainable_power.serializers import PrognosedPriceSerializer, PrognosedEmissionSerializer, EmissionSerializer
from sustainable_power.models import PrognosedPrice, Emission, PrognosedEmission

from django.utils.dateparse import parse_datetime
from datetime import datetime

DEFAULT_TIMESTAMP = parse_datetime('2020-11-01T20:00:00')


def call_api(url):
    response = requests.get(url)

    try:
        response.raise_for_status()

        parsed_response = response.json()
        result = parsed_response['result']['records']
        result.reverse()
        return result
    except requests.exceptions.RequestException:
        return None


def get_prices(timestamp):
    url = 'https://www.energidataservice.dk/proxy/api/datastore_search_sql?sql=' \
          'SELECT "HourUTC", "HourDK", "PriceArea", "SpotPriceDKK", "SpotPriceEUR" ' \
          'FROM "elspotprices" ' \
          f'WHERE ("PriceArea" = \'DK2\' OR "PriceArea" = \'DK1\') AND "HourDK" > \'{timestamp}\' ' \
          'ORDER BY "HourDK" DESC'

    return call_api(url)


def get_emissions(timestamp):
    url = 'https://www.energidataservice.dk/proxy/api/datastore_search_sql?sql=' \
          'SELECT "Minutes5UTC", "Minutes5DK", "PriceArea", "CO2Emission" ' \
          'FROM "co2emis" ' \
          f'WHERE "Minutes5DK" > \'{timestamp}\' ' \
          'ORDER BY "Minutes5UTC" DESC'

    return call_api(url)


def get_prognosed_emissions(timestamp):
    url = 'https://www.energidataservice.dk/proxy/api/datastore_search_sql?sql=' \
          'SELECT "Minutes5UTC", "Minutes5DK", "PriceArea", "CO2Emission" ' \
          f'FROM "co2emisprog" WHERE "Minutes5DK" > \'{timestamp}\' ' \
          'ORDER BY "Minutes5UTC" DESC'

    return call_api(url)


def update_prices():
    latest_db_timestamp = latest_price_timestamp()

    if latest_db_timestamp is not None:
        price_json = get_prices(latest_db_timestamp)
    else:
        price_json = get_prices(DEFAULT_TIMESTAMP)

    # Check dkk price is not Null
    price_json = eur_dkk_converter(price_json)

    price_serializer = PrognosedPriceSerializer(data=price_json, many=True)

    if price_serializer.is_valid():
        price_serializer.save()


def update_emissions():
    #Emission.objects.all().delete()

    latest_db_timestamp = latest_emission_timestamp()

    if latest_db_timestamp is not None:
        emission_json = get_emissions(latest_db_timestamp)
    else:
        emission_json = get_emissions(DEFAULT_TIMESTAMP)

    emission_serializer = EmissionSerializer(data=emission_json, many=True)

    if emission_serializer.is_valid():
        try:
            emission_serializer.save()
        # Catch when it's already in db..........
        except IntegrityError:
            pass


def update_prognosed_emissions():
    #PrognosedEmission.objects.all().delete()

    latest_db_timestamp = latest_prog_emission_timestamp()

    if latest_db_timestamp is not None:
        timestamp_now = datetime.now()

        # None of the data to retrieve is in db yet, so we append everything
        if timestamp_now > latest_db_timestamp:
            prog_emission_json = get_prognosed_emissions(latest_db_timestamp)

            prog_emission_serializer = PrognosedEmissionSerializer(data=prog_emission_json, many=True)

            if prog_emission_serializer.is_valid():
                prog_emission_serializer.save()
        # Some of the data/all of the data is already in db, so we update/append if necessary
        else:
            prog_emission_json = get_prognosed_emissions(timestamp_now)
            prog_emissions_not_in_db = [prog_emission for prog_emission in prog_emission_json if parse_datetime(prog_emission['Minutes5DK']) > latest_db_timestamp]
            prog_emissions_to_update = [prog_emission for prog_emission in prog_emission_json if parse_datetime(prog_emission['Minutes5DK']) <= latest_db_timestamp]

            # Append prognosed emissions not yet in db
            prog_emission_serializer = PrognosedEmissionSerializer(data=prog_emissions_not_in_db, many=True)

            if prog_emission_serializer.is_valid():
                prog_emission_serializer.save()

            # Update if the emission has changed, for every timestamp
            for prog_emission_data in prog_emissions_to_update:
                prog_emission_obj = PrognosedEmission.objects.get(Minutes5DK=prog_emission_data['Minutes5DK'],
                                                                  PriceArea=prog_emission_data['PriceArea'])
                if prog_emission_obj.CO2Emission != prog_emission_data['CO2Emission']:
                    prog_emission_serializer = PrognosedEmissionSerializer(prog_emission_obj, data=prog_emission_data)

                    if prog_emission_serializer.is_valid():
                        prog_emission_serializer.save()
    # No data in db yet, append everything
    else:
        prog_emission_json = get_prognosed_emissions(DEFAULT_TIMESTAMP)
        prog_emission_serializer = PrognosedEmissionSerializer(data=prog_emission_json, many=True)

        if prog_emission_serializer.is_valid():
            prog_emission_serializer.save()


# Helper functions
    # Converts from Eur to Dkk if Dkk price is not provided by the API
def eur_dkk_converter(prices):
    for price in prices:
        if not price['SpotPriceDKK']:
            price['SpotPriceDKK'] = price['SpotPriceEUR'] * 7.44

    return prices


def latest_price_timestamp():
    if PrognosedPrice.objects.count() > 0:
        last_price_db = PrognosedPrice.objects.last()

        last_price_db.HourDK = last_price_db.HourDK.replace(tzinfo=None)

        return last_price_db.HourDK
    else:
        return None


def latest_emission_timestamp():
    if Emission.objects.count() > 0:
        last_emission_db = Emission.objects.last()

        last_emission_db.Minutes5DK = last_emission_db.Minutes5DK.replace(tzinfo=None)

        return last_emission_db.Minutes5DK
    else:
        return None


def latest_prog_emission_timestamp():
    if PrognosedEmission.objects.count() > 0:
        last_emission_db = PrognosedEmission.objects.last()

        last_emission_db.Minutes5DK = last_emission_db.Minutes5DK.replace(tzinfo=None)

        return last_emission_db.Minutes5DK
    else:
        return None
