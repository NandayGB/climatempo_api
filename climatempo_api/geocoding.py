"""
Módulo de geocodificação: converte nome de cidade em coordenadas geográficas.
Utiliza a API gratuita Open-Meteo Geocoding (sem necessidade de chave API).
"""

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_coordinates(city_name: str) -> dict:
    """
    Obtém latitude e longitude para um nome de cidade.

    Args:
        city_name: Nome da cidade a ser pesquisada.

    Returns:
        Dicionário com name, country, admin1, latitude e longitude.

    Raises:
        ValueError: Se city_name estiver vazio ou a cidade não for encontrada.
        requests.exceptions.Timeout: Se a requisição exceder o tempo limite.
        requests.exceptions.HTTPError: Se a API retornar erro HTTP.
        requests.exceptions.ConnectionError: Se não houver conexão com a internet.
    """
    if not city_name or not city_name.strip():
        raise ValueError("O nome da cidade não pode estar vazio.")

    params = {
        "name": city_name.strip(),
        "count": 1,
        "language": "pt",
        "format": "json",
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("results")

    if not results:
        raise ValueError(f"Cidade '{city_name}' não encontrada. Verifique o nome e tente novamente.")

    location = results[0]
    return {
        "name": location.get("name", ""),
        "country": location.get("country", ""),
        "admin1": location.get("admin1", ""),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
    }
