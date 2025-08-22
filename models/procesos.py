from datetime import datetime
from typing import Optional, Dict, Any
from .empleado import Empleado

class ProcesoBase:
    """Clase base para todos los procesos de empleados"""
    
    def __init__(self, empleado: Empleado, tipo_proceso: str):
        self.empleado = empleado
        self.tipo_proceso = tipo_proceso
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el proceso a un diccionario"""
        datos = self.empleado.to_dict()
        datos["tipo_proceso"] = self.tipo_proceso
        return datos

class Onboarding(ProcesoBase):
    """Clase para procesos de onboarding"""
    
    def __init__(self, empleado: Empleado, submenu_onboarding: str = ""):
        super().__init__(empleado, "onboarding")
        self.submenu_onboarding = submenu_onboarding
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el onboarding a un diccionario"""
        datos = super().to_dict()
        datos.update({
            "submenu_onboarding": self.submenu_onboarding
        })
        return datos
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Onboarding':
        """Crea un onboarding desde un diccionario"""
        empleado = Empleado.from_dict(data)
        return cls(
            empleado=empleado,
            submenu_onboarding=data.get("submenu_onboarding", "")
        )

class Offboarding(ProcesoBase):
    """Clase para procesos de offboarding"""
    
    def __init__(self, empleado: Empleado, submenu_offboarding: str = ""):
        super().__init__(empleado, "offboarding")
        self.submenu_offboarding = submenu_offboarding
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el offboarding a un diccionario"""
        datos = super().to_dict()
        datos.update({
            "submenu_offboarding": self.submenu_offboarding
        })
        return datos
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Offboarding':
        """Crea un offboarding desde un diccionario"""
        empleado = Empleado.from_dict(data)
        return cls(
            empleado=empleado,
            submenu_offboarding=data.get("submenu_offboarding", "")
        )

class LateralMovement(ProcesoBase):
    """Clase para procesos de lateral movement"""
    
    def __init__(self, empleado: Empleado, empleo_anterior: str = "", submenu_lateral: str = ""):
        super().__init__(empleado, "lateral")
        self.empleo_anterior = empleo_anterior
        self.submenu_lateral = submenu_lateral
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el lateral movement a un diccionario"""
        datos = super().to_dict()
        datos.update({
            "empleo_anterior": self.empleo_anterior,
            "submenu_lateral": self.submenu_lateral
        })
        return datos
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LateralMovement':
        """Crea un lateral movement desde un diccionario"""
        empleado = Empleado.from_dict(data)
        return cls(
            empleado=empleado,
            empleo_anterior=data.get("empleo_anterior", ""),
            submenu_lateral=data.get("submenu_lateral", "")
        )
