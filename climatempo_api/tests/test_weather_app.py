"""
Suíte de testes para os módulos geocoding.py e weather.py.

Cobertura:
  - Cidade válida retornando dados com sucesso
  - Cidade inexistente retornando erro
  - Entrada vazia retornando mensagem de erro
  - Falha da API: timeout
  - Falha da API: erro de servidor (5xx)

Execução:
    python -m pytest tests/ -v
    # ou sem pytest:
    python -m unittest discover -s tests -v
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

import requests

# Garante que os módulos do projeto sejam encontrados ao rodar os testes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from geocoding import get_coordinates  # noqa: E402
from weather import get_weather         # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures reutilizáveis
# ---------------------------------------------------------------------------

VALID_GEOCODING_RESPONSE = {
    "results": [
        {
            "name": "Novo Hamburgo",
            "country": "Brasil",
            "admin1": "Rio Grande do Sul",
            "latitude": -29.6783,
            "longitude": -51.1306,
        }
    ]
}

VALID_WEATHER_RESPONSE = {
    "current": {
        "temperature_2m": 22.5,
        "apparent_temperature": 21.0,
        "relative_humidity_2m": 65,
        "wind_speed_10m": 15.0,
        "wind_direction_10m": 180,
        "precipitation": 0.0,
        "weather_code": 1,
    },
    "timezone": "America/Sao_Paulo",
}


def _make_mock_response(json_data: dict, raise_for_status=None) -> MagicMock:
    """Cria um mock de requests.Response."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = json_data
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    else:
        mock_resp.raise_for_status.return_value = None
    return mock_resp


# ---------------------------------------------------------------------------
# Testes de Geocodificação
# ---------------------------------------------------------------------------

class TestGetCoordinates(unittest.TestCase):
    """Testes para a função get_coordinates() em geocoding.py."""

    # ------------------------------------------------------------------
    # Cenário 1: Cidade válida – retorna coordenadas com sucesso
    # ------------------------------------------------------------------
    @patch("geocoding.requests.get")
    def test_cidade_valida_retorna_coordenadas(self, mock_get):
        """Uma cidade válida deve retornar nome, país e coordenadas corretos."""
        mock_get.return_value = _make_mock_response(VALID_GEOCODING_RESPONSE)

        result = get_coordinates("Novo Hamburgo RS Brasil")

        self.assertEqual(result["name"], "Novo Hamburgo")
        self.assertEqual(result["country"], "Brasil")
        self.assertEqual(result["admin1"], "Rio Grande do Sul")
        self.assertAlmostEqual(result["latitude"], -29.6783, places=4)
        self.assertAlmostEqual(result["longitude"], -51.1306, places=4)

    # ------------------------------------------------------------------
    # Cenário 2: Cidade inexistente – deve levantar ValueError
    # ------------------------------------------------------------------
    @patch("geocoding.requests.get")
    def test_cidade_inexistente_levanta_value_error(self, mock_get):
        """Uma cidade inexistente (API retorna lista vazia) deve gerar ValueError."""
        mock_get.return_value = _make_mock_response({})  # sem chave 'results'

        with self.assertRaises(ValueError) as ctx:
            get_coordinates("CidadeQueNaoExisteXYZ123")

        self.assertIn("não encontrada", str(ctx.exception))

    @patch("geocoding.requests.get")
    def test_cidade_inexistente_results_vazio(self, mock_get):
        """API retornando results=[] também deve gerar ValueError."""
        mock_get.return_value = _make_mock_response({"results": []})

        with self.assertRaises(ValueError):
            get_coordinates("AbcdefghijklmnopXYZ")

    # ------------------------------------------------------------------
    # Cenário 3: Entrada vazia – deve retornar mensagem de erro
    # ------------------------------------------------------------------
    def test_entrada_vazia_levanta_value_error(self):
        """String vazia deve gerar ValueError sem chegar a fazer requisição."""
        with self.assertRaises(ValueError) as ctx:
            get_coordinates("")

        self.assertIn("vazio", str(ctx.exception).lower())

    def test_entrada_somente_espacos_levanta_value_error(self):
        """String com apenas espaços deve ser tratada como vazia."""
        with self.assertRaises(ValueError):
            get_coordinates("   ")

    def test_entrada_none_levanta_value_error(self):
        """Valor None deve gerar ValueError."""
        with self.assertRaises(ValueError):
            get_coordinates(None)

    # ------------------------------------------------------------------
    # Cenário 4: Falha da API – timeout
    # ------------------------------------------------------------------
    @patch("geocoding.requests.get")
    def test_api_timeout_propaga_exception(self, mock_get):
        """Timeout na requisição deve propagar requests.exceptions.Timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        with self.assertRaises(requests.exceptions.Timeout):
            get_coordinates("Novo Hamburgo")

    # ------------------------------------------------------------------
    # Cenário 4: Falha da API – erro de servidor (5xx)
    # ------------------------------------------------------------------
    @patch("geocoding.requests.get")
    def test_api_erro_servidor_propaga_http_error(self, mock_get):
        """Erro HTTP 500 deve propagar requests.exceptions.HTTPError."""
        mock_get.return_value = _make_mock_response(
            {},
            raise_for_status=requests.exceptions.HTTPError("500 Server Error"),
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            get_coordinates("Novo Hamburgo")

    @patch("geocoding.requests.get")
    def test_api_conexao_recusada_propaga_connection_error(self, mock_get):
        """Erro de conexão deve propagar requests.exceptions.ConnectionError."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertRaises(requests.exceptions.ConnectionError):
            get_coordinates("Novo Hamburgo")


# ---------------------------------------------------------------------------
# Testes de Dados Meteorológicos
# ---------------------------------------------------------------------------

class TestGetWeather(unittest.TestCase):
    """Testes para a função get_weather() em weather.py."""

    # ------------------------------------------------------------------
    # Cenário 1: Coordenadas válidas – retorna dados meteorológicos
    # ------------------------------------------------------------------
    @patch("weather.requests.get")
    def test_coordenadas_validas_retorna_dados(self, mock_get):
        """Coordenadas válidas devem retornar dicionário com dados do clima."""
        mock_get.return_value = _make_mock_response(VALID_WEATHER_RESPONSE)

        result = get_weather(-29.6783, -51.1306)

        self.assertEqual(result["temperature"], 22.5)
        self.assertEqual(result["feels_like"], 21.0)
        self.assertEqual(result["humidity"], 65)
        self.assertEqual(result["wind_speed"], 15.0)
        self.assertEqual(result["precipitation"], 0.0)
        self.assertEqual(result["weather_code"], 1)
        self.assertEqual(result["description"], "Principalmente limpo")
        self.assertEqual(result["timezone"], "America/Sao_Paulo")

    @patch("weather.requests.get")
    def test_codigo_wmo_desconhecido_retorna_descricao_padrao(self, mock_get):
        """Código WMO não mapeado deve retornar 'Condição desconhecida'."""
        data = {**VALID_WEATHER_RESPONSE}
        data["current"] = {**data["current"], "weather_code": 999}
        mock_get.return_value = _make_mock_response(data)

        result = get_weather(-29.6783, -51.1306)

        self.assertEqual(result["description"], "Condição desconhecida")

    # ------------------------------------------------------------------
    # Cenário 4: Falha da API – timeout
    # ------------------------------------------------------------------
    @patch("weather.requests.get")
    def test_api_timeout_propaga_exception(self, mock_get):
        """Timeout na API de clima deve propagar requests.exceptions.Timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")

        with self.assertRaises(requests.exceptions.Timeout):
            get_weather(-29.6783, -51.1306)

    # ------------------------------------------------------------------
    # Cenário 4: Falha da API – erro de servidor
    # ------------------------------------------------------------------
    @patch("weather.requests.get")
    def test_api_erro_servidor_propaga_http_error(self, mock_get):
        """Erro HTTP 503 deve propagar requests.exceptions.HTTPError."""
        mock_get.return_value = _make_mock_response(
            {},
            raise_for_status=requests.exceptions.HTTPError("503 Service Unavailable"),
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            get_weather(-29.6783, -51.1306)

    @patch("weather.requests.get")
    def test_api_conexao_recusada_propaga_connection_error(self, mock_get):
        """Erro de conexão deve propagar requests.exceptions.ConnectionError."""
        mock_get.side_effect = requests.exceptions.ConnectionError("No route to host")

        with self.assertRaises(requests.exceptions.ConnectionError):
            get_weather(-29.6783, -51.1306)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
