"""
Script para gerar documentação em PDF do projeto Climatempo API
Requer: pip install fpdf2
"""

from fpdf import FPDF
from datetime import datetime

class PDFDocumentacao(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Cabeçalho das páginas"""
        pass
    
    def footer(self):
        """Rodapé das páginas"""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"P{self.page_no()}", align="C")
        
    def chapter_title(self, title):
        """Título de capítulo"""
        self.set_font("Arial", "B", 16)
        self.set_text_color(31, 119, 180)
        self.set_xy(15, self.get_y())
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)
        
    def section_title(self, title):
        """Título de seção"""
        self.set_font("Arial", "B", 12)
        self.set_text_color(51, 51, 51)
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)
        
    def body_text(self, text):
        """Texto do corpo"""
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, text)
        self.ln(2)

def gerar_documentacao():
    """Gera o arquivo PDF com documentação completa."""
    
    pdf = PDFDocumentacao()
    pdf.add_page()
    
    # =========== CAPA ===========
    pdf.ln(40)
    
    pdf.set_font("Arial", "B", 32)
    pdf.set_text_color(31, 119, 180)
    pdf.multi_cell(0, 15, "CLIMATEMPO API", align="C")
    
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(85, 85, 85)
    pdf.multi_cell(0, 10, "Aplicativo de Previsão do Tempo", align="C")
    
    pdf.ln(20)
    
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, "Documentação Técnica Completa", align="C")
    
    pdf.ln(30)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, f"Versão 1.0\n{datetime.now().strftime('%d de %B de %Y')}", align="C")
    
    pdf.ln(20)
    
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "Desenvolvido com:\nPython 3.10+ | Open-Meteo API", align="C")
    
    pdf.ln(40)
    
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 5, "Projeto de uso livre para fins educacionais", align="C")
    
    # =========== PÁGINA 2: ÍNDICE ===========
    pdf.add_page()
    pdf.chapter_title("ÍNDICE")
    
    indice_items = [
        "1. Visão Geral do Projeto",
        "2. Pré-requisitos e Instalação",
        "3. Como Usar",
        "4. Estrutura do Projeto",
        "5. Módulos e Funções",
        "6. Exemplos de Uso",
        "7. Tratamento de Erros",
        "8. APIs Utilizadas",
        "9. Testes",
        "10. Licença",
    ]
    
    for item in indice_items:
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, item, ln=True)
    
    # =========== PÁGINA 3: VISÃO GERAL ===========
    pdf.add_page()
    pdf.chapter_title("1. Visão Geral do Projeto")
    
    pdf.body_text(
        "O Climatempo API é um aplicativo de linha de comando desenvolvido em Python que busca dados "
        "meteorológicos em tempo real para qualquer cidade do mundo. O projeto utiliza as APIs gratuitas do "
        "Open-Meteo sem necessidade de cadastro ou chave de API."
    )
    
    pdf.section_title("Características principais:")
    
    features = [
        "✓ Interface amigável em linha de comando (CLI)",
        "✓ Suporte a cidades em qualquer lugar do mundo",
        "✓ Dados meteorológicos em tempo real",
        "✓ Sem necessidade de cadastro ou autenticação",
        "✓ APIs gratuitas com limite generoso",
        "✓ Tratamento completo de erros",
        "✓ Código modular e bem documentado",
        "✓ Suíte completa de testes unitários",
    ]
    
    for feature in features:
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, feature, ln=True, x=20)
    
    # =========== PÁGINA 4: PRÉ-REQUISITOS ===========
    pdf.add_page()
    pdf.chapter_title("2. Pré-requisitos e Instalação")
    
    pdf.section_title("Requisitos do Sistema:")
    pdf.body_text("• Python 3.10 ou superior\n• Conexão ativa com a internet")
    
    pdf.section_title("Instalação de Dependências:")
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(20, pdf.get_y())
    pdf.cell(0, 6, "$ pip install -r requirements.txt", ln=True)
    
    pdf.ln(4)
    
    pdf.section_title("Nota importante:")
    pdf.body_text(
        "Apenas a biblioteca 'requests' é necessária para executar o aplicativo. O pacote 'pytest' é "
        "opcional e serve apenas para os testes."
    )
    
    # =========== PÁGINA 5: COMO USAR ===========
    pdf.add_page()
    pdf.chapter_title("3. Como Usar")
    
    pdf.section_title("Execução Básica:")
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(20, pdf.get_y())
    pdf.cell(0, 6, "$ python weather_app.py", ln=True)
    
    pdf.ln(6)
    
    pdf.section_title("Exemplos de entrada de cidade:")
    
    examples = [
        "• Novo Hamburgo RS Brasil",
        "• São Paulo",
        "• Rio de Janeiro",
        "• Paris France",
        "• New York",
    ]
    
    for example in examples:
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, example, ln=True, x=20)
    
    pdf.ln(4)
    
    pdf.body_text(
        "O aplicativo retornará dados meteorológicos como temperatura, umidade, velocidade do vento, "
        "precipitação e descrição da condição climática."
    )
    
    # =========== PÁGINA 6: ESTRUTURA ===========
    pdf.add_page()
    pdf.chapter_title("4. Estrutura do Projeto")
    
    pdf.set_font("Courier", "", 8)
    pdf.set_x(20)
    structure = """climatempo_api/
├── weather_app.py
├── geocoding.py
├── weather.py
├── requirements.txt
├── tests/
│   ├── __init__.py
│   └── test_weather_app.py
└── README.md"""
    
    for line in structure.split('\n'):
        pdf.cell(0, 5, line, ln=True, x=20)
    
    pdf.ln(6)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)
    
    pdf.body_text(
        "weather_app.py: Ponto de entrada principal que orquestra a leitura do input do usuário, "
        "chamadas aos módulos de geocodificação e clima."
    )
    
    pdf.body_text(
        "geocoding.py: Módulo responsável por converter nomes de cidades em coordenadas geográficas."
    )
    
    pdf.body_text(
        "weather.py: Módulo que busca dados meteorológicos atuais a partir de coordenadas."
    )
    
    # =========== PÁGINA 7: MÓDULOS ===========
    pdf.add_page()
    pdf.chapter_title("5. Módulos e Funções")
    
    pdf.section_title("5.1 geocoding.py - get_coordinates()")
    pdf.body_text(
        "Descrição: Obtém latitude e longitude para um nome de cidade.\n\n"
        "Parâmetros: city_name (str) - Nome da cidade\n\n"
        "Retorno: Dicionário com name, country, admin1, latitude e longitude\n\n"
        "Exceções: ValueError, Timeout, HTTPError, ConnectionError"
    )
    
    pdf.section_title("5.2 weather.py - get_weather()")
    pdf.body_text(
        "Descrição: Busca dados meteorológicos atuais para as coordenadas.\n\n"
        "Parâmetros: latitude e longitude (floats)\n\n"
        "Retorno: Dicionário com temperature, feels_like, humidity, wind_speed, wind_direction, "
        "precipitation, description, timezone"
    )
    
    pdf.section_title("5.3 weather_app.py - display_weather()")
    pdf.body_text(
        "Descrição: Exibe os dados meteorológicos em formato amigável.\n\n"
        "Parâmetros: location (dict) e weather (dict)"
    )
    
    # =========== PÁGINA 8: EXEMPLO ===========
    pdf.add_page()
    pdf.chapter_title("6. Exemplo de Uso")
    
    pdf.set_font("Courier", "", 7.5)
    example_output = """$ python weather_app.py
====================================================
    Aplicativo de Previsão do Tempo
====================================================
Digite o nome da cidade: Novo Hamburgo RS Brasil
Buscando localização...
====================================================
Clima atual em: Novo Hamburgo, RS, Brasil
====================================================
Condição         : Principalmente limpo
Temperatura      : 22.5 °C
Sensação térmica : 21.0 °C
Umidade relativa : 65 %
Velocidade vento : 15.0 km/h
Direção vento    : Sul
Precipitação     : 0.0 mm
Fuso horário     : America/Sao_Paulo
===================================================="""
    
    for line in example_output.split('\n'):
        pdf.cell(0, 4, line, ln=True, x=15)
    
    # =========== PÁGINA 9: TRATAMENTO DE ERROS ===========
    pdf.add_page()
    pdf.chapter_title("7. Tratamento de Erros")
    
    pdf.section_title("Situações tratadas:")
    
    errors = [
        "• Entrada vazia → Mensagem de erro e saída com código 1",
        "• Cidade não encontrada → Mensagem informativa e saída com código 1",
        "• Timeout (> 10s) → Mensagem de timeout e saída com código 1",
        "• Sem conexão com internet → Mensagem de conexão e saída com código 1",
        "• Erro HTTP da API → Mensagem com código HTTP e saída com código 1",
    ]
    
    for error in errors:
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, error, x=20)
    
    # =========== PÁGINA 10: APIs ===========
    pdf.add_page()
    pdf.chapter_title("8. APIs Utilizadas")
    
    pdf.body_text(
        "Open-Meteo Geocoding:\nURL: https://geocoding-api.open-meteo.com/v1/search\n\n"
        "Open-Meteo Weather:\nURL: https://api.open-meteo.com/v1/forecast\n\n"
        "Ambas as APIs são gratuitas, sem necessidade de cadastro ou autenticação."
    )
    
    pdf.ln(6)
    
    pdf.section_title("Dados Meteorológicos Buscados:")
    
    fields = [
        "• temperature_2m — Temperatura a 2 m do solo (°C)",
        "• apparent_temperature — Sensação térmica (°C)",
        "• relative_humidity_2m — Umidade relativa (%)",
        "• wind_speed_10m — Velocidade do vento (km/h)",
        "• wind_direction_10m — Direção do vento (graus)",
        "• precipitation — Precipitação na última hora (mm)",
        "• weather_code — Código WMO de condição climática",
    ]
    
    for field in fields:
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, field, x=20)
    
    # =========== PÁGINA 11: TESTES ===========
    pdf.add_page()
    pdf.chapter_title("9. Testes")
    
    pdf.body_text(
        "A suíte de testes utiliza unittest com unittest.mock — não faz chamadas reais à internet."
    )
    
    pdf.ln(4)
    
    pdf.section_title("Executar com pytest (recomendado):")
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(20, pdf.get_y())
    pdf.cell(0, 6, "$ pytest tests/ -v", ln=True)
    
    pdf.ln(4)
    
    pdf.section_title("Executar com unittest:")
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(20, pdf.get_y())
    pdf.cell(0, 6, "$ python -m unittest discover -s tests -v", ln=True)
    
    pdf.ln(6)
    
    pdf.section_title("Cenários Cobertos:")
    
    scenarios = [
        "1. Geocoding: Cidade válida → Retorna coordenadas",
        "2. Geocoding: Cidade inexistente → Lança ValueError",
        "3. Geocoding: Entrada vazia → Lança ValueError",
        "4. Geocoding: Timeout da API → Propaga Timeout",
        "5. Geocoding: Erro HTTP → Propaga HTTPError",
        "6. Weather: Coordenadas válidas → Retorna dados",
        "7. Weather: Código WMO desconhecido → Retorna descrição",
        "8. Weather: Timeout da API → Propaga Timeout",
        "9. Weather: Erro HTTP → Propaga HTTPError",
    ]
    
    for scenario in scenarios:
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, scenario, x=20)
    
    # =========== PÁGINA 12: LICENÇA ===========
    pdf.add_page()
    pdf.chapter_title("10. Licença")
    
    pdf.ln(20)
    
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(31, 119, 180)
    pdf.multi_cell(0, 10, "Projeto de uso livre para fins educacionais", align="C")
    
    pdf.ln(30)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)
    
    pdf.section_title("Informações Adicionais:")
    
    pdf.body_text(
        "Este projeto foi desenvolvido como exemplo de boas práticas em Python.\n\n"
        "Características:\n"
        "• Utiliza APIs públicas e gratuitas do Open-Meteo\n"
        "• Código modular, bem documentado e totalmente testado\n"
        "• Suporta cidades em qualquer lugar do mundo\n"
        "• Interface amigável em linha de comando"
    )
    
    pdf.ln(10)
    
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4, f"Documentação gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", align="C")
    
    # Salvar PDF
    filename = "Climatempo_API_Documentacao.pdf"
    pdf.output(filename)
    print(f"✓ Documentação gerada com sucesso: {filename}")
    return filename

if __name__ == "__main__":
    gerar_documentacao()
