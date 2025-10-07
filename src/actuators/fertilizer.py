"""
Fertilizer System Module
Sistema de controle de fertilização automatizado para agricultura de precisão
Controla: aplicação de NPK, taxa de aplicação, dosagem
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from enum import Enum


class FertilizerType(Enum):
    """Tipos de fertilizantes NPK"""
    NPK_20_10_10 = "NPK 20-10-10"  # Alto em Nitrogênio
    NPK_10_20_20 = "NPK 10-20-20"  # Médio N, alto P e K
    NPK_15_15_15 = "NPK 15-15-15"  # Balanceado
    NPK_04_14_08 = "NPK 04-14-08"  # Baixo N, alto P
    UREA = "Uréia 45-00-00"  # Nitrogênio puro


class ApplicationMode(Enum):
    """Modos de aplicação"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    VARIABLE_RATE = "variable_rate"  # Taxa variável
    OFF = "off"


class FertilizerSystem:
    """
    Classe que simula um sistema de fertilização embarcado
    
    Atributos:
        system_id (str): Identificador único do sistema
        tank_capacity (float): Capacidade do tanque em kg
        max_rate (float): Taxa máxima de aplicação em kg/ha
    """
    
    def __init__(self, system_id: str, tank_capacity: float = 500.0, max_rate: float = 200.0):
        """
        Inicializa o sistema de fertilização
        
        Args:
            system_id: ID único do sistema
            tank_capacity: Capacidade do tanque em kg
            max_rate: Taxa máxima de aplicação em kg/ha
        """
        self.system_id = system_id
        self.tank_capacity = tank_capacity
        self.max_rate = max_rate
        
        # Estado do sistema
        self.is_active = False
        self.mode = ApplicationMode.OFF
        self.current_fertilizer = None
        self.tank_level = tank_capacity  # kg
        self.application_rate = 0.0  # kg/ha
        
        # Estatísticas
        self.total_applied = 0.0  # kg
        self.area_covered = 0.0  # hectares
        self.last_application = None
        self.applications_count = 0
        
        # Configurações
        self.target_npk = {'N': 30.0, 'P': 15.0, 'K': 40.0}  # mg/kg
        
        print(f"✅ Sistema de Fertilização {self.system_id} inicializado")
        print(f"   Capacidade do tanque: {self.tank_capacity} kg")
        print(f"   Taxa máxima: {self.max_rate} kg/ha")
    
    def start(self, mode: ApplicationMode = ApplicationMode.MANUAL):
        """
        Ativa o sistema de fertilização
        
        Args:
            mode: Modo de operação
        """
        self.is_active = True
        self.mode = mode
        print(f"🟢 Sistema {self.system_id} ATIVADO - Modo: {mode.value}")
    
    def stop(self):
        """Desativa o sistema de fertilização"""
        self.is_active = False
        self.mode = ApplicationMode.OFF
        self.application_rate = 0.0
        print(f"🔴 Sistema {self.system_id} DESATIVADO")
    
    def load_fertilizer(self, fertilizer_type: FertilizerType, amount: float) -> bool:
        """
        Carrega fertilizante no tanque
        
        Args:
            fertilizer_type: Tipo de fertilizante
            amount: Quantidade em kg
        
        Returns:
            bool: True se sucesso
        """
        if self.is_active:
            print(f"⚠️ Não é possível carregar com o sistema ativo!")
            return False
        
        if amount > self.tank_capacity:
            print(f"⚠️ Quantidade excede capacidade do tanque!")
            return False
        
        self.current_fertilizer = fertilizer_type
        self.tank_level = amount
        
        print(f"✅ Tanque carregado com {amount} kg de {fertilizer_type.value}")
        
        return True
    
    def set_application_rate(self, rate: float) -> bool:
        """
        Define taxa de aplicação
        
        Args:
            rate: Taxa em kg/ha
        
        Returns:
            bool: True se sucesso
        """
        if not self.is_active:
            print(f"⚠️ Sistema não está ativo!")
            return False
        
        if rate < 0 or rate > self.max_rate:
            print(f"⚠️ Taxa deve estar entre 0 e {self.max_rate} kg/ha")
            return False
        
        if self.current_fertilizer is None:
            print(f"⚠️ Nenhum fertilizante carregado!")
            return False
        
        self.application_rate = rate
        print(f"🌱 Taxa de aplicação ajustada para {rate} kg/ha")
        
        return True
    
    def apply(self, area: float) -> Dict[str, float]:
        """
        Aplica fertilizante em uma área
        
        Args:
            area: Área em hectares
        
        Returns:
            dict: Informações da aplicação
        """
        if not self.is_active:
            raise RuntimeError(f"Sistema {self.system_id} não está ativo")
        
        if self.current_fertilizer is None:
            raise RuntimeError("Nenhum fertilizante carregado")
        
        if self.application_rate == 0:
            raise RuntimeError("Taxa de aplicação não definida")
        
        # Calcula quantidade necessária
        required_amount = self.application_rate * area
        
        if required_amount > self.tank_level:
            print(f"⚠️ Fertilizante insuficiente! Necessário: {required_amount:.1f} kg, Disponível: {self.tank_level:.1f} kg")
            required_amount = self.tank_level
            area = self.tank_level / self.application_rate
        
        # Aplica
        self.tank_level -= required_amount
        self.total_applied += required_amount
        self.area_covered += area
        self.applications_count += 1
        self.last_application = datetime.now()
        
        # Calcula composição NPK aplicada
        npk_composition = self._get_npk_composition(self.current_fertilizer)
        applied_npk = {
            'N': (required_amount * npk_composition['N']) / 100,
            'P': (required_amount * npk_composition['P']) / 100,
            'K': (required_amount * npk_composition['K']) / 100
        }
        
        result = {
            'area_hectares': round(area, 2),
            'amount_applied_kg': round(required_amount, 2),
            'fertilizer_type': self.current_fertilizer.value,
            'application_rate': self.application_rate,
            'tank_remaining_kg': round(self.tank_level, 2),
            'npk_applied': {k: round(v, 2) for k, v in applied_npk.items()}
        }
        
        print(f"✅ Aplicação concluída!")
        print(f"   Área: {result['area_hectares']} ha")
        print(f"   Quantidade: {result['amount_applied_kg']} kg")
        print(f"   NPK aplicado: N={result['npk_applied']['N']} P={result['npk_applied']['P']} K={result['npk_applied']['K']} kg")
        
        return result
    
    def _get_npk_composition(self, fertilizer_type: FertilizerType) -> Dict[str, float]:
        """
        Retorna composição NPK do fertilizante
        
        Args:
            fertilizer_type: Tipo de fertilizante
        
        Returns:
            dict: Porcentagens de N, P, K
        """
        compositions = {
            FertilizerType.NPK_20_10_10: {'N': 20.0, 'P': 10.0, 'K': 10.0},
            FertilizerType.NPK_10_20_20: {'N': 10.0, 'P': 20.0, 'K': 20.0},
            FertilizerType.NPK_15_15_15: {'N': 15.0, 'P': 15.0, 'K': 15.0},
            FertilizerType.NPK_04_14_08: {'N': 4.0, 'P': 14.0, 'K': 8.0},
            FertilizerType.UREA: {'N': 45.0, 'P': 0.0, 'K': 0.0}
        }
        
        return compositions.get(fertilizer_type, {'N': 0.0, 'P': 0.0, 'K': 0.0})
    
    def recommend_fertilizer(self, current_npk: Dict[str, float]) -> Dict[str, any]:
        """
        Recomenda fertilizante baseado nos níveis atuais de NPK do solo
        
        Args:
            current_npk: Níveis atuais {'N': float, 'P': float, 'K': float}
        
        Returns:
            dict: Recomendação de fertilização
        """
        deficits = {
            'N': max(0, self.target_npk['N'] - current_npk.get('N', 0)),
            'P': max(0, self.target_npk['P'] - current_npk.get('P', 0)),
            'K': max(0, self.target_npk['K'] - current_npk.get('K', 0))
        }
        
        # Lógica simplificada de recomendação
        if deficits['N'] > 10:
            recommended = FertilizerType.NPK_20_10_10
            reason = "Alto déficit de Nitrogênio"
        elif deficits['P'] > 10:
            recommended = FertilizerType.NPK_04_14_08
            reason = "Alto déficit de Fósforo"
        elif deficits['K'] > 10:
            recommended = FertilizerType.NPK_10_20_20
            reason = "Alto déficit de Potássio"
        elif sum(deficits.values()) > 15:
            recommended = FertilizerType.NPK_15_15_15
            reason = "Déficit balanceado"
        else:
            recommended = None
            reason = "Níveis adequados"
        
        # Calcula taxa recomendada
        if recommended:
            # Fórmula simplificada: deficit médio * fator de conversão
            avg_deficit = sum(deficits.values()) / 3
            recommended_rate = min(self.max_rate, avg_deficit * 3)
        else:
            recommended_rate = 0
        
        return {
            'current_npk': current_npk,
            'target_npk': self.target_npk,
            'deficits': deficits,
            'recommended_fertilizer': recommended.value if recommended else "Nenhum",
            'recommended_rate_kg_ha': round(recommended_rate, 1),
            'reason': reason
        }
    
    def variable_rate_apply(self, zones: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Aplica fertilizante com taxa variável por zona
        
        Args:
            zones: Lista de dicts com {'area': float, 'npk': dict}
        
        Returns:
            list: Resultados por zona
        """
        if self.mode != ApplicationMode.VARIABLE_RATE:
            print(f"⚠️ Sistema não está em modo taxa variável!")
            return []
        
        results = []
        
        for i, zone in enumerate(zones, 1):
            print(f"\n📍 Processando Zona {i}...")
            
            # Recomenda fertilizante para esta zona
            recommendation = self.recommend_fertilizer(zone['npk'])
            
            if recommendation['recommended_fertilizer'] != "Nenhum":
                # Carrega fertilizante recomendado (simulação)
                recommended_type = FertilizerType[recommendation['recommended_fertilizer'].replace(' ', '_').replace('-', '_')]
                
                # Ajusta taxa
                self.set_application_rate(recommendation['recommended_rate_kg_ha'])
                
                # Aplica
                result = self.apply(zone['area'])
                result['zone'] = i
                result['recommendation'] = recommendation
                
                results.append(result)
        
        return results
    
    def get_status(self) -> Dict[str, any]:
        """
        Retorna status completo do sistema
        
        Returns:
            dict: Status do sistema
        """
        return {
            'system_id': self.system_id,
            'is_active': self.is_active,
            'mode': self.mode.value,
            'current_fertilizer': self.current_fertilizer.value if self.current_fertilizer else None,
            'tank_level_kg': round(self.tank_level, 2),
            'tank_capacity_kg': self.tank_capacity,
            'tank_level_percent': round((self.tank_level / self.tank_capacity) * 100, 1),
            'application_rate_kg_ha': self.application_rate,
            'total_applied_kg': round(self.total_applied, 2),
            'area_covered_ha': round(self.area_covered, 2),
            'applications_count': self.applications_count,
            'last_application': self.last_application.isoformat() if self.last_application else None
        }
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas de uso
        
        Returns:
            dict: Estatísticas
        """
        avg_rate = self.total_applied / max(self.area_covered, 1)
        
        return {
            'total_applied_kg': round(self.total_applied, 2),
            'total_applied_tons': round(self.total_applied / 1000, 3),
            'area_covered_hectares': round(self.area_covered, 2),
            'average_rate_kg_ha': round(avg_rate, 2),
            'applications_count': self.applications_count,
            'last_application': self.last_application
        }
    
    def __repr__(self):
        status = "ATIVO" if self.is_active else "INATIVO"
        fert = self.current_fertilizer.value if self.current_fertilizer else "Vazio"
        return f"FertilizerSystem(id={self.system_id}, status={status}, fertilizer={fert})"


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste do Sistema de Fertilização ===\n")
    
    # Criar sistema
    fertilizer = FertilizerSystem(
        system_id="FERT_001",
        tank_capacity=500.0,
        max_rate=200.0
    )
    
    # Carregar fertilizante
    fertilizer.load_fertilizer(FertilizerType.NPK_15_15_15, 300.0)
    
    # Ativar sistema
    fertilizer.start(ApplicationMode.MANUAL)
    
    # Definir taxa e aplicar
    fertilizer.set_application_rate(80.0)
    
    print("\n🌱 Aplicando fertilizante...")
    result = fertilizer.apply(area=2.5)
    
    # Teste de recomendação
    print("\n💡 Testando recomendação...")
    current_soil = {'N': 15.0, 'P': 8.0, 'K': 25.0}
    recommendation = fertilizer.recommend_fertilizer(current_soil)
    print(f"\nRecomendação:")
    print(f"  Fertilizante: {recommendation['recommended_fertilizer']}")
    print(f"  Taxa: {recommendation['recommended_rate_kg_ha']} kg/ha")
    print(f"  Motivo: {recommendation['reason']}")
    
    # Status
    print("\n📊 Status:")
    status = fertilizer.get_status()
    print(f"  Nível do tanque: {status['tank_level_kg']} kg ({status['tank_level_percent']}%)")
    print(f"  Total aplicado: {status['total_applied_kg']} kg")
    print(f"  Área coberta: {status['area_covered_ha']} ha")
    
    # Desativar
    fertilizer.stop()