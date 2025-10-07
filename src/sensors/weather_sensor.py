"""
Weather Sensor Module
Simula uma estação meteorológica para agricultura de precisão
Mede: temperatura, umidade do ar, pressão atmosférica, vento, luminosidade
"""

import random
import time
from datetime import datetime
from typing import Dict, Optional


class WeatherSensor:
    """
    Classe que simula uma estação meteorológica embarcada
    
    Atributos:
        sensor_id (str): Identificador único do sensor
        location (tuple): Coordenadas (latitude, longitude)
        altitude (float): Altitude em metros
    """
    
    def __init__(self, sensor_id: str, location: tuple = (0.0, 0.0), altitude: float = 0.0):
        """
        Inicializa a estação meteorológica
        
        Args:
            sensor_id: ID único do sensor
            location: Tupla com (latitude, longitude)
            altitude: Altitude em metros
        """
        self.sensor_id = sensor_id
        self.location = location
        self.altitude = altitude
        self.is_active = False
        self.last_reading = None
        
        # Parâmetros base para simulação
        self.base_temperature = 25.0  # °C
        self.base_humidity = 60.0  # %
        self.base_pressure = 1013.25  # hPa
        self.base_wind_speed = 5.0  # km/h
        self.base_luminosity = 800.0  # lux
        
        print(f"✅ Estação Meteorológica {self.sensor_id} inicializada")
        print(f"   Localização: {self.location}")
        print(f"   Altitude: {self.altitude}m")
    
    def start(self):
        """Ativa o sensor"""
        self.is_active = True
        print(f"🟢 Estação {self.sensor_id} ATIVADA")
    
    def stop(self):
        """Desativa o sensor"""
        self.is_active = False
        print(f"🔴 Estação {self.sensor_id} DESATIVADA")
    
    def read_temperature(self) -> float:
        """
        Lê temperatura do ar
        
        Returns:
            float: Temperatura em °C
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        variation = random.uniform(-3, 3)
        temp = self.base_temperature + variation
        
        return round(temp, 1)
    
    def read_humidity(self) -> float:
        """
        Lê umidade relativa do ar
        
        Returns:
            float: Umidade em % (0-100)
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        variation = random.uniform(-10, 10)
        humidity = max(0, min(100, self.base_humidity + variation))
        
        return round(humidity, 1)
    
    def read_pressure(self) -> float:
        """
        Lê pressão atmosférica
        
        Returns:
            float: Pressão em hPa
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        variation = random.uniform(-5, 5)
        pressure = self.base_pressure + variation
        
        return round(pressure, 2)
    
    def read_wind(self) -> Dict[str, float]:
        """
        Lê velocidade e direção do vento
        
        Returns:
            dict: {'speed': float (km/h), 'direction': float (graus)}
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        wind = {
            'speed': round(max(0, self.base_wind_speed + random.uniform(-2, 5)), 1),
            'direction': round(random.uniform(0, 360), 1)
        }
        
        return wind
    
    def read_luminosity(self) -> float:
        """
        Lê intensidade luminosa
        
        Returns:
            float: Luminosidade em lux
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        # Simula variação ao longo do dia
        hour = datetime.now().hour
        if 6 <= hour <= 18:  # Dia
            base = 800
            variation = random.uniform(-100, 200)
        else:  # Noite
            base = 50
            variation = random.uniform(-20, 30)
        
        luminosity = max(0, base + variation)
        
        return round(luminosity, 0)
    
    def calculate_heat_index(self, temp: float, humidity: float) -> float:
        """
        Calcula índice de calor (sensação térmica)
        
        Args:
            temp: Temperatura em °C
            humidity: Umidade relativa em %
        
        Returns:
            float: Índice de calor em °C
        """
        # Fórmula simplificada de índice de calor
        hi = temp + 0.5555 * ((6.11 * pow(10, (7.5 * temp / (237.7 + temp))) * (humidity / 100)) - 10)
        return round(hi, 1)
    
    def get_rain_probability(self, pressure: float, humidity: float) -> float:
        """
        Estima probabilidade de chuva baseada em pressão e umidade
        
        Args:
            pressure: Pressão atmosférica em hPa
            humidity: Umidade relativa em %
        
        Returns:
            float: Probabilidade de chuva em % (0-100)
        """
        # Modelo simplificado
        pressure_factor = max(0, (1013.25 - pressure) / 20)
        humidity_factor = max(0, (humidity - 60) / 40)
        
        probability = min(100, (pressure_factor + humidity_factor) * 50)
        
        return round(probability, 1)
    
    def read_all(self) -> Dict[str, any]:
        """
        Realiza leitura completa de todos os parâmetros
        
        Returns:
            dict: Dicionário com todas as leituras e metadados
        """
        if not self.is_active:
            raise RuntimeError(f"Sensor {self.sensor_id} não está ativo")
        
        temp = self.read_temperature()
        humidity = self.read_humidity()
        pressure = self.read_pressure()
        wind = self.read_wind()
        luminosity = self.read_luminosity()
        
        reading = {
            'sensor_id': self.sensor_id,
            'timestamp': datetime.now().isoformat(),
            'location': self.location,
            'altitude': self.altitude,
            'temperature': temp,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind['speed'],
            'wind_direction': wind['direction'],
            'luminosity': luminosity,
            'heat_index': self.calculate_heat_index(temp, humidity),
            'rain_probability': self.get_rain_probability(pressure, humidity)
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
            'altitude': self.altitude,
            'last_reading': self.last_reading
        }
    
    def get_wind_direction_name(self, degrees: float) -> str:
        """
        Converte graus em nome da direção do vento
        
        Args:
            degrees: Direção em graus (0-360)
        
        Returns:
            str: Nome da direção (N, NE, E, SE, S, SW, W, NW)
        """
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = round(degrees / 45) % 8
        return directions[index]
    
    def __repr__(self):
        status = "ATIVO" if self.is_active else "INATIVO"
        return f"WeatherSensor(id={self.sensor_id}, status={status}, location={self.location})"


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste da Estação Meteorológica ===\n")
    
    # Criar sensor
    sensor = WeatherSensor(
        sensor_id="WEATHER_001",
        location=(-25.4284, -49.2733),  # Curitiba, PR
        altitude=934.6
    )
    
    # Ativar sensor
    sensor.start()
    
    # Realizar 3 leituras
    print("\n📊 Realizando leituras...\n")
    for i in range(3):
        reading = sensor.read_all()
        print(f"Leitura {i+1}:")
        print(f"  🌡️ Temperatura: {reading['temperature']}°C")
        print(f"  💧 Umidade: {reading['humidity']}%")
        print(f"  📊 Pressão: {reading['pressure']} hPa")
        print(f"  💨 Vento: {reading['wind_speed']} km/h ({sensor.get_wind_direction_name(reading['wind_direction'])})")
        print(f"  ☀️ Luminosidade: {reading['luminosity']} lux")
        print(f"  🌡️ Sensação Térmica: {reading['heat_index']}°C")
        print(f"  🌧️ Prob. Chuva: {reading['rain_probability']}%")
        print()
        time.sleep(2)
    
    # Status do sensor
    print("Status:", sensor.get_status())
    
    # Desativar
    sensor.stop()