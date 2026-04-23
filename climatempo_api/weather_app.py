"""
Aplicativo de Previsão do Tempo
================================
Ponto de entrada principal. Solicita o nome de uma cidade ao usuário,
busca as coordenadas via geocodificação e exibe os dados climáticos atuais.

Uso:
    python weather_app.py
"""

import sys

import requests

from geocoding import get_coordinates
from weather import get_weather

WIND_DIRECTIONS = [
    "Norte", "Nordeste", "Leste", "Sudeste",
    "Sul", "Sudoeste", "Oeste", "Noroeste",
]


def _wind_direction_label(degrees: float | None) -> str:
    """Converte graus em rótulo de direção cardinal."""
    if degrees is None:
        return "N/A"
    index = round(degrees / 45) % 8
    return WIND_DIRECTIONS[index]


def display_weather(location: dict, weather: dict) -> None:
    """
    Exibe os dados meteorológicos em formato amigável ao usuário.

    Args:
        location: Dicionário retornado por get_coordinates().
        weather:  Dicionário retornado por get_weather().
    """
    parts = [location["name"]]
    if location.get("admin1"):
        parts.append(location["admin1"])
    if location.get("country"):
        parts.append(location["country"])
    city_display = ", ".join(parts)

    wind_label = _wind_direction_label(weather.get("wind_direction"))

    print()
    print("=" * 52)
    print(f"  Clima atual em: {city_display}")
    print("=" * 52)
    print(f"  Condição         : {weather['description']}")
    print(f"  Temperatura      : {weather['temperature']} °C")
    print(f"  Sensação térmica : {weather['feels_like']} °C")
    print(f"  Umidade relativa : {weather['humidity']} %")
    print(f"  Velocidade vento : {weather['wind_speed']} km/h")
    print(f"  Direção vento    : {wind_label} ({weather['wind_direction']}°)")
    print(f"  Precipitação     : {weather['precipitation']} mm")
    print(f"  Fuso horário     : {weather['timezone']}")
    print("=" * 52)
    print()


def main() -> None:
    """Fluxo principal do aplicativo."""
    print()
    print("=" * 52)
    print("      Aplicativo de Previsão do Tempo")
    print("      Powered by Open-Meteo (open-meteo.com)")
    print("=" * 52)

    city_name = input("\nDigite o nome da cidade (ex: Novo Hamburgo RS Brasil): ").strip()

    try:
        if not city_name:
            raise ValueError("O nome da cidade não pode estar vazio.")

        print(f"\nBuscando localização para '{city_name}'...")
        location = get_coordinates(city_name)
        print(f"Localização encontrada: {location['name']}, {location.get('admin1', '')}, {location.get('country', '')}")

        print("Obtendo dados meteorológicos...")
        weather = get_weather(location["latitude"], location["longitude"])

        display_weather(location, weather)

    except ValueError as exc:
        print(f"\n[Erro] {exc}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\n[Erro] Não foi possível conectar à API. Verifique sua conexão com a internet.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\n[Erro] A requisição excedeu o tempo limite (10s). Tente novamente.")
        sys.exit(1)
    except requests.exceptions.HTTPError as exc:
        print(f"\n[Erro de API] {exc}")
        sys.exit(1)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"\n[Erro inesperado] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
