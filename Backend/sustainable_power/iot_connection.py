from datetime import datetime

import bluetooth
import socket
import time

from sustainable_power.models import Device, Emission, PrognosedPrice, Value
from sustainable_power.serializers import DeviceSerializer, ValueSerializer


def find_device_addr(device_name, retries=0):
    # If there is No Device attached we just return False
    if device_name == "No Device":
        return False

    # Max amount of times we will try
    max_retries = 1

    # If we have tried to get in contact 5 times we return none
    if retries >= max_retries:
        return False

    # Find nearby bluetooth devices
    nearby_devices = bluetooth.discover_devices(lookup_names=True)

    device_addr = ""

    # Go through every device in the nearby area
    for device in nearby_devices:
        # If the device name matches with the one we are looking for
        if device[1] == device_name:
            # Set the address to the corresponding address
            device_addr = device[0]

    # If we could not find a device address, we try again
    if device_addr == "":
        print("Couldn't find device " + str(device_name) + ", trying again " + str(retries + 1) + " out of " + str(
            max_retries) + " tries.")
        return find_device_addr(device_name, retries + 1)

    return device_addr


def send_message_receive_message(device_addr, msg):
    # Specify a port - 1 is arbitrarily chosen meaning you can choose any port
    port = 1
    # Create a socket
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    # Connect to the socket
    sock.connect((device_addr, port))
    # If 10 seconds goes by without connection to the socket we consider the socket disconnected
    sock.settimeout(10.0)

    # Ask the device if it is ready
    sock.send(bytes(msg, 'UTF-8'))

    # Save the current time so we can count up from here
    current_time = time.time()
    # How long we will wait for a ready call from the device
    timeout_for_ready_call = 10

    # Specify received message
    received_message = ""
    # Wait for data to be received and continue reading the data until the null character is received
    while (received_message == "" or received_message[len(received_message) - 1] != '\0') and \
            time.time() - timeout_for_ready_call < current_time:
        # sock.recv halts the process until anything is received
        # It appends it to data as we have not necessarily received all the data yet
        received_message += sock.recv(1024).decode("UTF-8")

    # Close the socket
    sock.close()

    # Return the received message excluding the very last character as that's a null character
    return received_message[0:-1]


def ask_if_ready(device_name):
    # Find the address of the device
    device_addr = find_device_addr(device_name)

    # If we got False back we return False to say that we did not manage to complete the task
    if device_addr is False:
        return False

    # Send the message "Ready" to the device and save the received message in ready_state
    ready_state = send_message_receive_message(device_addr, "Ready?")

    # If the ready_state is true we set the ready_state to True otherwise we set it to False
    if "true" in ready_state.lower():
        ready_state = True
    else:
        ready_state = False

    # We return ready_state as this contains True if the device is ready or False if there was an error
    return ready_state


def ask_for_value(device_name):
    # Find the address of the device
    device_addr = find_device_addr(device_name)

    # If we got False back we return False to say that we did not manage to complete the task
    if device_addr is False:
        return False

    # Send the message "Value" to the device and save the received message in value
    value = send_message_receive_message(device_addr, "Value")

    # If the value is false we set value to None as nothing could be received
    if "false" in value.lower():
        value = None

    # We return value as this contains the value received
    return value


def start_device(device_name):
    # Find the address of the device
    device_addr = find_device_addr(device_name)

    # If we got False back we return False to say that we did not manage to complete the task
    if device_addr is False:
        return False

    # Send the message "Start" to the device and save the received message in start_state
    start_state = send_message_receive_message(device_addr, "Start")

    # If the start_state is true we set the start_state to True otherwise we set it to False
    if start_state.lower() == "true":
        start_state = True
    else:
        start_state = False

    # We return start_state as this contains True if the device has started or False if there was an error
    return start_state


def stop_device(device_name):
    # Find the address of the device
    device_addr = find_device_addr(device_name)

    # If we got False back we return False to say that we did not manage to complete the task
    if device_addr is False:
        return False

    # Send the message "Stop" to the device and save the received message in stop_state
    stop_state = send_message_receive_message(device_addr, "Stop")

    # If the start_state is true we set the start_state to True otherwise we set it to False
    if stop_state.lower() == "true":
        start_state = True
    else:
        start_state = False

    # We return stop_state as this contains True if the device has stopped or False if there was an error
    return start_state


def test_device(device_name):
    # Find the address of the device
    device_addr = find_device_addr(device_name)

    # If we got False back we return False to say that we did not manage to complete the task
    if device_addr is False:
        return False

    # Send the message "Connected" to the device and return the message received
    return send_message_receive_message(device_addr, "Connected")


def check_all_devices():
    # Get all devices from the database
    devices = Device.objects.all()

    # Check every device one by one
    for device in devices:
        check_device(device)


def check_device(device, prev_ready=False):
    # Find the ready state of the device
    ready_state = ask_if_ready(device.bluetooth_address)

    # Ask for the value the device currently has
    value_from_device = ask_for_value(device.bluetooth_address)

    # Update the device with the ready state and the value
    updated_device = Device.objects.get(pk=device.id)
    value = Value.objects.get(device=updated_device)
    updated_device.ready = ready_state
    value.value = float(value_from_device)

    # Send the updated device and value to the database
    device_serializer = DeviceSerializer(updated_device, data=vars(updated_device))
    value_serializer = ValueSerializer(value, data=vars(value))

    # Update the device and value in the database
    if device_serializer.is_valid():
        device_serializer.save()
    if value_serializer.is_valid():
        value_serializer.save()

    # Check ready state, if it is false we just stop here because we are not going to turn it on anyway
    if ready_state is False:
        return

    # Get the current time
    current_time = datetime.now()

    # Check allowed on time - allowed on time is on from hh:mm-hh:mm
    # Split it into start and end
    start_time = device.allowed_on_time.split('-')[0]
    end_time = device.allowed_on_time.split('-')[1]

    # If it is not within the allowed time we return
    if within_start_end_time(current_time, start_time, end_time) is False:
        return

    # Check should be done before
    # - If time before it should be done is getting critically low, turn it on despite anything else
    # - We check if time is getting critically low by adding teh time to complete to our current time
    # - As well as 5 more minutes, just to make sure we finish the task before it is supposed to
    hour = current_time.hour
    minute = (current_time.minute + device.time_to_complete + 5) % 60
    if current_time.minute + device.time_to_complete + 5 >= 60:
        hour = (current_time.hour + 1) % 24
    if before_timestamp(current_time.replace(hour=hour, minute=minute),
                        device.completed_before):
        # If we are before this time, i.e. it's not critical, we pass as we don't need to start it yet
        pass
    else:
        start_device(device.bluetooth_address)

    # Check preferred CO2 emission, if the latest emission is higher than the preferred emission, we return
    emissions = Emission.objects.all().order_by('Minutes5DK')
    if emissions.last().CO2Emission > device.preferred_emission:
        return

    # Check preferred Price, if the price is higher than the preferred price, we return
    current_active_price_time = current_time
    current_price = PrognosedPrice.objects.get(
        HourDK=current_active_price_time.replace(minute=0, second=0, microsecond=0), PriceArea="DK1")
    if current_price.SpotPriceDKK > device.preferred_price:
        return

    # If all is good turn it on, otherwise we have already returned at some point and will do nothing
    start_device(device.bluetooth_address)
    return


def within_start_end_time(current_time, start_time, end_time):
    # Split it up into the four different values that show hour and minute for each time
    start_hour = int(start_time.split(':')[0])
    start_minute = int(start_time.split(':')[1])
    end_hour = int(end_time.split(':')[0])
    end_minute = int(end_time.split(':')[1])

    if (current_time.hour > start_hour or (current_time.hour >= start_hour and current_time.minute >= start_minute)) \
            and (current_time.hour < end_hour or (current_time.hour <= end_hour and current_time.minute <= end_minute)):
        # We return True if the current time is within the start and end time
        return True
    else:
        # We return False if the current time is not within the start and end time
        return False


def before_timestamp(current_time, timestamp):
    if current_time.isoformat() < timestamp.isoformat():
        return True
    return False
