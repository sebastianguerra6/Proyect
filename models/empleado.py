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

class PersonaHeadcount:
    """Clase modelo para representar una persona en el headcount"""
    
    def __init__(self, nombre: str, apellido: str, email: str, departamento: str, cargo: str,
                 telefono: str = "", fecha_contratacion: str = "", salario: str = "", estado: str = "Activo"):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.departamento = departamento
        self.cargo = cargo
        self.telefono = telefono
        self.fecha_contratacion = fecha_contratacion
        self.salario = salario
        self.estado = estado
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = f"{nombre.lower()}_{apellido.lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la persona a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "departamento": self.departamento,
            "cargo": self.cargo,
            "telefono": self.telefono,
            "fecha_contratacion": self.fecha_contratacion,
            "salario": self.salario,
            "estado": self.estado,
            "fecha_registro": self.fecha_registro
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PersonaHeadcount':
        """Crea una persona desde un diccionario"""
        return cls(
            nombre=data.get("nombre", ""),
            apellido=data.get("apellido", ""),
            email=data.get("email", ""),
            departamento=data.get("departamento", ""),
            cargo=data.get("cargo", ""),
            telefono=data.get("telefono", ""),
            fecha_contratacion=data.get("fecha_contratacion", ""),
            salario=data.get("salario", ""),
            estado=data.get("estado", "Activo")
        )
