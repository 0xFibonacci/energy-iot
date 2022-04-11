from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from sustainable_power.serializers import *

import bluetooth
import socket


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def user_list(request):
    # GET list of users, POST a new user, DELETE all users
    if request.method == 'GET':
        users = User.objects.all()

        first_name = request.GET.get('first_name', None)

        if first_name is not None:
            users = users.filter(first_name__icontains=first_name)

        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    # find user by pk (primary key / id)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # GET / PUT / DELETE user
    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def device_list(request):
    user_id = request.user.pk

    # GET list of devices, POST new device, DELETE all devices
    if request.method == 'GET':
        devices = Device.objects.filter(user=user_id)
        device_serializer = DeviceSerializer(devices, many=True)
        return JsonResponse(device_serializer.data, safe=False)

    elif request.method == 'POST':
        device_data = JSONParser().parse(request)
        device_data['user'] = user_id
        device_serializer = DeviceSerializer(data=device_data)

        if device_serializer.is_valid():
            device_serializer.save()
            return JsonResponse(device_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Device.objects.filter(user=user_id).delete()
        return JsonResponse({'message': f'{count[0]} Devices were deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def device_detail(request, pk):
    # find device på pk (primary key / id)
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        return JsonResponse({'message': 'The device does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        device_serializer = DeviceSerializer(device)
        return JsonResponse(device_serializer.data)
    elif request.method == 'PUT':
        device_data = JSONParser().parse(request)
        device_serializer = DeviceSerializer(device, data=device_data)

        if device_serializer.is_valid():
            device_serializer.save()
            return JsonResponse(device_serializer.data)
        return JsonResponse(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        device.delete()
        return JsonResponse({'message': 'Device was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def price_list(request):
    # Get list of prices
    if request.method == 'GET':
        prices = PrognosedPrice.objects.all()

        price_serializer = PrognosedPriceSerializer(prices, many=True)

        return JsonResponse(price_serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def emission_list(request):
    if request.method == 'GET':
        emissions = Emission.objects.all().order_by('Minutes5DK')

        emission_serializer = EmissionSerializer(emissions, many=True)

        return JsonResponse(emission_serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def prognosed_emission_list(request):
    if request.method == 'GET':
        prognosed_emissions = PrognosedEmission.objects.all().order_by('Minutes5DK')

        prognosed_emission_serializer = PrognosedEmissionSerializer(prognosed_emissions, many=True)

        return JsonResponse(prognosed_emission_serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bluetooth_devices(request):
    if request.method == 'GET':
        # We discover nearby devices with the parameter lookup_names set to True
        # As that makes us able to use the name of the device instead of the address in the frontend
        nearby_devices = bluetooth.discover_devices(lookup_names=True)

        # We create an array for our names so we can just send this back
        device_names = []

        # We want the names to the front end because the user is unlikely to know the address of their Bluetooth
        # Device, however they are more likely to know the name of their bluetooth device
        for device in nearby_devices:
            device_names.append(device[1])

        # Return a list of device names for the front end to display and choose from
        return JsonResponse(device_names, safe=False)