from typing import List, Optional, Tuple
from models import Empleado, Onboarding, Offboarding, LateralMovement, PersonaHeadcount
from data import EmpleadoRepository
from tkinter import messagebox

class EmpleadoService:
    """Servicio para manejar la lógica de negocio de empleados"""
    
    def __init__(self, repository: EmpleadoRepository):
        self.repository = repository
    
    def validar_datos_generales(self, datos: dict) -> Tuple[bool, List[str]]:
        """Valida los datos generales del empleado"""
        errores = []
        
        # Validar campos obligatorios
        if not datos.get('sid', '').strip():
            errores.append("SID es obligatorio")
        
        if not datos.get('area', '').strip():
            errores.append("Área es obligatoria")
        
        return len(errores) == 0, errores
    
    def validar_datos_persona_headcount(self, datos: dict) -> Tuple[bool, List[str]]:
        """Valida los datos de una persona del headcount"""
        errores = []
        
        # Validar campos obligatorios
        if not datos.get('nombre', '').strip():
            errores.append("Nombre es obligatorio")
        
        if not datos.get('apellido', '').strip():
            errores.append("Apellido es obligatorio")
        
        if not datos.get('email', '').strip():
            errores.append("Email es obligatorio")
        
        if not datos.get('departamento', '').strip():
            errores.append("Departamento es obligatorio")
        
        if not datos.get('cargo', '').strip():
            errores.append("Cargo es obligatorio")
        
        return len(errores) == 0, errores
    
    def validar_tipo_proceso(self, tipo_proceso: str) -> Tuple[bool, str]:
        """Valida que se haya seleccionado un tipo de proceso"""
        tipos_validos = ['onboarding', 'offboarding', 'lateral']
        
        if not tipo_proceso:
            return False, "Debe seleccionar un tipo de proceso"
        
        if tipo_proceso not in tipos_validos:
            return False, f"Tipo de proceso '{tipo_proceso}' no es válido"
        
        return True, ""
    
    def crear_empleado(self, datos: dict) -> Optional[Empleado]:
        """Crea un objeto Empleado desde los datos del formulario"""
        try:
            return Empleado(
                sid=datos.get('sid', ''),
                area=datos.get('area', ''),
                ingreso_por=datos.get('ingreso_por', ''),
                subarea=datos.get('subarea', ''),
                fecha=datos.get('fecha', '')
            )
        except Exception as e:
            print(f"Error al crear empleado: {str(e)}")
            return None
    
    def crear_persona_headcount(self, datos: dict) -> Optional[PersonaHeadcount]:
        """Crea un objeto PersonaHeadcount desde los datos del formulario"""
        try:
            return PersonaHeadcount(
                nombre=datos.get('nombre', ''),
                apellido=datos.get('apellido', ''),
                email=datos.get('email', ''),
                departamento=datos.get('departamento', ''),
                cargo=datos.get('cargo', ''),
                telefono=datos.get('telefono', ''),
                fecha_contratacion=datos.get('fecha_contratacion', ''),
                salario=datos.get('salario', ''),
                estado=datos.get('estado', 'Activo')
            )
        except Exception as e:
            print(f"Error al crear persona del headcount: {str(e)}")
            return None
    
    def crear_onboarding(self, datos_generales: dict, datos_especificos: dict) -> Optional[Onboarding]:
        """Crea un proceso de onboarding"""
        try:
            empleado = self.crear_empleado(datos_generales)
            if not empleado:
                return None
            
            return Onboarding(
                empleado=empleado,
                submenu_onboarding=datos_especificos.get('submenu_onboarding', '')
            )
        except Exception as e:
            print(f"Error al crear onboarding: {str(e)}")
            return None
    
    def crear_offboarding(self, datos_generales: dict, datos_especificos: dict) -> Optional[Offboarding]:
        """Crea un proceso de offboarding"""
        try:
            empleado = self.crear_empleado(datos_generales)
            if not empleado:
                return None
            
            return Offboarding(
                empleado=empleado,
                submenu_offboarding=datos_especificos.get('submenu_offboarding', '')
            )
        except Exception as e:
            print(f"Error al crear offboarding: {str(e)}")
            return None
    
    def crear_lateral_movement(self, datos_generales: dict, datos_especificos: dict) -> Optional[LateralMovement]:
        """Crea un proceso de lateral movement"""
        try:
            empleado = self.crear_empleado(datos_generales)
            if not empleado:
                return None
            
            return LateralMovement(
                empleado=empleado,
                empleo_anterior=datos_especificos.get('empleo_anterior', ''),
                submenu_lateral=datos_especificos.get('submenu_lateral', '')
            )
        except Exception as e:
            print(f"Error al crear lateral movement: {str(e)}")
            return None
    
    def guardar_proceso(self, tipo_proceso: str, datos_generales: dict, 
                       datos_especificos: dict) -> Tuple[bool, str]:
        """Guarda un proceso según su tipo"""
        try:
            # Validar datos generales
            es_valido, errores = self.validar_datos_generales(datos_generales)
            if not es_valido:
                return False, f"Errores en datos generales: {', '.join(errores)}"
            
            # Validar tipo de proceso
            es_valido, error = self.validar_tipo_proceso(tipo_proceso)
            if not es_valido:
                return False, error
            
            # Crear y guardar el proceso según el tipo
            if tipo_proceso == 'onboarding':
                proceso = self.crear_onboarding(datos_generales, datos_especificos)
                if proceso:
                    exito = self.repository.guardar_onboarding(proceso)
                    return exito, "Onboarding guardado exitosamente" if exito else "Error al guardar onboarding"
            
            elif tipo_proceso == 'offboarding':
                proceso = self.crear_offboarding(datos_generales, datos_especificos)
                if proceso:
                    exito = self.repository.guardar_offboarding(proceso)
                    return exito, "Offboarding guardado exitosamente" if exito else "Error al guardar offboarding"
            
            elif tipo_proceso == 'lateral':
                proceso = self.crear_lateral_movement(datos_generales, datos_especificos)
                if proceso:
                    exito = self.repository.guardar_lateral_movement(proceso)
                    return exito, "Lateral movement guardado exitosamente" if exito else "Error al guardar lateral movement"
            
            return False, "Tipo de proceso no soportado"
            
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def guardar_persona_headcount(self, datos: dict) -> Tuple[bool, str]:
        """Guarda una persona en el headcount"""
        try:
            # Validar datos
            es_valido, errores = self.validar_datos_persona_headcount(datos)
            if not es_valido:
                return False, f"Errores en datos: {', '.join(errores)}"
            
            # Crear persona
            persona = self.crear_persona_headcount(datos)
            if not persona:
                return False, "Error al crear persona del headcount"
            
            # Guardar en repositorio
            exito = self.repository.guardar_persona_headcount(persona)
            return exito, "Persona guardada exitosamente en el headcount" if exito else "Error al guardar persona en el headcount"
            
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def buscar_por_sid(self, sid: str) -> List[dict]:
        """Busca registros por SID"""
        if not sid.strip():
            return []
        
        return self.repository.buscar_por_sid(sid.strip())
    
    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas de los procesos almacenados"""
        return self.repository.obtener_estadisticas()
    
    def cargar_onboardings(self) -> List[Onboarding]:
        """Carga todos los procesos de onboarding"""
        return self.repository.cargar_onboardings()
    
    def cargar_offboardings(self) -> List[Offboarding]:
        """Carga todos los procesos de offboarding"""
        return self.repository.cargar_offboardings()
    
    def cargar_lateral_movements(self) -> List[LateralMovement]:
        """Carga todos los procesos de lateral movement"""
        return self.repository.cargar_lateral_movements()
    
    def cargar_personas_headcount(self) -> List[PersonaHeadcount]:
        """Carga todas las personas del headcount"""
        return self.repository.cargar_personas_headcount()
