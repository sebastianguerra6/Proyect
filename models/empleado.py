from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class Empleado:
    """Clase modelo para representar un empleado o proceso"""
    
    def __init__(self, sid: str, nueva_sub_unidad: str, nuevo_cargo: str,
                 ingreso_por: str = "", request_date: Optional[str] = None, 
                 fecha: Optional[str] = None, status: str = "Pendiente",
                 tipo_proceso: str = "", nombre: str = "", apellido: str = "", 
                 email: str = "", telefono: str = "", departamento: str = "",
                 cargo: str = "", fecha_contratacion: str = "", salario: str = "",
                 estado: str = "Activo"):
        
        # Campos para procesos
        self.sid = sid
        self.nueva_sub_unidad = nueva_sub_unidad
        self.nuevo_cargo = nuevo_cargo
        self.ingreso_por = ingreso_por
        self.request_date = request_date or datetime.now().strftime("%Y-%m-%d")
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.tipo_proceso = tipo_proceso
        self.status = status
        
        # Campos para headcount
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.departamento = departamento
        self.cargo = cargo
        self.fecha_contratacion = fecha_contratacion
        self.salario = salario
        self.estado = estado
        
        # Campos comunes
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
            "tipo_proceso": self.tipo_proceso,
            "sid": self.sid,
            "nueva_sub_unidad": self.nueva_sub_unidad,
            "nuevo_cargo": self.nuevo_cargo,
            "ingreso_por": self.ingreso_por,
            "request_date": self.request_date,
            "fecha": self.fecha,
            "status": self.status,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "departamento": self.departamento,
            "cargo": self.cargo,
            "fecha_contratacion": self.fecha_contratacion,
            "salario": self.salario,
            "estado": self.estado,
            "fecha_registro": self.fecha_registro,
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
            status=data.get("status", "Pendiente"),
            tipo_proceso=data.get("tipo_proceso", ""),
            nombre=data.get("nombre", ""),
            apellido=data.get("apellido", ""),
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            departamento=data.get("departamento", ""),
            cargo=data.get("cargo", ""),
            fecha_contratacion=data.get("fecha_contratacion", ""),
            salario=data.get("salario", ""),
            estado=data.get("estado", "Activo")
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
