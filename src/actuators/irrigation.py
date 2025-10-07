"""
Irrigation System Module
Sistema de controle de irrigação automatizado para agricultura de precisão
Controla: válvulas, bombas, vazão, pressão
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from enum import Enum


class IrrigationMode(Enum):
    """Modos de operação do sistema de irrigação"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SCHEDULED = "scheduled"
    OFF = "off"


class IrrigationSystem:
    """
    Classe que simula um sistema de irrigação embarcado
    
    Atributos:
        system_id (str): Identificador único do sistema
        zones (int): Número de zonas de irrigação
        max_flow_rate (float): Vazão máxima em L/min
    """
    
    def __init__(self, system_id: str, zones: int = 4, max_flow_rate: float = 100.0):
        """
        Inicializa o sistema de irrigação
        
        Args:
            system_id: ID único do sistema
            zones: Número de zonas de irrigação
            max_flow_rate: Vazão máxima em L/min
        """
        self.system_id = system_id
        self.num_zones = zones
        self.max_flow_rate = max_flow_rate
        
        # Estado do sistema
        self.is_active = False
        self.mode = IrrigationMode.OFF
        self.current_flow_rate = 0.0
        self.current_pressure = 0.0  # Bar
        self.total_volume = 0.0  # Litros totais
        
        # Estado das zonas
        self.zones_status = {i: False for i in range(1, zones + 1)}
        
        # Estatísticas
        self.operation_time = 0  # Minutos
        self.last_irrigation = None
        self.next_scheduled = None
        
        # Setpoints
        self.target_soil_moisture = 50.0  # % - para modo automático
        self.schedule_times = []  # Horários programados
        
        print(f"✅ Sistema de Irrigação {self.system_id} inicializado")
        print(f"   Número de zonas: {self.num_zones}")
        print(f"   Vazão máxima: {self.max_flow_rate} L/min")
    
    def start(self, mode: IrrigationMode = IrrigationMode.MANUAL):
        """
        Ativa o sistema de irrigação
        
        Args:
            mode: Modo de operação
        """
        self.is_active = True
        self.mode = mode
        print(f"🟢 Sistema {self.system_id} ATIVADO - Modo: {mode.value}")
    
    def stop(self):
        """Desativa o sistema de irrigação"""
        self.is_active = False
        self.mode = IrrigationMode.OFF
        self.current_flow_rate = 0.0
        self.current_pressure = 0.0
        
        # Desativa todas as zonas
        for zone in self.zones_status:
            self.zones_status[zone] = False
        
        print(f"🔴 Sistema {self.system_id} DESATIVADO")
    
    def open_zone(self, zone_number: int) -> bool:
        """
        Abre válvula de uma zona específica
        
        Args:
            zone_number: Número da zona (1 a num_zones)
        
        Returns:
            bool: True se sucesso
        """
        if not self.is_active:
            print(f"⚠️ Sistema não está ativo!")
            return False
        
        if zone_number not in self.zones_status:
            print(f"⚠️ Zona {zone_number} não existe!")
            return False
        
        self.zones_status[zone_number] = True
        print(f"💧 Zona {zone_number} ABERTA")
        
        # Atualiza vazão e pressão
        self._update_flow_and_pressure()
        
        return True
    
    def close_zone(self, zone_number: int) -> bool:
        """
        Fecha válvula de uma zona específica
        
        Args:
            zone_number: Número da zona
        
        Returns:
            bool: True se sucesso
        """
        if zone_number not in self.zones_status:
            print(f"⚠️ Zona {zone_number} não existe!")
            return False
        
        self.zones_status[zone_number] = False
        print(f"🔒 Zona {zone_number} FECHADA")
        
        # Atualiza vazão e pressão
        self._update_flow_and_pressure()
        
        return True
    
    def set_flow_rate(self, flow_rate: float) -> bool:
        """
        Define vazão do sistema
        
        Args:
            flow_rate: Vazão desejada em L/min
        
        Returns:
            bool: True se sucesso
        """
        if not self.is_active:
            print(f"⚠️ Sistema não está ativo!")
            return False
        
        if flow_rate < 0 or flow_rate > self.max_flow_rate:
            print(f"⚠️ Vazão deve estar entre 0 e {self.max_flow_rate} L/min")
            return False
        
        self.current_flow_rate = flow_rate
        print(f"💦 Vazão ajustada para {flow_rate} L/min")
        
        return True
    
    def _update_flow_and_pressure(self):
        """Atualiza vazão e pressão baseado nas zonas abertas"""
        active_zones = sum(1 for status in self.zones_status.values() if status)
        
        if active_zones == 0:
            self.current_flow_rate = 0.0
            self.current_pressure = 0.0
        else:
            # Distribui vazão entre zonas ativas
            self.current_flow_rate = min(
                self.max_flow_rate,
                active_zones * (self.max_flow_rate / self.num_zones)
            )
            
            # Pressão varia com número de zonas (simulação)
            base_pressure = 2.5  # Bar
            self.current_pressure = base_pressure + random.uniform(-0.2, 0.2)
    
    def irrigate_zone(self, zone_number: int, duration_minutes: float):
        """
        Irriga uma zona por determinado tempo
        
        Args:
            zone_number: Número da zona
            duration_minutes: Duração em minutos
        """
        if not self.is_active:
            print(f"⚠️ Sistema não está ativo!")
            return
        
        print(f"💧 Iniciando irrigação da Zona {zone_number} por {duration_minutes} min")
        
        self.open_zone(zone_number)
        self.operation_time += duration_minutes
        
        # Calcula volume
        volume = self.current_flow_rate * duration_minutes
        self.total_volume += volume
        
        print(f"✅ Irrigação concluída - Volume: {volume:.1f} L")
        
        self.close_zone(zone_number)
        self.last_irrigation = datetime.now()
    
    def auto_irrigate(self, current_soil_moisture: float) -> bool:
        """
        Modo automático: irriga baseado na umidade do solo
        
        Args:
            current_soil_moisture: Umidade atual do solo em %
        
        Returns:
            bool: True se irrigação foi ativada
        """
        if not self.is_active or self.mode != IrrigationMode.AUTOMATIC:
            return False
        
        if current_soil_moisture < self.target_soil_moisture:
            deficit = self.target_soil_moisture - current_soil_moisture
            
            # Calcula tempo de irrigação necessário (simplificado)
            duration = min(30, deficit * 2)  # Máximo 30 minutos
            
            print(f"🤖 Irrigação automática acionada!")
            print(f"   Umidade atual: {current_soil_moisture}%")
            print(f"   Umidade alvo: {self.target_soil_moisture}%")
            print(f"   Duração: {duration:.1f} min")
            
            # Irriga todas as zonas
            for zone in range(1, self.num_zones + 1):
                self.open_zone(zone)
            
            return True
        
        return False
    
    def schedule_irrigation(self, times: List[str]):
        """
        Programa horários de irrigação
        
        Args:
            times: Lista de horários no formato "HH:MM"
        """
        self.schedule_times = times
        print(f"📅 Irrigação programada para: {', '.join(times)}")
        
        # Define próxima irrigação
        self._update_next_scheduled()
    
    def _update_next_scheduled(self):
        """Atualiza próximo horário programado"""
        if not self.schedule_times:
            self.next_scheduled = None
            return
        
        now = datetime.now()
        today = now.date()
        
        # Procura próximo horário hoje
        for time_str in sorted(self.schedule_times):
            hour, minute = map(int, time_str.split(':'))
            scheduled_time = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
            
            if scheduled_time > now:
                self.next_scheduled = scheduled_time
                return
        
        # Se não há mais hoje, usa primeiro horário de amanhã
        hour, minute = map(int, sorted(self.schedule_times)[0].split(':'))
        tomorrow = today + timedelta(days=1)
        self.next_scheduled = datetime.combine(tomorrow, datetime.min.time().replace(hour=hour, minute=minute))
    
    def get_status(self) -> Dict[str, any]:
        """
        Retorna status completo do sistema
        
        Returns:
            dict: Status do sistema
        """
        active_zones = [zone for zone, status in self.zones_status.items() if status]
        
        return {
            'system_id': self.system_id,
            'is_active': self.is_active,
            'mode': self.mode.value,
            'flow_rate': round(self.current_flow_rate, 2),
            'pressure': round(self.current_pressure, 2),
            'total_volume': round(self.total_volume, 1),
            'operation_time_minutes': self.operation_time,
            'active_zones': active_zones,
            'zones_status': self.zones_status,
            'last_irrigation': self.last_irrigation.isoformat() if self.last_irrigation else None,
            'next_scheduled': self.next_scheduled.isoformat() if self.next_scheduled else None,
            'target_moisture': self.target_soil_moisture
        }
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas de uso
        
        Returns:
            dict: Estatísticas
        """
        return {
            'total_volume_liters': round(self.total_volume, 1),
            'operation_hours': round(self.operation_time / 60, 2),
            'average_flow_rate': round(self.total_volume / max(self.operation_time, 1), 2),
            'last_irrigation': self.last_irrigation,
            'irrigations_today': 0  # Seria calculado com histórico real
        }
    
    def __repr__(self):
        status = "ATIVO" if self.is_active else "INATIVO"
        return f"IrrigationSystem(id={self.system_id}, status={status}, mode={self.mode.value})"


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste do Sistema de Irrigação ===\n")
    
    # Criar sistema
    irrigation = IrrigationSystem(
        system_id="IRR_001",
        zones=4,
        max_flow_rate=100.0
    )
    
    # Ativar em modo manual
    irrigation.start(IrrigationMode.MANUAL)
    
    # Abrir zona 1
    irrigation.open_zone(1)
    irrigation.set_flow_rate(45.0)
    
    print("\n📊 Status:")
    status = irrigation.get_status()
    print(f"  Vazão: {status['flow_rate']} L/min")
    print(f"  Pressão: {status['pressure']} Bar")
    print(f"  Zonas ativas: {status['active_zones']}")
    
    # Simular irrigação
    print("\n💧 Simulando irrigação...")
    irrigation.irrigate_zone(1, 10.0)
    
    # Modo automático
    print("\n🤖 Testando modo automático...")
    irrigation.mode = IrrigationMode.AUTOMATIC
    irrigation.target_soil_moisture = 60.0
    irrigation.auto_irrigate(current_soil_moisture=45.0)
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = irrigation.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Desativar
    irrigation.stop()