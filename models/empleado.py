from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class Empleado:
    """Clase modelo para representar un empleado"""
    
    def __init__(self, sid: str, nueva_sub_unidad: str, nuevo_cargo: str,
                 ingreso_por: str = "", request_date: Optional[str] = None, 
                 fecha: Optional[str] = None, status: str = "Pendiente"):
        self.sid = sid
        self.nueva_sub_unidad = nueva_sub_unidad
        self.nuevo_cargo = nuevo_cargo
        self.ingreso_por = ingreso_por
        self.request_date = request_date or datetime.now().strftime("%Y-%m-%d")
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status
        
        # Generar número de caso único
        self.numero_caso = self._generar_numero_caso()
        
        # Campos adicionales para edición (inicialmente null)
        self.mail = None
        self.closing_date_app = None
        self.app_quality = None
        self.confirmation_by_user = None
        self.comment = None
    
    def _generar_numero_caso(self) -> str:
        """Genera un número de caso único basado en timestamp y SID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"CASE-{timestamp}-{short_uuid}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el empleado a un diccionario"""
        return {
            "numero_caso": self.numero_caso,
            "sid": self.sid,
            "nueva_sub_unidad": self.nueva_sub_unidad,
            "nuevo_cargo": self.nuevo_cargo,
            "ingreso_por": self.ingreso_por,
            "request_date": self.request_date,
            "fecha": self.fecha,
            "fecha_registro": self.fecha_registro,
            "status": self.status,
            "mail": self.mail,
            "closing_date_app": self.closing_date_app,
            "app_quality": self.app_quality,
            "confirmation_by_user": self.confirmation_by_user,
            "comment": self.comment
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Empleado':
        """Crea un empleado desde un diccionario"""
        empleado = cls(
            sid=data.get("sid", ""),
            nueva_sub_unidad=data.get("nueva_sub_unidad", ""),
            nuevo_cargo=data.get("nuevo_cargo", ""),
            ingreso_por=data.get("ingreso_por", ""),
            request_date=data.get("request_date", ""),
            fecha=data.get("fecha", ""),
            status=data.get("status", "Pendiente")
        )
        
        # Asignar número de caso si existe, sino generar uno nuevo
        if data.get("numero_caso"):
            empleado.numero_caso = data.get("numero_caso")
        
        # Asignar campos adicionales
        empleado.mail = data.get("mail")
        empleado.closing_date_app = data.get("closing_date_app")
        empleado.app_quality = data.get("app_quality")
        empleado.confirmation_by_user = data.get("confirmation_by_user")
        empleado.comment = data.get("comment")
        
        return empleado

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
