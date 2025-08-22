from datetime import datetime
from typing import Optional, Dict, Any

class Empleado:
    """Clase modelo para representar un empleado"""
    
    def __init__(self, sid: str, area: str, 
                 ingreso_por: str = "", subarea: str = "", fecha: Optional[str] = None):
        self.sid = sid
        self.area = area
        self.ingreso_por = ingreso_por
        self.subarea = subarea
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el empleado a un diccionario"""
        return {
            "sid": self.sid,
            "area": self.area,
            "ingreso_por": self.ingreso_por,
            "subarea": self.subarea,
            "fecha": self.fecha,
            "fecha_registro": self.fecha_registro
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Empleado':
        """Crea un empleado desde un diccionario"""
        return cls(
            sid=data.get("sid", ""),
            area=data.get("area", ""),
            ingreso_por=data.get("ingreso_por", ""),
            subarea=data.get("subarea", ""),
            fecha=data.get("fecha", "")
        )
