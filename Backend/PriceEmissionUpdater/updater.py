from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from PriceEmissionUpdater import api_handler
from sustainable_power.iot_connection import check_all_devices


def start_price_updater():
    # Update db on server-start
    api_handler.update_prices()

    # Setup and start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(api_handler.update_prices, 'cron', day_of_week='mon-sun', hour=17, minute=1)
    scheduler.start()


def start_emission_updater():
    # Update db on server-start
    api_handler.update_emissions()

    # Setup and start scheduler
    scheduler = BackgroundScheduler()

    # Sync time to run at exact 5 minutes intervals (e.g. 10:05:05, 10:10:05, 10:15:05)
    synced_time = sync_time_5_minute_intervals()

    scheduler.add_job(api_handler.update_emissions, 'interval', start_date=synced_time, minutes=5)
    scheduler.start()


def start_prognosed_emission_updater():
    # Update db on server-start
    api_handler.update_prognosed_emissions()

    # Setup and start scheduler
    scheduler = BackgroundScheduler()

    # Sync time to run at exact 5 minutes intervals (e.g. 10:05:05, 10:10:05, 10:15:05)
    synced_time = sync_time_5_minute_intervals()

    scheduler.add_job(api_handler.update_prognosed_emissions, 'interval', start_date=synced_time, minutes=5)
    scheduler.add_job(check_all_devices, 'interval', start_date=synced_time, minutes=5)
    scheduler.start()


# Helper functions
def sync_time_5_minute_intervals():
    time = datetime.now().time()
    minutes_left = 5 - (datetime.now().time().minute % 5)
    synced_minute = (time.minute + minutes_left) % 60
    synced_hour = datetime.now().hour
    
    if time.minute + minutes_left >= 60:
        synced_hour += 1

    synced_time = datetime.now().replace(hour=synced_hour, minute=synced_minute, second=5, microsecond=0)

    return synced_time
