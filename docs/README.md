<img width="1655" height="893" alt="image" src="https://github.com/user-attachments/assets/722b75fb-2d84-40a1-8f55-1756df162a11" />
<img width="1703" height="906" alt="image" src="https://github.com/user-attachments/assets/4d64145c-9951-48ba-9101-5414eb0108ee" />
<img width="1682" height="835" alt="image" src="https://github.com/user-attachments/assets/5ebe739c-4aa4-4664-a1ec-6b7068272359" />



# 🌾 AgriSense - Sistema de Automação Agrícola

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Sistema completo de automação e monitoramento para agricultura de precisão, desenvolvido como projeto de portfólio para vaga de **Engenheiro Embarcado Júnior em Automação Agrícola**.

## 📋 Sobre o Projeto

AgriSense é uma plataforma de demonstração que simula um sistema embarcado completo para automação agrícola, implementando:

- 🌡️ **Monitoramento em Tempo Real** - Sensores de solo, clima e GPS
- 💧 **Controle de Irrigação** - Sistema automatizado com 4 zonas
- 🌱 **Gestão de Fertilização** - Aplicação controlada de NPK
- 📡 **Protocolos Industriais** - CAN Bus e ISOBUS (ISO 11783)
- 🗺️ **Agricultura de Precisão** - Mapas de produtividade e zonas de manejo
- 📊 **Dashboard Interativo** - Interface web em tempo real

## 🎯 Objetivos do Projeto

Este projeto demonstra competências essenciais para a vaga:

✅ Desenvolvimento de sistemas embarcados  
✅ Programação em Python para sistemas de controle  
✅ Implementação de protocolos CAN e ISOBUS  
✅ Integração de sensores e atuadores  
✅ Documentação técnica completa  
✅ Arquitetura de software bem estruturada

## 🚀 Tecnologias Utilizadas

### Core

- **Python 3.11+** - Linguagem principal
- **Streamlit** - Framework para dashboard web
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica

### Visualização

- **Plotly** - Gráficos interativos
- **Matplotlib** - Visualizações estáticas

### Protocolos

- Simulação de **CAN Bus** (Controller Area Network)
- Simulação de **ISOBUS** (ISO 11783)

## 📁 Estrutura do Projeto

```
agrisense-automacao-agricola/
│
├── app.py                          # Dashboard principal Streamlit
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação principal
│
├── src/                            # Código fonte
│   ├── sensors/                    # Módulos de sensores
│   │   ├── soil_sensor.py         # Sensor de solo (umidade, pH, NPK)
│   │   ├── weather_sensor.py      # Estação meteorológica
│   │   └── gps_sensor.py          # GPS RTK para agricultura de precisão
│   │
│   ├── actuators/                  # Módulos de atuadores
│   │   ├── irrigation.py          # Sistema de irrigação
│   │   └── fertilizer.py          # Sistema de fertilização
│   │
│   ├── protocols/                  # Protocolos de comunicação
│   │   ├── can_protocol.py        # Protocolo CAN Bus
│   │   └── isobus_simulator.py    # Protocolo ISOBUS
│   │
│   └── utils/                      # Utilitários
│       ├── data_generator.py      # Gerador de dados simulados
│       └── logger.py              # Sistema de logs
│
├── data/                           # Dados e logs
├── docs/                           # Documentação técnica
│   ├── ARCHITECTURE.md            # Arquitetura do sistema
│   ├── API_REFERENCE.md           # Referência das APIs
│   └── USER_MANUAL.md             # Manual do usuário
│
└── tests/                          # Testes unitários

```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Git
- Ambiente virtual Python (recomendado)

### Passo a Passo

1. **Clone o repositório:**

```bash
git clone https://github.com/Daniel-1984/agrisense-automacao-agricola.git
cd agrisense-automacao-agricola
```

2. **Crie e ative o ambiente virtual:**

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Execute o dashboard:**

```bash
streamlit run app.py
```

5. **Acesse no navegador:**

```
http://localhost:8501
```

## 💻 Uso dos Módulos

### Exemplo: Sensor de Solo

```python
from src.sensors.soil_sensor import SoilSensor

# Criar e ativar sensor
sensor = SoilSensor(
    sensor_id="SOIL_001",
    location=(-25.4284, -49.2733),  # Curitiba, PR
    sampling_rate=5
)
sensor.start()

# Ler dados
reading = sensor.read_all()
print(f"Umidade: {reading['moisture']}%")
print(f"pH: {reading['ph']}")
print(f"NPK: N={reading['nitrogen']}, P={reading['phosphorus']}, K={reading['potassium']}")
```

### Exemplo: Sistema de Irrigação

```python
from src.actuators.irrigation import IrrigationSystem, IrrigationMode

# Criar sistema
irrigation = IrrigationSystem(
    system_id="IRR_001",
    zones=4,
    max_flow_rate=100.0
)

# Ativar em modo automático
irrigation.start(IrrigationMode.AUTOMATIC)

# Abrir zona e definir vazão
irrigation.open_zone(1)
irrigation.set_flow_rate(45.0)

# Irrigar por 20 minutos
irrigation.irrigate_zone(1, duration_minutes=20.0)
```

### Exemplo: Protocolo CAN

```python
from src.protocols.can_protocol import CANProtocol, CANBaudRate

# Inicializar CAN Bus
can = CANProtocol(
    bus_id="CAN0",
    baudrate=CANBaudRate.RATE_250K,
    node_address=0x17
)
can.start()

# Enviar dados de sensor
can.send_sensor_data('temperature', 25.5)
can.send_sensor_data('humidity', 65.2)

# Enviar comando para atuador
can.send_actuator_command('irrigation', 'start')
can.send_actuator_command('irrigation', 'set_rate', 450)
```

## 📊 Funcionalidades do Dashboard

### 1. Monitoramento em Tempo Real

- Temperatura, umidade do ar e do solo
- Níveis de nutrientes (N, P, K)
- pH do solo
- Condições climáticas

### 2. Controle de Atuadores

- Sistema de irrigação com 4 zonas independentes
- Controle de vazão e pressão
- Sistema de fertilização com múltiplos tipos de NPK
- Estatísticas de consumo

### 3. Protocolos de Comunicação

- Monitor de mensagens CAN Bus
- Status de conexão ISOBUS
- Comandos Task Controller
- Logs de comunicação

### 4. Mapas e Análises

- Mapa de calor de produtividade
- Zonas de manejo
- Análise de tendências
- Recomendações automáticas

## 🧪 Testes

Execute os módulos individuais para testar:

```bash
# Testar sensor de solo
python -m src.sensors.soil_sensor

# Testar estação meteorológica
python -m src.sensors.weather_sensor

# Testar GPS
python -m src.sensors.gps_sensor

# Testar sistema de irrigação
python -m src.actuators.irrigation

# Testar protocolo CAN
python -m src.protocols.can_protocol
```

## 📚 Documentação Adicional

- [Arquitetura do Sistema](docs/ARCHITECTURE.md)
- [Referência de APIs](docs/API_REFERENCE.md)
- [Manual do Usuário](docs/USER_MANUAL.md)

## 🎓 Conceitos Demonstrados

### Sistemas Embarcados

- Arquitetura de software embarcado
- Gerenciamento de sensores e atuadores
- Comunicação em tempo real
- Tratamento de erros e exceções

### Protocolos de Comunicação

- **CAN Bus**: Implementação de mensagens CAN padrão e estendidas
- **ISOBUS**: Simulação do ISO 11783 para máquinas agrícolas
- Task Controller e Process Data

### Agricultura de Precisão

- Monitoramento multi-sensor
- Controle de taxa variável
- Mapeamento de produtividade
- Zonas de manejo diferenciado

### Boas Práticas

- Código modular e reutilizável
- Documentação completa com docstrings
- Type hints para melhor legibilidade
- Sistema de logs estruturado
- Tratamento de exceções

## 🚜 Aplicações Reais

Este projeto simula funcionalidades encontradas em:

- Tratores autônomos
- Pulverizadores inteligentes
- Semeadoras com taxa variável
- Colheitadeiras com mapeamento
- Sistemas de irrigação de precisão
- Estações meteorológicas agrícolas

## 👨‍💻 Autor

**Daniel**

- GitHub: [@Daniel-1984](https://github.com/Daniel-1984)
- Localização: Curitiba, PR - Brasil
- Projeto: Portfólio para Engenheiro Embarcado Júnior

## 🎯 Desenvolvido Para

Vaga de **Engenheiro Embarcado Júnior** especializado em **Automação Agrícola**

Demonstrando competências em:

- Desenvolvimento de sistemas embarcados
- Programação em Python e C
- Protocolos CAN e ISOBUS
- Integração de sensores e atuadores
- Agricultura de precisão
- Documentação técnica

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

Desenvolvido como projeto de demonstração de competências técnicas para processos seletivos na área de automação agrícola e sistemas embarcados.

---

<p align="center">
  <strong>🌾 AgriSense - Tecnologia para o campo do futuro 🚜</strong>
</p>

<p align="center">
  Feito com ❤️ e Python
</p>
