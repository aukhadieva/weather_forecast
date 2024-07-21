import openmeteo_requests

import requests_cache
import pandas as pd
from geopy import Nominatim
from retry_requests import retry

from config import settings


def get_weather(location):
    """
    Сервисная функция для получения данных о погоде по полученному городу
    """
    geolocator = Nominatim(user_agent='Weather')
    geocode_location = geolocator.geocode(location)

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': geocode_location.latitude,
        'longitude': geocode_location.longitude,
        'hourly': "temperature_2m",
        'daily': ['temperature_2m_max'],
        'timezone': settings.TIME_ZONE,
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()

    daily_data = {'date': pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive='left'
    ), 'temperature_2m_max': daily_temperature_2m_max}

    return daily_data['date'][0].date(), round(daily_data['temperature_2m_max'][0])
