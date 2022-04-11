from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField

from sustainable_power.models import *


class UserSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id',
                  'email',
                  'password',
                  'default_price',
                  'default_emission',
                  'region')


'''
class UserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'city',
                  'username',
                  'email',
                  'password')
'''


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = ('pref_min_value',
                  'pref_max_value',
                  'value',
                  'increase_decrease',
                  'device')


class DeviceSerializer(serializers.ModelSerializer):
    value = ValueSerializer(required=False)

    class Meta:
        model = Device
        fields = ('id',
                  'name',
                  'ready',
                  'completed_before',
                  'time_to_complete',
                  'allowed_on_time',
                  'energy_consumption',
                  'preferred_price',
                  'preferred_emission',
                  'bluetooth_address',
                  'user',
                  'value')

    def create(self, validated_data):

        try:
            value_data = validated_data.pop('value')
            device = Device.objects.create(**validated_data)

            Value.objects.create(device=device, **value_data)
        except KeyError:
            device = Device.objects.create(**validated_data)
            return device

        return device

    def update(self, instance, validated_data):
        try:
            value_data = validated_data.pop('value')
            value = instance.value

            for key, v in value_data.items():
                setattr(value, key, v)
            value.save()

            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()

            return instance
        except KeyError:

            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()

            return instance


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id',
                  'region')


class PrognosedPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrognosedPrice
        fields = ('HourDK',
                  'SpotPriceDKK',
                  'PriceArea')


class EmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emission
        fields = ('Minutes5DK',
                  'CO2Emission',
                  'PriceArea')


class PrognosedEmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrognosedEmission
        fields = ('Minutes5DK',
                  'CO2Emission',
                  'PriceArea')


"""
class PrognosedPriceSerializer(serializers.ModelSerializer):

    # HourDK = serializers.DateTimeField(source='date_time')
    # SpotPriceDKK = serializers.FloatField(source='price')
    # PriceArea = serializers.FloatField(source='area')

    # date_time = serializers.DateTimeField(source='HourDK')
    price = serializers.FloatField(source='SpotPriceEUR')
    area = serializers.CharField(source='PriceArea')

    class Meta:
        model = PrognosedPrice
        fields = ('price',
                  'area')
"""