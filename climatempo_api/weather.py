"""
Módulo de clima: busca dados meteorológicos atuais a partir de coordenadas geográficas.
Utiliza a API gratuita Open-Meteo (sem necessidade de chave API).
"""

import requests

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Tabela de descrições para os códigos WMO de condição climática
WMO_DESCRIPTIONS = {
    0: "Céu limpo",
    1: "Principalmente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Neblina",
    48: "Neblina com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa intensa",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Granizo",
    80: "Pancadas de chuva leve",
    81: "Pancadas de chuva moderada",
    82: "Pancadas de chuva forte",
    85: "Pancadas de neve leve",
    86: "Pancadas de neve forte",
    95: "Tempestade",
    96: "Tempestade com granizo leve",
    99: "Tempestade com granizo forte",
}


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Busca dados meteorológicos atuais para as coordenadas fornecidas.

    Args:
        latitude: Latitude da localização.
        longitude: Longitude da localização.

    Returns:
        Dicionário com temperature, feels_like, humidity, wind_speed,
        wind_direction, precipitation, description e timezone.

    Raises:
        requests.exceptions.Timeout: Se a requisição exceder o tempo limite.
        requests.exceptions.HTTPError: Se a API retornar erro HTTP.
        requests.exceptions.ConnectionError: Se não houver conexão com a internet.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "precipitation",
        ],
        "timezone": "auto",
        "forecast_days": 1,
    }

    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    current = data.get("current", {})

    weather_code = current.get("weather_code", -1)
    description = WMO_DESCRIPTIONS.get(weather_code, "Condição desconhecida")

    return {
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m"),
        "precipitation": current.get("precipitation"),
        "weather_code": weather_code,
        "description": description,
        "timezone": data.get("timezone", ""),
    }
