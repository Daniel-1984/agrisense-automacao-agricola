"""
Soil Sensor Module
Simula um sensor de solo para agricultura de precisão
Mede: umidade, pH, NPK (Nitrogênio, Fósforo, Potássio)
"""

import random
import time
from datetime import datetime
from typing import Dict, Optional


class SoilSensor:
    """
    Classe que simula um sensor de solo embarcado
    
    Atributos:
        sensor_id (str): Identificador único do sensor
        location (tuple): Coordenadas (latitude, longitude)
        sampling_rate (int): Taxa de amostragem em segundos
    """
    
    def __init__(self, sensor_id: str, location: tuple = (0.0, 0.0), sampling_rate: int = 5):
        """
        Inicializa o sensor de solo
        
        Args:
            sensor_id: ID único do sensor
            location: Tupla com (latitude, longitude)
            sampling_rate: Intervalo entre leituras em segundos
        """
        self.sensor_id = sensor_id
        self.location = location
        self.sampling_rate = sampling_rate
        self.is_active = False
        self.last_reading = None
        
        # Parâmetros base para simulação realista
        self.base_moisture = 50.0  # Umidade base em %
        self.base_ph = 6.5  # pH base
        self.base_nitrogen = 30.0  # N em mg/kg
        self.base_phosphorus = 15.0  # P em mg/kg
        self.base_potassium = 40.0  # K em mg/kg
        
        print(f"✅ Sensor de Solo {self.sensor_id} inicializado")
        print(f"   Localização: {self.location}")
        print(f"   Taxa de amostragem: {self.sampling_rate}s")
    
    def start(self):
        """Ativa o sensor"""
        self.is_active = True
        print(f"🟢 Sensor {self.sensor_id} ATIVADO")
    
    def stop(self):
        """Desativa o sensor"""
        self.is_active = False
        print(f"🔴 Sensor {self.sensor_id} DESATIVADO")
    
    def read_moisture(self) -> float:
        """
        Lê umidade do solo
        
        Returns:
            float: Umidade em % (0-100)
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        # Simula variação natural da umidade
        variation = random.uniform(-5, 5)
        moisture = max(0, min(100, self.base_moisture + variation))
        
        return round(moisture, 2)
    
    def read_ph(self) -> float:
        """
        Lê pH do solo
        
        Returns:
            float: pH do solo (0-14)
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        # Simula variação de pH
        variation = random.uniform(-0.3, 0.3)
        ph = max(0, min(14, self.base_ph + variation))
        
        return round(ph, 2)
    
    def read_npk(self) -> Dict[str, float]:
        """
        Lê níveis de nutrientes NPK
        
        Returns:
            dict: {'nitrogen': float, 'phosphorus': float, 'potassium': float}
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        npk = {
            'nitrogen': round(self.base_nitrogen + random.uniform(-5, 5), 2),
            'phosphorus': round(self.base_phosphorus + random.uniform(-3, 3), 2),
            'potassium': round(self.base_potassium + random.uniform(-8, 8), 2)
        }
        
        return npk
    
    def read_all(self) -> Dict[str, any]:
        """
        Realiza leitura completa de todos os parâmetros
        
        Returns:
            dict: Dicionário com todas as leituras e metadados
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        npk = self.read_npk()
        
        reading = {
            'sensor_id': self.sensor_id,
            'timestamp': datetime.now().isoformat(),
            'location': self.location,
            'moisture': self.read_moisture(),
            'ph': self.read_ph(),
            'nitrogen': npk['nitrogen'],
            'phosphorus': npk['phosphorus'],
            'potassium': npk['potassium'],
            'temperature_soil': round(random.uniform(18, 28), 1)  # Temperatura do solo
        }
        
        self.last_reading = reading
        return reading
    
    def get_status(self) -> Dict[str, any]:
        """
        Retorna status atual do sensor
        
        Returns:
            dict: Status do sensor
        """
        return {
            'sensor_id': self.sensor_id,
            'is_active': self.is_active,
            'location': self.location,
            'sampling_rate': self.sampling_rate,
            'last_reading': self.last_reading
        }
    
    def calibrate(self, moisture: float = None, ph: float = None):
        """
        Calibra os valores base do sensor
        
        Args:
            moisture: Novo valor base de umidade
            ph: Novo valor base de pH
        """
        if moisture is not None:
            self.base_moisture = moisture
            print(f"🔧 Umidade base calibrada para {moisture}%")
        
        if ph is not None:
            self.base_ph = ph
            print(f"🔧 pH base calibrado para {ph}")
    
    def __repr__(self):
        status = "ATIVO" if self.is_active else "INATIVO"
        return f"SoilSensor(id={self.sensor_id}, status={status}, location={self.location})"


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste do Sensor de Solo ===\n")
    
    # Criar sensor
    sensor = SoilSensor(
        sensor_id="SOIL_001",
        location=(-25.4284, -49.2733),  # Curitiba, PR
        sampling_rate=5
    )
    
    # Ativar sensor
    sensor.start()
    
    # Realizar 3 leituras
    print("\n📊 Realizando leituras...\n")
    for i in range(3):
        reading = sensor.read_all()
        print(f"Leitura {i+1}:")
        print(f"  💧 Umidade: {reading['moisture']}%")
        print(f"  🧪 pH: {reading['ph']}")
        print(f"  🌱 N: {reading['nitrogen']} mg/kg")
        print(f"  🌱 P: {reading['phosphorus']} mg/kg")
        print(f"  🌱 K: {reading['potassium']} mg/kg")
        print(f"  🌡️ Temp Solo: {reading['temperature_soil']}°C")
        print()
        time.sleep(2)
    
    # Status do sensor
    print("Status:", sensor.get_status())
    
    # Desativar
    sensor.stop()