import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import APIException


def fetch_google_reviews(place_id):
    cache_key = f"google_reviews_{place_id}"
    reviews = cache.get(cache_key)
    if reviews is not None:
        return reviews

    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "reviews",
        "key": settings.GOOGLE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != "OK":
            raise APIException(f"Ошибка Google Places API: {data.get('error_message', 'Unknown error')}")
        reviews = data.get("result", {}).get("reviews", [])
        cache.set(cache_key, reviews, timeout=86400)  # Кэш на 24 часа
        return reviews
    except requests.exceptions.RequestException as e:
        raise APIException(f"Ошибка запроса к Google Places API: {str(e)}")


def fetch_geocoding_data(city_name, province="Ontario"):
    cache_key = f"geocode_{city_name}_{province}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{city_name}, {province}, Canada",
        "key": settings.GOOGLE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "OK" or not data.get("results"):
            raise APIException(f"Город {city_name} не найден")
        result = data["results"][0]
        place_id = result.get("place_id")
        latitude = result["geometry"]["location"]["lat"]
        longitude = result["geometry"]["location"]["lng"]
        geocode_data = (place_id, latitude, longitude)
        cache.set(cache_key, geocode_data, timeout=604800)
        return geocode_data
    except requests.exceptions.RequestException as e:
        raise APIException(f"Ошибка Geocoding API: {str(e)}")
