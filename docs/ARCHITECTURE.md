# 🏗️ Arquitetura do Sistema AgriSense

## Visão Geral

AgriSense é um sistema embarcado de automação agrícola desenvolvido com arquitetura modular em camadas, seguindo princípios de design orientado a objetos e boas práticas de engenharia de software.

## 📐 Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│                  CAMADA DE APRESENTAÇÃO                  │
│                    (app.py - Streamlit)                  │
│              Dashboard Web Interativo                    │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   CAMADA DE APLICAÇÃO                    │
│                  (Lógica de Negócio)                     │
│   - Controle de Irrigação                               │
│   - Gestão de Fertilização                              │
│   - Análise de Dados                                    │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  CAMADA DE PROTOCOLO                     │
│              (CAN Bus / ISOBUS)                          │
│   - Comunicação entre ECUs                              │
│   - Gerenciamento de mensagens                          │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    CAMADA DE HARDWARE                    │
│           (Sensores e Atuadores Simulados)              │
│   - Sensores: Solo, Clima, GPS                         │
│   - Atuadores: Irrigação, Fertilização                 │
└─────────────────────────────────────────────────────────┘
```

## 🧩 Componentes Principais

### 1. Módulo de Sensores (`src/sensors/`)

#### SoilSensor

**Responsabilidade**: Monitoramento das condições do solo

**Funcionalidades**:

- Leitura de umidade (0-100%)
- Medição de pH (0-14)
- Análise de nutrientes NPK (mg/kg)
- Temperatura do solo

**Interfaces**:

```python
class SoilSensor:
    def start() -> None
    def stop() -> None
    def read_moisture() -> float
    def read_ph() -> float
    def read_npk() -> Dict[str, float]
    def read_all() -> Dict[str, any]
    def get_status() -> Dict[str, any]
```

**Comunicação**: Envia dados via CAN Bus (IDs 0x100-0x104)

#### WeatherSensor

**Responsabilidade**: Monitoramento meteorológico

**Funcionalidades**:

- Temperatura e umidade do ar
- Pressão atmosférica
- Velocidade e direção do vento
- Luminosidade
- Probabilidade de chuva

**Características**:

- Taxa de amostragem: 1-60 segundos
- Precisão: ±0.1°C (temperatura), ±2% (umidade)
- Algoritmo de cálculo de índice de calor

#### GPSSensor

**Responsabilidade**: Posicionamento e navegação

**Funcionalidades**:

- Coordenadas GPS (latitude, longitude, altitude)
- Velocidade e direção (heading)
- Precisão configurável (RTK/DGPS/Standard)

**Níveis de Precisão**:

- RTK: ±2cm (agricultura de precisão)
- DGPS: ±50cm
- Standard: ±5m

**Algoritmos**:

- Fórmula de Haversine para cálculo de distâncias
- Simulação de movimento com compensação de latitude

### 2. Módulo de Atuadores (`src/actuators/`)

#### IrrigationSystem

**Responsabilidade**: Controle de irrigação automatizada

**Modos de Operação**:

1. **MANUAL**: Controle direto pelo operador
2. **AUTOMATIC**: Baseado em umidade do solo
3. **SCHEDULED**: Programação por horários
4. **OFF**: Sistema desativado

**Características**:

- 4 zonas independentes
- Vazão configurável (0-100 L/min)
- Monitoramento de pressão
- Registro de consumo

**Lógica de Controle Automático**:

```python
if umidade_atual < umidade_alvo:
    deficit = umidade_alvo - umidade_atual
    tempo_irrigacao = min(30, deficit * 2)  # máx 30 min
    irrigar(tempo_irrigacao)
```

#### FertilizerSystem

**Responsabilidade**: Aplicação controlada de fertilizantes

**Tipos de Fertilizantes**:

- NPK 20-10-10 (alto nitrogênio)
- NPK 10-20-20 (alto fósforo e potássio)
- NPK 15-15-15 (balanceado)
- Uréia 45-00-00

**Funcionalidades**:

- Taxa variável de aplicação
- Recomendação automática baseada em análise de solo
- Cálculo de dosagem por zona
- Registro de consumo por hectare

**Algoritmo de Recomendação**:

```python
deficit_N = max(0, target_N - current_N)
deficit_P = max(0, target_P - current_P)
deficit_K = max(0, target_K - current_K)

if deficit_N > 10:
    return NPK_20_10_10
elif deficit_P > 10:
    return NPK_04_14_08
# ... lógica completa
```

### 3. Módulo de Protocolos (`src/protocols/`)

#### CAN Protocol

**Responsabilidade**: Comunicação CAN Bus

**Especificações**:

- Baudrates suportados: 125k, 250k, 500k, 1M bps
- ID padrão (11 bits) e estendido (29 bits)
- Data Length Code: 0-8 bytes
- Buffer TX/RX com filtros

**Estrutura de Mensagem**:

```
┌────────────┬─────┬──────────────────┬─────┐
│  CAN ID    │ DLC │      DATA        │ CRC │
│  11/29 bits│ 4b  │    0-8 bytes     │ 15b │
└────────────┴─────┴──────────────────┴─────┘
```

**Mapeamento de IDs**:

- 0x100-0x1FF: Sensores
- 0x200-0x2FF: Atuadores
- 0x300-0x3FF: Controle do sistema

#### ISOBUS Protocol

**Responsabilidade**: Implementação ISO 11783

**Componentes**:

1. **Task Controller (TC)**: Gerenciamento de tarefas
2. **Process Data (PD)**: Dados de processo (DDI)
3. **Virtual Terminal (VT)**: Interface do operador

**Endereços Padrão**:

- 0x00: Trator
- 0xF4: Task Controller
- 0xF5: Virtual Terminal
- 0xFF: Broadcast

**Parameter Group Numbers (PGN)**:

- Definição de setpoints
- Requisição de valores
- Status de trabalho

### 4. Módulo Utilitários (`src/utils/`)

#### DataGenerator

**Responsabilidade**: Geração de dados para testes

**Datasets Disponíveis**:

- Histórico de sensores de solo
- Dados meteorológicos
- Trilhas GPS
- Logs de irrigação e fertilização
- Mapas de produtividade

**Uso**:

```python
soil_data = DataGenerator.generate_soil_data(
    num_samples=200,
    hours=48
)
```

#### Logger

**Responsabilidade**: Sistema de logs estruturado

**Níveis de Log**:

- DEBUG: Informações detalhadas
- INFO: Eventos normais
- WARNING: Avisos
- ERROR: Erros recuperáveis
- CRITICAL: Erros críticos

**Tipos de Eventos**:

- Leituras de sensores
- Comandos de atuadores
- Mensagens de protocolo
- Alertas do sistema

**Formato**:

- Logs em texto (.log)
- Eventos estruturados em JSON (.json)

## 🔄 Fluxo de Dados

### 1. Monitoramento de Sensores

```
Sensor Físico → Leitura → Protocolo CAN → Processamento → Dashboard
     ↓                                                         ↓
  [Hardware]           [can_protocol.py]                  [app.py]
                              ↓
                         Logger
```

### 2. Controle de Atuadores

```
Dashboard → Comando → Validação → Protocolo CAN → Atuador Físico
 [app.py]              [irrigation.py]    [can_protocol.py]    [Hardware]
                            ↓
                       Logger + Status
```

### 3. Comunicação ISOBUS

```
Task Controller → PGN Message → ISOBUS Network → Implemento
      ↓                              ↓
   [Trator]                      [Pulverizador]
                                      ↓
                                 Setpoints
```

## 🎯 Padrões de Design Utilizados

### 1. Singleton Pattern

**Onde**: Logger global
**Por quê**: Única instância de log para todo o sistema

### 2. Strategy Pattern

**Onde**: Modos de operação (IrrigationMode, ApplicationMode)
**Por quê**: Diferentes estratégias de controle

### 3. Observer Pattern (Implícito)

**Onde**: Sistema de eventos e alertas
**Por quê**: Notificação de mudanças de estado

### 4. Factory Pattern (Simplificado)

**Onde**: Criação de mensagens CAN
**Por quê**: Construção padronizada de objetos

## 🔐 Tratamento de Erros

### Hierarquia de Exceções

```python
Exception
    └── RuntimeError
        ├── "Sensor não está ativo"
        ├── "Bus CAN não está ativo"
        └── "Sistema não está ativo"
```

### Estratégias:

1. **Validação de entrada**: Verificação de parâmetros
2. **Estado do sistema**: Verificação se componente está ativo
3. **Limites de hardware**: Validação de valores físicos
4. **Logging automático**: Registro de todos os erros

## 📊 Performance e Otimização

### Considerações:

- **Taxa de amostragem**: Configurável (1-60s)
- **Buffers**: TX/RX com tamanho limitado
- **Carga do bus CAN**: Monitoramento de utilização
- **Simulação**: Dados realistas com baixo overhead

### Métricas:

- Latência de comunicação: < 10ms (simulado)
- Taxa de erro: < 0.1%
- Utilização de CPU: Baixa (evento-driven)

## 🧪 Testabilidade

### Características:

1. **Módulos independentes**: Cada classe pode ser testada isoladamente
2. **Dados simulados**: Geração controlada de cenários
3. **Modo de teste**: Execução de `__main__` em cada módulo
4. **Logs detalhados**: Rastreabilidade completa

### Exemplo de Teste:

```python
# Executar módulo individualmente
python -m src.sensors.soil_sensor

# Output:
# ✅ Sensor de Solo SOIL_001 inicializado
# 🟢 Sensor SOIL_001 ATIVADO
# 📊 Realizando leituras...
```

## 🚀 Escalabilidade

### Pontos de Extensão:

1. **Novos sensores**: Implementar interface base
2. **Novos protocolos**: Adicionar em `src/protocols/`
3. **Novos atuadores**: Estender `src/actuators/`
4. **Algoritmos de IA**: Integrar em camada de aplicação

### Exemplo de Extensão:

```python
# Adicionar novo sensor
class Camerasensor(BaseSensor):
    def read_image(self) -> np.ndarray:
        # Implementação
        pass
```

## 📝 Documentação do Código

### Padrão:

- **Docstrings**: Google Style
- **Type Hints**: Para todos os métodos públicos
- **Comentários**: Apenas para lógica complexa
- **README**: Em cada módulo principal

### Exemplo:

```python
def send_message(self, can_id: int, data: bytes) -> bool:
    """
    Envia mensagem CAN

    Args:
        can_id: ID da mensagem
        data: Dados (máximo 8 bytes)

    Returns:
        bool: True se enviado com sucesso

    Raises:
        RuntimeError: Se bus não está ativo
    """
```

## 🔄 Ciclo de Vida dos Componentes

### Estados Típicos:

```
INICIALIZADO → ATIVO → OPERANDO → PAUSADO → INATIVO
     ↓           ↓         ↓          ↓
   start()   comando    pause()    stop()
```

### Transições:

- Validação antes de cada transição
- Logging de mudanças de estado
- Limpeza de recursos ao desativar

## 🎓 Conceitos de Sistemas Embarcados

### Implementados:

1. ✅ Gerenciamento de periféricos (sensores/atuadores)
2. ✅ Protocolos de comunicação industrial
3. ✅ Sistema de tempo real (simulado)
4. ✅ Tratamento de interrupções (eventos)
5. ✅ Máquinas de estado
6. ✅ Logging estruturado
7. ✅ Calibração de sensores

---

<p align="center">
  <strong>Arquitetura projetada para demonstrar competências em sistemas embarcados e automação agrícola</strong>
</p>
