"""
Data Generator Module
Gera dados simulados para testes e demonstração do sistema
Cria datasets realistas de sensores, clima e operações agrícolas
"""

import random
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np


class DataGenerator:
    """
    Classe para gerar dados simulados de agricultura de precisão
    """
    
    @staticmethod
    def generate_soil_data(num_samples: int = 100, hours: int = 24) -> pd.DataFrame:
        """
        Gera dados históricos de sensores de solo
        
        Args:
            num_samples: Número de amostras
            hours: Período em horas
        
        Returns:
            DataFrame: Dados de solo
        """
        now = datetime.now()
        timestamps = [now - timedelta(hours=hours * i / num_samples) for i in range(num_samples)]
        timestamps.reverse()
        
        # Gera variação natural ao longo do tempo
        base_moisture = 50.0
        base_temp = 22.0
        
        data = {
            'timestamp': timestamps,
            'moisture': [
                max(20, min(80, base_moisture + np.sin(i/10) * 10 + random.uniform(-3, 3)))
                for i in range(num_samples)
            ],
            'temperature': [
                max(15, min(35, base_temp + np.sin(i/8) * 5 + random.uniform(-2, 2)))
                for i in range(num_samples)
            ],
            'ph': [
                max(5.0, min(8.0, 6.5 + random.uniform(-0.3, 0.3)))
                for i in range(num_samples)
            ],
            'nitrogen': [
                max(10, min(60, 30 + random.uniform(-5, 5)))
                for i in range(num_samples)
            ],
            'phosphorus': [
                max(5, min(40, 15 + random.uniform(-3, 3)))
                for i in range(num_samples)
            ],
            'potassium': [
                max(15, min(80, 40 + random.uniform(-8, 8)))
                for i in range(num_samples)
            ]
        }
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    @staticmethod
    def generate_weather_data(num_samples: int = 100, hours: int = 24) -> pd.DataFrame:
        """
        Gera dados meteorológicos históricos
        
        Args:
            num_samples: Número de amostras
            hours: Período em horas
        
        Returns:
            DataFrame: Dados meteorológicos
        """
        now = datetime.now()
        timestamps = [now - timedelta(hours=hours * i / num_samples) for i in range(num_samples)]
        timestamps.reverse()
        
        data = {
            'timestamp': timestamps,
            'temperature': [
                max(15, min(38, 25 + np.sin(i/12) * 8 + random.uniform(-2, 2)))
                for i in range(num_samples)
            ],
            'humidity': [
                max(30, min(95, 60 + np.cos(i/10) * 15 + random.uniform(-5, 5)))
                for i in range(num_samples)
            ],
            'pressure': [
                max(980, min(1040, 1013 + random.uniform(-5, 5)))
                for i in range(num_samples)
            ],
            'wind_speed': [
                max(0, min(30, 8 + random.uniform(-3, 7)))
                for i in range(num_samples)
            ],
            'wind_direction': [
                random.uniform(0, 360)
                for i in range(num_samples)
            ],
            'luminosity': [
                max(0, 800 if 6 <= (timestamps[i].hour) <= 18 else 10) + random.uniform(-100, 100)
                for i in range(num_samples)
            ],
            'rain_probability': [
                max(0, min(100, 30 + random.uniform(-20, 30)))
                for i in range(num_samples)
            ]
        }
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    @staticmethod
    def generate_gps_track(num_points: int = 50, 
                          start_lat: float = -25.4284, 
                          start_lon: float = -49.2733) -> pd.DataFrame:
        """
        Gera trilha GPS simulada
        
        Args:
            num_points: Número de pontos
            start_lat: Latitude inicial
            start_lon: Longitude inicial
        
        Returns:
            DataFrame: Trilha GPS
        """
        now = datetime.now()
        
        lat = start_lat
        lon = start_lon
        
        data = {
            'timestamp': [],
            'latitude': [],
            'longitude': [],
            'altitude': [],
            'speed': [],
            'heading': []
        }
        
        for i in range(num_points):
            data['timestamp'].append(now + timedelta(seconds=i * 5))
            data['latitude'].append(lat)
            data['longitude'].append(lon)
            data['altitude'].append(934 + random.uniform(-0.5, 0.5))
            data['speed'].append(max(0, 15 + random.uniform(-3, 3)))
            data['heading'].append(random.uniform(0, 360))
            
            # Simula movimento
            lat += random.uniform(-0.0001, 0.0001)
            lon += random.uniform(-0.0001, 0.0001)
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    @staticmethod
    def generate_irrigation_log(num_events: int = 20, days: int = 30) -> pd.DataFrame:
        """
        Gera histórico de irrigação
        
        Args:
            num_events: Número de eventos
            days: Período em dias
        
        Returns:
            DataFrame: Log de irrigação
        """
        now = datetime.now()
        
        data = {
            'timestamp': [
                now - timedelta(days=random.uniform(0, days))
                for _ in range(num_events)
            ],
            'zone': [random.randint(1, 4) for _ in range(num_events)],
            'duration_minutes': [random.uniform(10, 45) for _ in range(num_events)],
            'flow_rate_lmin': [random.uniform(30, 80) for _ in range(num_events)],
            'volume_liters': []
        }
        
        # Calcula volume
        for i in range(num_events):
            volume = data['duration_minutes'][i] * data['flow_rate_lmin'][i]
            data['volume_liters'].append(round(volume, 1))
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    @staticmethod
    def generate_fertilizer_log(num_applications: int = 10, days: int = 60) -> pd.DataFrame:
        """
        Gera histórico de fertilização
        
        Args:
            num_applications: Número de aplicações
            days: Período em dias
        
        Returns:
            DataFrame: Log de fertilização
        """
        now = datetime.now()
        
        fertilizer_types = [
            'NPK 20-10-10',
            'NPK 10-20-20',
            'NPK 15-15-15',
            'Uréia 45-00-00'
        ]
        
        data = {
            'timestamp': [
                now - timedelta(days=random.uniform(0, days))
                for _ in range(num_applications)
            ],
            'fertilizer_type': [
                random.choice(fertilizer_types)
                for _ in range(num_applications)
            ],
            'area_hectares': [
                random.uniform(1.0, 10.0)
                for _ in range(num_applications)
            ],
            'rate_kg_ha': [
                random.uniform(50, 150)
                for _ in range(num_applications)
            ],
            'total_kg': []
        }
        
        # Calcula total
        for i in range(num_applications):
            total = data['area_hectares'][i] * data['rate_kg_ha'][i]
            data['total_kg'].append(round(total, 1))
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    @staticmethod
    def generate_productivity_map(grid_size: int = 20) -> pd.DataFrame:
        """
        Gera mapa de produtividade simulado
        
        Args:
            grid_size: Tamanho da grade (grid_size x grid_size)
        
        Returns:
            DataFrame: Mapa de produtividade
        """
        data = {
            'x': [],
            'y': [],
            'productivity': []
        }
        
        for i in range(grid_size):
            for j in range(grid_size):
                data['x'].append(i)
                data['y'].append(j)
                
                # Cria padrão de produtividade com variação
                base = 60
                pattern = np.sin(i/3) * np.cos(j/3) * 15
                noise = random.uniform(-5, 5)
                
                productivity = max(30, min(90, base + pattern + noise))
                data['productivity'].append(round(productivity, 1))
        
        df = pd.DataFrame(data)
        
        return df
    
    @staticmethod
    def generate_zone_analysis(num_zones: int = 5) -> pd.DataFrame:
        """
        Gera análise por zona de manejo
        
        Args:
            num_zones: Número de zonas
        
        Returns:
            DataFrame: Análise por zona
        """
        data = {
            'zone_id': list(range(1, num_zones + 1)),
            'area_hectares': [random.uniform(5, 20) for _ in range(num_zones)],
            'avg_productivity': [random.uniform(45, 85) for _ in range(num_zones)],
            'soil_type': [random.choice(['Argiloso', 'Arenoso', 'Médio']) for _ in range(num_zones)],
            'avg_moisture': [random.uniform(40, 70) for _ in range(num_zones)],
            'avg_nitrogen': [random.uniform(20, 45) for _ in range(num_zones)],
            'recommendation': []
        }
        
        # Gera recomendações baseadas nos dados
        for i in range(num_zones):
            if data['avg_productivity'][i] < 60:
                rec = "Aumentar fertilização"
            elif data['avg_moisture'][i] < 50:
                rec = "Aumentar irrigação"
            else:
                rec = "Manter manejo atual"
            
            data['recommendation'].append(rec)
        
        df = pd.DataFrame(data)
        
        return df
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, filename: str, directory: str = "data"):
        """
        Salva DataFrame em CSV
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo
            directory: Diretório de destino
        """
        import os
        
        # Cria diretório se não existe
        os.makedirs(directory, exist_ok=True)
        
        filepath = os.path.join(directory, filename)
        df.to_csv(filepath, index=False)
        
        print(f"✅ Dados salvos em: {filepath}")


# Exemplo de uso
if __name__ == "__main__":
    print("=== Gerador de Dados ===\n")
    
    # Gerar dados de solo
    print("📊 Gerando dados de solo...")
    soil_df = DataGenerator.generate_soil_data(num_samples=200, hours=48)
    print(f"   {len(soil_df)} amostras geradas")
    print(soil_df.head())
    
    # Gerar dados meteorológicos
    print("\n🌤️ Gerando dados meteorológicos...")
    weather_df = DataGenerator.generate_weather_data(num_samples=200, hours=48)
    print(f"   {len(weather_df)} amostras geradas")
    
    # Gerar trilha GPS
    print("\n📍 Gerando trilha GPS...")
    gps_df = DataGenerator.generate_gps_track(num_points=100)
    print(f"   {len(gps_df)} pontos gerados")
    
    # Gerar log de irrigação
    print("\n💧 Gerando log de irrigação...")
    irrigation_df = DataGenerator.generate_irrigation_log(num_events=30)
    print(f"   {len(irrigation_df)} eventos gerados")
    
    # Gerar mapa de produtividade
    print("\n🗺️ Gerando mapa de produtividade...")
    productivity_df = DataGenerator.generate_productivity_map(grid_size=15)
    print(f"   {len(productivity_df)} células geradas")
    
    # Salvar em CSV (opcional)
    # DataGenerator.save_to_csv(soil_df, "soil_data.csv")
    
    print("\n✅ Geração de dados concluída!")