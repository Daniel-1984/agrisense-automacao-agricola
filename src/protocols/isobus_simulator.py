"""
CAN Protocol Module
Simula protocolo CAN (Controller Area Network) para sistemas embarcados
Usado em automação agrícola para comunicação entre ECUs
"""

import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class CANBaudRate(Enum):
    """Taxas de transmissão CAN padrão"""
    RATE_125K = 125000
    RATE_250K = 250000
    RATE_500K = 500000
    RATE_1M = 1000000


class CANMessagePriority(Enum):
    """Prioridade das mensagens CAN"""
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class CANMessage:
    """
    Representa uma mensagem CAN
    
    Atributos:
        can_id (int): Identificador CAN (11 ou 29 bits)
        data (bytes): Dados (0-8 bytes)
        timestamp (float): Timestamp da mensagem
        is_extended (bool): Se usa ID estendido (29 bits)
    """
    
    def __init__(self, can_id: int, data: bytes, is_extended: bool = False):
        """
        Cria uma mensagem CAN
        
        Args:
            can_id: ID CAN (0x000-0x7FF para padrão, 0x00000000-0x1FFFFFFF para estendido)
            data: Dados em bytes (máximo 8 bytes)
            is_extended: Se True, usa ID de 29 bits
        """
        if len(data) > 8:
            raise ValueError("Mensagem CAN pode ter no máximo 8 bytes")
        
        if is_extended:
            if can_id > 0x1FFFFFFF:
                raise ValueError("ID estendido deve ser <= 0x1FFFFFFF")
        else:
            if can_id > 0x7FF:
                raise ValueError("ID padrão deve ser <= 0x7FF")
        
        self.can_id = can_id
        self.data = data
        self.is_extended = is_extended
        self.timestamp = time.time()
        self.dlc = len(data)  # Data Length Code
    
    def __repr__(self):
        data_hex = ' '.join(f'{b:02X}' for b in self.data)
        id_format = "Extended" if self.is_extended else "Standard"
        return f"CAN({id_format} ID=0x{self.can_id:X}, DLC={self.dlc}, Data=[{data_hex}])"


class CANProtocol:
    """
    Classe que simula um controlador CAN Bus
    
    Atributos:
        bus_id (str): Identificador único do bus CAN
        baudrate (CANBaudRate): Taxa de transmissão
        node_address (int): Endereço deste nó na rede
    """
    
    def __init__(self, bus_id: str = "CAN0", baudrate: CANBaudRate = CANBaudRate.RATE_250K, node_address: int = 0x01):
        """
        Inicializa o controlador CAN
        
        Args:
            bus_id: ID do bus CAN
            baudrate: Taxa de transmissão
            node_address: Endereço deste nó (0x00-0xFF)
        """
        self.bus_id = bus_id
        self.baudrate = baudrate
        self.node_address = node_address
        
        # Estado do bus
        self.is_active = False
        self.bus_load = 0.0  # Carga do bus em %
        self.error_count = 0
        
        # Buffers de mensagens
        self.tx_buffer = []  # Mensagens a transmitir
        self.rx_buffer = []  # Mensagens recebidas
        
        # Estatísticas
        self.messages_sent = 0
        self.messages_received = 0
        self.errors = []
        
        # Filtros de recepção
        self.rx_filters = []  # Lista de IDs aceitos
        
        print(f"✅ CAN Bus {self.bus_id} inicializado")
        print(f"   Baudrate: {self.baudrate.value} bps")
        print(f"   Endereço do nó: 0x{self.node_address:02X}")
    
    def start(self):
        """Ativa o bus CAN"""
        self.is_active = True
        self.error_count = 0
        print(f"🟢 CAN Bus {self.bus_id} ATIVO")
    
    def stop(self):
        """Desativa o bus CAN"""
        self.is_active = False
        print(f"🔴 CAN Bus {self.bus_id} DESATIVADO")
    
    def send_message(self, can_id: int, data: bytes, is_extended: bool = False) -> bool:
        """
        Envia mensagem CAN
        
        Args:
            can_id: ID da mensagem
            data: Dados em bytes (máximo 8 bytes)
            is_extended: Se usa ID estendido
        
        Returns:
            bool: True se enviado com sucesso
        """
        if not self.is_active:
            print(f"⚠️ Bus CAN não está ativo!")
            return False
        
        try:
            message = CANMessage(can_id, data, is_extended)
            
            # Simula envio (na realidade seria hardware)
            self.tx_buffer.append(message)
            self.messages_sent += 1
            
            # Simula carga do bus
            self._update_bus_load()
            
            print(f"📤 Enviado: {message}")
            
            return True
        
        except Exception as e:
            print(f"❌ Erro ao enviar: {e}")
            self.error_count += 1
            self.errors.append({'timestamp': datetime.now(), 'error': str(e)})
            return False
    
    def receive_message(self) -> Optional[CANMessage]:
        """
        Recebe mensagem do buffer
        
        Returns:
            CANMessage ou None se buffer vazio
        """
        if not self.is_active:
            return None
        
        if self.rx_buffer:
            message = self.rx_buffer.pop(0)
            self.messages_received += 1
            print(f"📥 Recebido: {message}")
            return message
        
        return None
    
    def simulate_incoming_message(self, can_id: int, data: bytes, is_extended: bool = False):
        """
        Simula recepção de mensagem (para testes)
        
        Args:
            can_id: ID da mensagem
            data: Dados
            is_extended: Se é ID estendido
        """
        if not self.is_active:
            return
        
        # Verifica filtros
        if self.rx_filters and can_id not in self.rx_filters:
            return  # Mensagem filtrada
        
        message = CANMessage(can_id, data, is_extended)
        self.rx_buffer.append(message)
    
    def add_rx_filter(self, can_id: int):
        """
        Adiciona filtro de recepção
        
        Args:
            can_id: ID CAN a aceitar
        """
        if can_id not in self.rx_filters:
            self.rx_filters.append(can_id)
            print(f"🔍 Filtro adicionado: 0x{can_id:X}")
    
    def clear_rx_filters(self):
        """Remove todos os filtros (aceita todas as mensagens)"""
        self.rx_filters = []
        print(f"🔍 Filtros limpos - aceitando todas as mensagens")
    
    def _update_bus_load(self):
        """Atualiza carga do bus CAN"""
        # Simulação simplificada de carga
        messages_per_sec = len(self.tx_buffer) + len(self.rx_buffer)
        
        # CAN frame: ~130 bits (aproximado)
        # Carga = (mensagens/s * bits/mensagem) / baudrate
        bits_per_sec = messages_per_sec * 130
        self.bus_load = min(100, (bits_per_sec / self.baudrate.value) * 100)
    
    def send_sensor_data(self, sensor_type: str, value: float) -> bool:
        """
        Envia dados de sensor via CAN
        
        Args:
            sensor_type: Tipo do sensor ('temperature', 'humidity', 'pressure', etc)
            value: Valor do sensor
        
        Returns:
            bool: True se enviado
        """
        # Define IDs CAN específicos por tipo de sensor
        sensor_ids = {
            'temperature': 0x100,
            'humidity': 0x101,
            'pressure': 0x102,
            'soil_moisture': 0x103,
            'npk': 0x104
        }
        
        can_id = sensor_ids.get(sensor_type, 0x1FF)
        
        # Converte valor float para bytes (little-endian)
        data = int(value * 100).to_bytes(4, byteorder='little', signed=True)
        data += bytes([0, 0, 0, 0])  # Padding para 8 bytes
        
        return self.send_message(can_id, data)
    
    def send_actuator_command(self, actuator_type: str, command: str, value: int = 0) -> bool:
        """
        Envia comando para atuador via CAN
        
        Args:
            actuator_type: Tipo do atuador ('irrigation', 'fertilizer')
            command: Comando ('start', 'stop', 'set_rate')
            value: Valor opcional
        
        Returns:
            bool: True se enviado
        """
        actuator_ids = {
            'irrigation': 0x200,
            'fertilizer': 0x201,
            'valve': 0x202
        }
        
        commands = {
            'start': 0x01,
            'stop': 0x02,
            'set_rate': 0x03,
            'status': 0x04
        }
        
        can_id = actuator_ids.get(actuator_type, 0x2FF)
        cmd_byte = commands.get(command, 0x00)
        
        # Formato: [CMD, VALUE_H, VALUE_L, 0, 0, 0, 0, 0]
        data = bytes([cmd_byte, (value >> 8) & 0xFF, value & 0xFF, 0, 0, 0, 0, 0])
        
        return self.send_message(can_id, data)
    
    def get_status(self) -> Dict[str, any]:
        """
        Retorna status do bus CAN
        
        Returns:
            dict: Status
        """
        return {
            'bus_id': self.bus_id,
            'is_active': self.is_active,
            'baudrate': self.baudrate.value,
            'node_address': f"0x{self.node_address:02X}",
            'bus_load_percent': round(self.bus_load, 2),
            'messages_sent': self.messages_sent,
            'messages_received': self.messages_received,
            'error_count': self.error_count,
            'tx_buffer_size': len(self.tx_buffer),
            'rx_buffer_size': len(self.rx_buffer),
            'rx_filters': [f"0x{id:X}" for id in self.rx_filters]
        }
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas de comunicação
        
        Returns:
            dict: Estatísticas
        """
        total_messages = self.messages_sent + self.messages_received
        error_rate = (self.error_count / max(total_messages, 1)) * 100
        
        return {
            'total_messages': total_messages,
            'messages_sent': self.messages_sent,
            'messages_received': self.messages_received,
            'error_count': self.error_count,
            'error_rate_percent': round(error_rate, 2),
            'average_bus_load': round(self.bus_load, 2)
        }
    
    def __repr__(self):
        status = "ATIVO" if self.is_active else "INATIVO"
        return f"CANProtocol(id={self.bus_id}, status={status}, baudrate={self.baudrate.value})"


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste do Protocolo CAN ===\n")
    
    # Criar controlador CAN
    can = CANProtocol(
        bus_id="CAN0",
        baudrate=CANBaudRate.RATE_250K,
        node_address=0x17
    )
    
    # Ativar bus
    can.start()
    
    # Enviar dados de sensores
    print("\n📤 Enviando dados de sensores...")
    can.send_sensor_data('temperature', 25.5)
    can.send_sensor_data('humidity', 65.2)
    can.send_sensor_data('soil_moisture', 48.7)
    
    # Enviar comandos para atuadores
    print("\n📤 Enviando comandos para atuadores...")
    can.send_actuator_command('irrigation', 'start')
    can.send_actuator_command('irrigation', 'set_rate', 450)
    can.send_actuator_command('fertilizer', 'start')
    
    # Simular recepção de mensagens
    print("\n📥 Simulando recepção...")
    can.simulate_incoming_message(0x300, bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]))
    
    received = can.receive_message()
    if received:
        print(f"Mensagem recebida: {received}")
    
    # Status e estatísticas
    print("\n📊 Status:")
    status = can.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n📊 Estatísticas:")
    stats = can.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Desativar
    can.stop()