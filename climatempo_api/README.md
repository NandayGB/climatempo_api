# Aplicativo de Previsão do Tempo

Aplicativo de linha de comando em Python que busca dados meteorológicos em tempo real para qualquer cidade do mundo, utilizando as APIs gratuitas do [Open-Meteo](https://open-meteo.com/) — **sem necessidade de cadastro ou chave de API**.

---

## Estrutura do Projeto

```
climatempo_api/
├── weather_app.py        # Ponto de entrada — executa o aplicativo
├── geocoding.py          # Módulo de geocodificação (cidade → coordenadas)
├── weather.py            # Módulo de clima (coordenadas → dados meteorológicos)
├── requirements.txt      # Dependências Python
├── tests/
│   ├── __init__.py
│   └── test_weather_app.py   # Suíte de testes unitários
└── README.md
```

---

## Pré-requisitos

- Python **3.10+**
- Conexão com a internet

---

## Instalação

```bash
# Clone ou baixe os arquivos do projeto, acesse a pasta e instale a dependência:
pip install -r requirements.txt
```

> Apenas a biblioteca `requests` é necessária para executar o aplicativo.  
> O pacote `pytest` é opcional e serve apenas para os testes.

---

## Como Usar

```bash
python weather_app.py
```

O aplicativo solicitará o nome de uma cidade:

```
====================================================
      Aplicativo de Previsão do Tempo
      Powered by Open-Meteo (open-meteo.com)
====================================================

Digite o nome da cidade (ex: Novo Hamburgo RS Brasil): Novo Hamburgo RS Brasil

Buscando localização para 'Novo Hamburgo RS Brasil'...
Localização encontrada: Novo Hamburgo, Rio Grande do Sul, Brasil
Obtendo dados meteorológicos...

====================================================
  Clima atual em: Novo Hamburgo, Rio Grande do Sul, Brasil
====================================================
  Condição         : Principalmente limpo
  Temperatura      : 22.5 °C
  Sensação térmica : 21.0 °C
  Umidade relativa : 65 %
  Velocidade vento : 15.0 km/h
  Direção vento    : Sul (180°)
  Precipitação     : 0.0 mm
  Fuso horário     : America/Sao_Paulo
====================================================
```

**Dicas de entrada:**
- `Novo Hamburgo RS Brasil`
- `São Paulo`
- `Rio de Janeiro`
- `Paris France`
- `New York`

---

## Módulos

### `geocoding.py`

| Função | Descrição |
|---|---|
| `get_coordinates(city_name)` | Recebe o nome de uma cidade e retorna um dicionário com `name`, `country`, `admin1`, `latitude` e `longitude`. Gera `ValueError` para entradas vazias ou cidades não encontradas. |

**API utilizada:** `https://geocoding-api.open-meteo.com/v1/search`

---

### `weather.py`

| Função | Descrição |
|---|---|
| `get_weather(latitude, longitude)` | Recebe coordenadas e retorna dados meteorológicos atuais: temperatura, sensação térmica, umidade, vento, precipitação e descrição da condição (WMO). |

**API utilizada:** `https://api.open-meteo.com/v1/forecast`

**Parâmetros buscados (current):**
- `temperature_2m` — Temperatura a 2 m do solo (°C)
- `apparent_temperature` — Sensação térmica (°C)
- `relative_humidity_2m` — Umidade relativa (%)
- `wind_speed_10m` — Velocidade do vento (km/h)
- `wind_direction_10m` — Direção do vento (graus)
- `precipitation` — Precipitação na última hora (mm)
- `weather_code` — Código WMO de condição climática

---

### `weather_app.py`

Ponto de entrada principal. Orquestra a leitura do input do usuário, chamadas aos módulos `geocoding` e `weather`, e exibição do resultado formatado. Trata todos os erros possíveis com mensagens em português.

---

## Testes

A suíte de testes usa `unittest` com `unittest.mock` — **não faz chamadas reais à internet**.

### Executar com pytest (recomendado)

```bash
pytest tests/ -v
```

### Executar com unittest (sem dependências extras)

```bash
python -m unittest discover -s tests -v
```

### Cenários cobertos

| # | Módulo | Cenário | Resultado esperado |
|---|---|---|---|
| 1 | `geocoding` | Cidade válida (`Novo Hamburgo RS Brasil`) | Retorna coordenadas corretas |
| 2 | `geocoding` | Cidade inexistente | Lança `ValueError` com mensagem de erro |
| 3 | `geocoding` | Entrada vazia `""` | Lança `ValueError` com mensagem de erro |
| 4 | `geocoding` | Entrada somente espaços | Lança `ValueError` |
| 5 | `geocoding` | `None` como entrada | Lança `ValueError` |
| 6 | `geocoding` | Timeout da API | Propaga `requests.exceptions.Timeout` |
| 7 | `geocoding` | Erro 500 do servidor | Propaga `requests.exceptions.HTTPError` |
| 8 | `geocoding` | Sem conexão com a internet | Propaga `requests.exceptions.ConnectionError` |
| 9 | `weather` | Coordenadas válidas | Retorna dados e descrição WMO correta |
| 10 | `weather` | Código WMO desconhecido | Retorna `"Condição desconhecida"` |
| 11 | `weather` | Timeout da API | Propaga `requests.exceptions.Timeout` |
| 12 | `weather` | Erro 503 do servidor | Propaga `requests.exceptions.HTTPError` |
| 13 | `weather` | Sem conexão com a internet | Propaga `requests.exceptions.ConnectionError` |

---

## APIs Utilizadas

| API | URL Base | Autenticação |
|---|---|---|
| Open-Meteo Geocoding | `https://geocoding-api.open-meteo.com/v1/search` | Nenhuma |
| Open-Meteo Weather | `https://api.open-meteo.com/v1/forecast` | Nenhuma |

Ambas são gratuitas, sem necessidade de cadastro, com limite generoso de requisições para uso pessoal.

---

## Tratamento de Erros

| Situação | Comportamento |
|---|---|
| Entrada vazia | Mensagem de erro e saída com código 1 |
| Cidade não encontrada | Mensagem informativa e saída com código 1 |
| Timeout (> 10s) | Mensagem de timeout e saída com código 1 |
| Sem internet | Mensagem de conexão e saída com código 1 |
| Erro HTTP da API | Mensagem com código HTTP e saída com código 1 |

---

## Licença

Projeto de uso livre para fins educacionais.
