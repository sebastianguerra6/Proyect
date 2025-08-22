from typing import List, Optional, Tuple
from models import Empleado, Onboarding, Offboarding, LateralMovement
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
