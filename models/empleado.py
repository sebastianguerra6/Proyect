from datetime import datetime
from typing import Optional, Dict, Any

class Empleado:
    """Clase modelo para representar un empleado"""
    
    def __init__(self, id_empleado: str, area: str, empleo: str, 
                 ingreso_por: str = "", fecha: Optional[str] = None):
        self.id_empleado = id_empleado
        self.area = area
        self.empleo = empleo
        self.ingreso_por = ingreso_por
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el empleado a un diccionario"""
        return {
            "id": self.id_empleado,
            "area": self.area,
            "empleo": self.empleo,
            "ingreso_por": self.ingreso_por,
            "fecha": self.fecha,
            "fecha_registro": self.fecha_registro
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Empleado':
        """Crea un empleado desde un diccionario"""
        return cls(
            id_empleado=data.get("id", ""),
            area=data.get("area", ""),
            empleo=data.get("empleo", ""),
            ingreso_por=data.get("ingreso_por", ""),
            fecha=data.get("fecha", "")
        )
