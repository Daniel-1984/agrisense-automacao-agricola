"""
Logger Module
Sistema de logging estruturado para agricultura de precisão
Registra eventos, alertas, erros e operações do sistema
"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import json


class LogLevel(Enum):
    """Níveis de log"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class EventType(Enum):
    """Tipos de eventos do sistema"""
    SENSOR_READING = "sensor_reading"
    ACTUATOR_COMMAND = "actuator_command"
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    ERROR = "error"
    ALERT = "alert"
    IRRIGATION = "irrigation"
    FERTILIZATION = "fertilization"
    CAN_MESSAGE = "can_message"
    ISOBUS_MESSAGE = "isobus_message"


class AgriLogger:
    """
    Sistema de logging para agricultura de precisão
    
    Attributes:
        name (str): Nome do logger
        log_dir (str): Diretório dos logs
    """
    
    def __init__(self, name: str = "AgriSense", log_dir: str = "logs"):
        """
        Inicializa o sistema de logging
        
        Args:
            name: Nome do logger
            log_dir: Diretório para salvar logs
        """
        self.name = name
        self.log_dir = log_dir
        
        # Cria diretório de logs se não existir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configura logger principal
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove handlers existentes
        self.logger.handlers.clear()
        
        # Configura handlers
        self._setup_handlers()
        
        print(f"✅ Sistema de logs inicializado: {name}")
        print(f"   Diretório: {log_dir}")
    
    def _setup_handlers(self):
        """Configura handlers de log (arquivo e console)"""
        
        # Formato de log detalhado
        detailed_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Formato de log simples para console
        simple_format = logging.Formatter(
            '%(levelname)s | %(message)s'
        )
        
        # Handler para arquivo (todos os níveis)
        today = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(
            os.path.join(self.log_dir, f'{self.name}_{today}.log'),
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_format)
        self.logger.addHandler(file_handler)
        
        # Handler para console (INFO e acima)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_format)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs):
        """
        Log de debug
        
        Args:
            message: Mensagem
            **kwargs: Dados adicionais
        """
        self.logger.debug(self._format_message(message, kwargs))
    
    def info(self, message: str, **kwargs):
        """
        Log de informação
        
        Args:
            message: Mensagem
            **kwargs: Dados adicionais
        """
        self.logger.info(self._format_message(message, kwargs))
    
    def warning(self, message: str, **kwargs):
        """
        Log de aviso
        
        Args:
            message: Mensagem
            **kwargs: Dados adicionais
        """
        self.logger.warning(self._format_message(message, kwargs))
    
    def error(self, message: str, **kwargs):
        """
        Log de erro
        
        Args:
            message: Mensagem
            **kwargs: Dados adicionais
        """
        self.logger.error(self._format_message(message, kwargs))
    
    def critical(self, message: str, **kwargs):
        """
        Log crítico
        
        Args:
            message: Mensagem
            **kwargs: Dados adicionais
        """
        self.logger.critical(self._format_message(message, kwargs))
    
    def _format_message(self, message: str, data: Dict[str, Any]) -> str:
        """
        Formata mensagem com dados adicionais
        
        Args:
            message: Mensagem base
            data: Dados adicionais
        
        Returns:
            str: Mensagem formatada
        """
        if data:
            data_str = " | ".join([f"{k}={v}" for k, v in data.items()])
            return f"{message} | {data_str}"
        return message
    
    def log_event(self, event_type: EventType, message: str, data: Optional[Dict[str, Any]] = None):
        """
        Registra evento estruturado
        
        Args:
            event_type: Tipo do evento
            message: Mensagem
            data: Dados do evento
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type.value,
            'message': message,
            'data': data or {}
        }
        
        self.info(f"[{event_type.value.upper()}] {message}", **event['data'])
        
        # Salva evento em arquivo JSON (log estruturado)
        self._save_event_json(event)
    
    def _save_event_json(self, event: Dict[str, Any]):
        """
        Salva evento em formato JSON
        
        Args:
            event: Evento para salvar
        """
        today = datetime.now().strftime('%Y-%m-%d')
        json_file = os.path.join(self.log_dir, f'{self.name}_events_{today}.json')
        
        # Lê eventos existentes
        events = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    events = json.load(f)
            except:
                events = []
        
        # Adiciona novo evento
        events.append(event)
        
        # Salva de volta
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
    
    def log_sensor_reading(self, sensor_id: str, sensor_type: str, value: float, unit: str):
        """
        Registra leitura de sensor
        
        Args:
            sensor_id: ID do sensor
            sensor_type: Tipo do sensor
            value: Valor lido
            unit: Unidade
        """
        self.log_event(
            EventType.SENSOR_READING,
            f"Sensor {sensor_type} leitura",
            {
                'sensor_id': sensor_id,
                'sensor_type': sensor_type,
                'value': value,
                'unit': unit
            }
        )
    
    def log_actuator_command(self, actuator_id: str, actuator_type: str, command: str, parameters: Dict[str, Any]):
        """
        Registra comando de atuador
        
        Args:
            actuator_id: ID do atuador
            actuator_type: Tipo do atuador
            command: Comando enviado
            parameters: Parâmetros do comando
        """
        self.log_event(
            EventType.ACTUATOR_COMMAND,
            f"Comando {command} para {actuator_type}",
            {
                'actuator_id': actuator_id,
                'actuator_type': actuator_type,
                'command': command,
                'parameters': parameters
            }
        )
    
    def log_irrigation(self, zone: int, duration: float, volume: float):
        """
        Registra evento de irrigação
        
        Args:
            zone: Zona irrigada
            duration: Duração em minutos
            volume: Volume em litros
        """
        self.log_event(
            EventType.IRRIGATION,
            f"Irrigação zona {zone}",
            {
                'zone': zone,
                'duration_minutes': duration,
                'volume_liters': volume
            }
        )
    
    def log_fertilization(self, fertilizer_type: str, area: float, rate: float, total: float):
        """
        Registra evento de fertilização
        
        Args:
            fertilizer_type: Tipo de fertilizante
            area: Área em hectares
            rate: Taxa em kg/ha
            total: Total aplicado em kg
        """
        self.log_event(
            EventType.FERTILIZATION,
            f"Fertilização com {fertilizer_type}",
            {
                'fertilizer_type': fertilizer_type,
                'area_hectares': area,
                'rate_kg_ha': rate,
                'total_kg': total
            }
        )
    
    def log_alert(self, alert_type: str, severity: str, message: str, source: str):
        """
        Registra alerta do sistema
        
        Args:
            alert_type: Tipo do alerta
            severity: Severidade (low, medium, high, critical)
            message: Mensagem do alerta
            source: Origem do alerta
        """
        self.log_event(
            EventType.ALERT,
            f"ALERTA [{severity.upper()}] {alert_type}: {message}",
            {
                'alert_type': alert_type,
                'severity': severity,
                'source': source
            }
        )
    
    def log_can_message(self, can_id: int, data: bytes, direction: str):
        """
        Registra mensagem CAN
        
        Args:
            can_id: ID CAN
            data: Dados da mensagem
            direction: 'TX' ou 'RX'
        """
        data_hex = ' '.join(f'{b:02X}' for b in data)
        
        self.debug(
            f"CAN {direction}",
            can_id=f"0x{can_id:X}",
            data=data_hex
        )
    
    def log_isobus_message(self, pgn: int, source: int, destination: int, description: str):
        """
        Registra mensagem ISOBUS
        
        Args:
            pgn: Parameter Group Number
            source: Endereço fonte
            destination: Endereço destino
            description: Descrição da mensagem
        """
        self.debug(
            f"ISOBUS: {description}",
            pgn=f"0x{pgn:X}",
            source=f"0x{source:02X}",
            destination=f"0x{destination:02X}"
        )
    
    def get_log_file_path(self) -> str:
        """
        Retorna caminho do arquivo de log atual
        
        Returns:
            str: Caminho do arquivo
        """
        today = datetime.now().strftime('%Y-%m-%d')
        return os.path.join(self.log_dir, f'{self.name}_{today}.log')
    
    def get_stats(self) -> Dict[str, int]:
        """
        Retorna estatísticas dos logs
        
        Returns:
            dict: Estatísticas
        """
        stats = {
            'debug': 0,
            'info': 0,
            'warning': 0,
            'error': 0,
            'critical': 0
        }
        
        log_file = self.get_log_file_path()
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if 'DEBUG' in line:
                        stats['debug'] += 1
                    elif 'INFO' in line:
                        stats['info'] += 1
                    elif 'WARNING' in line:
                        stats['warning'] += 1
                    elif 'ERROR' in line:
                        stats['error'] += 1
                    elif 'CRITICAL' in line:
                        stats['critical'] += 1
        
        return stats


# Singleton global
_global_logger: Optional[AgriLogger] = None


def get_logger(name: str = "AgriSense") -> AgriLogger:
    """
    Obtém instância global do logger
    
    Args:
        name: Nome do logger
    
    Returns:
        AgriLogger: Instância do logger
    """
    global _global_logger
    
    if _global_logger is None:
        _global_logger = AgriLogger(name)
    
    return _global_logger


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste do Sistema de Logs ===\n")
    
    # Criar logger
    logger = AgriLogger("AgriSense_Test")
    
    # Logs básicos
    logger.info("Sistema iniciado")
    logger.debug("Modo de debug ativado", version="1.0.0")
    logger.warning("Umidade do solo abaixo do ideal", zone=1, value=35)
    logger.error("Falha na comunicação CAN", bus="CAN0")
    
    # Eventos estruturados
    logger.log_sensor_reading("SOIL_001", "soil_moisture", 45.3, "%")
    logger.log_irrigation(zone=1, duration=30.0, volume=1350.0)
    logger.log_fertilization("NPK 15-15-15", area=5.0, rate=80.0, total=400.0)
    
    # Alerta
    logger.log_alert(
        alert_type="low_moisture",
        severity="medium",
        message="Umidade do solo abaixo de 40%",
        source="SOIL_001"
    )
    
    # Estatísticas
    print("\n📊 Estatísticas dos logs:")
    stats = logger.get_stats()
    for level, count in stats.items():
        print(f"  {level}: {count}")
    
    print(f"\n📁 Arquivo de log: {logger.get_log_file_path()}")