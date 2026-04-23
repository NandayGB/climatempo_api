<img width="1408" height="768" alt="Gemini_Generated_Image_kpbrs0kpbrs0kpbr (1)" src="https://github.com/user-attachments/assets/fdf32169-901b-4521-8972-d4aa829d007c" />
# 🌤️ Aplicativo de Previsão do Tempo (CLI) 💻

Um aplicativo de linha de comando (CLI) simples e eficiente desenvolvido em **Python**. Ele permite consultar dados meteorológicos em tempo real para qualquer cidade do mundo utilizando as APIs gratuitas do **Open-Meteo** — sem necessidade de cadastro ou chave de API.

---

## 🖼️ Interface (GUI - conceito)

O projeto também inclui um conceito de interface gráfica moderna e limpa:

- 🌞 Ícone grande representando a condição climática (ex: “Principalmente limpo”)
- 🌡️ Temperatura em destaque
- 📊 Cards informativos:
  - Sensação térmica  
  - Umidade  
  - Vento  
  - Precipitação  
- 🔍 Barra de pesquisa para cidades  
- 📅 Previsão para próximos dias  
- 🎨 Design minimalista e intuitivo  

---

## 📁 Estrutura do Projeto


climatempo_api/
├── weather_app.py # Ponto de entrada — executa o aplicativo
├── geocoding.py # Módulo de geocodificação (cidade → coordenadas)
├── weather.py # Módulo de clima (coordenadas → dados meteorológicos)
├── requirements.txt # Dependências Python
├── tests/
│ ├── init.py
│ └── test_weather_app.py # Testes unitários
└── README.md # Documentação do projeto


---

## 🛠️ Pré-requisitos

- 🐍 Python **3.10+**
- 🌐 Conexão com a internet

---

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
Acesse a pasta:
cd climatempo_api
Instale as dependências:
pip install -r requirements.txt

📌 Nota:

requests é obrigatório
pytest é opcional (apenas para testes)
📖 Como Usar

Execute o comando:

python weather_app.py

Exemplo de uso:

====================================================
      🌤️ Aplicativo de Previsão do Tempo
====================================================

➡️ Digite o nome da cidade:
Novo Hamburgo RS Brasil

🔍 Buscando localização...
✅ Localização encontrada

📊 Clima atual:
✨ Condição         : Principalmente limpo
🌡️ Temperatura      : 22.5 °C
🥶 Sensação térmica : 21.0 °C
💧 Umidade          : 65 %
💨 Vento            : 15.0 km/h
☔ Precipitação     : 0.0 mm
💡 Exemplos de Entrada
Novo Hamburgo RS Brasil
São Paulo
Rio de Janeiro
Paris France
New York
🧩 Módulos
📍 geocoding.py

Responsável por converter nome da cidade em coordenadas.

Função principal:

get_coordinates(city_name)

Retorna:

name
country
admin1
latitude
longitude

Erros:

ValueError para entrada inválida ou cidade não encontrada

API:

https://geocoding-api.open-meteo.com/v1/search
☁️ weather.py

Responsável por buscar dados meteorológicos.

Função principal:

get_weather(latitude, longitude)

Dados retornados:

Temperatura
Sensação térmica
Umidade
Velocidade do vento
Direção do vento
Precipitação
Condição climática (WMO)

API:

https://api.open-meteo.com/v1/forecast
🚀 weather_app.py
Ponto de entrada do sistema
Integra os módulos
Trata erros
Exibe dados formatados no terminal
🧪 Testes

Utiliza:

unittest
unittest.mock
▶️ Executar com pytest:
pytest tests/ -v
▶️ Executar com unittest:
python -m unittest discover -s tests -v
✅ Cenários de Teste
#	Módulo	Cenário	Resultado
1	geocoding	Cidade válida	OK
2	geocoding	Cidade inexistente	Erro
3	geocoding	Entrada vazia	Erro
4	geocoding	Apenas espaços	Erro
5	geocoding	None	Erro
6	geocoding	Timeout API	Exceção
7	geocoding	Erro 500	Exceção
8	geocoding	Sem internet	Exceção
9	weather	Coordenadas válidas	OK
10	weather	Código WMO desconhecido	OK
11	weather	Timeout	Exceção
12	weather	Erro 503	Exceção
13	weather	Sem internet	Exceção
🌐 APIs Utilizadas
API	URL	Autenticação
Open-Meteo Geocoding	https://geocoding-api.open-meteo.com/v1/search
	❌
Open-Meteo Weather	https://api.open-meteo.com/v1/forecast
	❌

✔️ Gratuitas
✔️ Sem cadastro
✔️ Uso ideal para projetos pessoais

🚨 Tratamento de Erros
Situação	Comportamento
Entrada inválida	Mensagem + exit(1)
Cidade não encontrada	Mensagem + exit(1)
Timeout	Mensagem + exit(1)
Sem internet	Mensagem + exit(1)
Erro HTTP	Mensagem + exit(1)
📄 Licença

📚 Projeto de uso livre para fins educacionais.
