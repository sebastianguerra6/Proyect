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
    
    def __init__(self, empleado: Empleado, fecha_ingreso: str = "", 
                 departamento_destino: str = "", supervisor: str = "",
                 salario: str = "", tipo_contrato: str = "", 
                 observaciones: str = ""):
        super().__init__(empleado, "onboarding")
        self.fecha_ingreso = fecha_ingreso or datetime.now().strftime("%Y-%m-%d")
        self.departamento_destino = departamento_destino
        self.supervisor = supervisor
        self.salario = salario
        self.tipo_contrato = tipo_contrato
        self.observaciones = observaciones
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el onboarding a un diccionario"""
        datos = super().to_dict()
        datos.update({
            "fecha_ingreso": self.fecha_ingreso,
            "departamento_destino": self.departamento_destino,
            "supervisor": self.supervisor,
            "salario": self.salario,
            "tipo_contrato": self.tipo_contrato,
            "observaciones": self.observaciones
        })
        return datos
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Onboarding':
        """Crea un onboarding desde un diccionario"""
        empleado = Empleado.from_dict(data)
        return cls(
            empleado=empleado,
            fecha_ingreso=data.get("fecha_ingreso", ""),
            departamento_destino=data.get("departamento_destino", ""),
            supervisor=data.get("supervisor", ""),
            salario=data.get("salario", ""),
            tipo_contrato=data.get("tipo_contrato", ""),
            observaciones=data.get("observaciones", "")
        )

class Offboarding(ProcesoBase):
    """Clase para procesos de offboarding"""
    
    def __init__(self, empleado: Empleado, fecha_salida: str = "",
                 motivo_salida: str = "", tipo_salida: str = "",
                 entrevista_salida: str = "", equipos_devueltos: str = "",
                 observaciones: str = ""):
        super().__init__(empleado, "offboarding")
        self.fecha_salida = fecha_salida or datetime.now().strftime("%Y-%m-%d")
        self.motivo_salida = motivo_salida
        self.tipo_salida = tipo_salida
        self.entrevista_salida = entrevista_salida
        self.equipos_devueltos = equipos_devueltos
        self.observaciones = observaciones
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el offboarding a un diccionario"""
        datos = super().to_dict()
        datos.update({
            "fecha_salida": self.fecha_salida,
            "motivo_salida": self.motivo_salida,
            "tipo_salida": self.tipo_salida,
            "entrevista_salida": self.entrevista_salida,
            "equipos_devueltos": self.equipos_devueltos,
            "observaciones": self.observaciones
        })
        return datos
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Offboarding':
        """Crea un offboarding desde un diccionario"""
        empleado = Empleado.from_dict(data)
        return cls(
            empleado=empleado,
            fecha_salida=data.get("fecha_salida", ""),
            motivo_salida=data.get("motivo_salida", ""),
            tipo_salida=data.get("tipo_salida", ""),
            entrevista_salida=data.get("entrevista_salida", ""),
            equipos_devueltos=data.get("equipos_devueltos", ""),
            observaciones=data.get("observaciones", "")
        )

class LateralMovement(ProcesoBase):
    """Clase para procesos de lateral movement"""
    
    def __init__(self, empleado: Empleado, fecha_movimiento: str = "",
                 departamento_origen: str = "", departamento_destino: str = "",
                 cargo_anterior: str = "", cargo_nuevo: str = "",
                 motivo_movimiento: str = "", observaciones: str = ""):
        super().__init__(empleado, "lateral")
        self.fecha_movimiento = fecha_movimiento or datetime.now().strftime("%Y-%m-%d")
        self.departamento_origen = departamento_origen
        self.departamento_destino = departamento_destino
        self.cargo_anterior = cargo_anterior
        self.cargo_nuevo = cargo_nuevo
        self.motivo_movimiento = motivo_movimiento
        self.observaciones = observaciones
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el lateral movement a un diccionario"""
        datos = super().to_dict()
        datos.update({
            "fecha_movimiento": self.fecha_movimiento,
            "departamento_origen": self.departamento_origen,
            "departamento_destino": self.departamento_destino,
            "cargo_anterior": self.cargo_anterior,
            "cargo_nuevo": self.cargo_nuevo,
            "motivo_movimiento": self.motivo_movimiento,
            "observaciones": self.observaciones
        })
        return datos
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LateralMovement':
        """Crea un lateral movement desde un diccionario"""
        empleado = Empleado.from_dict(data)
        return cls(
            empleado=empleado,
            fecha_movimiento=data.get("fecha_movimiento", ""),
            departamento_origen=data.get("departamento_origen", ""),
            departamento_destino=data.get("departamento_destino", ""),
            cargo_anterior=data.get("cargo_anterior", ""),
            cargo_nuevo=data.get("cargo_nuevo", ""),
            motivo_movimiento=data.get("motivo_movimiento", ""),
            observaciones=data.get("observaciones", "")
        )
