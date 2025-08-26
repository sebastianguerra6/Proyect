from typing import List, Optional, Tuple, Dict, Any
from models import Empleado, Onboarding, Offboarding, LateralMovement, PersonaHeadcount
from data import EmpleadoRepository
from tkinter import messagebox

class EmpleadoService:
    """Servicio para manejar la lógica de negocio de empleados"""
    
    def __init__(self, repository: EmpleadoRepository):
        self.repository = repository
    
    def validar_datos_generales(self, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida los datos generales del empleado"""
        campos_obligatorios = ['sid', 'nueva_sub_unidad', 'nuevo_cargo', 'status']
        campos_vacios = []
        
        for campo in campos_obligatorios:
            if not datos.get(campo, '').strip():
                campos_vacios.append(campo)
        
        if campos_vacios:
            return False, f"Campos obligatorios vacíos: {', '.join(campos_vacios)}"
        
        return True, "Datos válidos"
    
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
    
    def crear_empleado(self, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuevo empleado"""
        exito, mensaje = self.validar_datos_generales(datos)
        if not exito:
            return False, mensaje
        
        try:
            empleado = Empleado(
                sid=datos['sid'],
                nueva_sub_unidad=datos['nueva_sub_unidad'],
                nuevo_cargo=datos['nuevo_cargo'],
                ingreso_por=datos.get('ingreso_por', ''),
                request_date=datos.get('request_date'),
                fecha=datos.get('fecha'),
                status=datos.get('status', 'Pendiente')
            )
            
            return True, f"Empleado creado exitosamente. Número de caso: {empleado.numero_caso}"
        except Exception as e:
            return False, f"Error al crear empleado: {str(e)}"
    
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
            es_valido, mensaje = self.validar_datos_generales(datos_generales)
            if not es_valido:
                return False, mensaje
            
            # Validar tipo de proceso
            es_valido, error = self.validar_tipo_proceso(tipo_proceso)
            if not es_valido:
                return False, error
            
            # Crear empleado para obtener el número de caso
            empleado = Empleado(
                sid=datos_generales['sid'],
                nueva_sub_unidad=datos_generales['nueva_sub_unidad'],
                nuevo_cargo=datos_generales['nuevo_cargo'],
                ingreso_por=datos_generales.get('ingreso_por', ''),
                request_date=datos_generales.get('request_date'),
                fecha=datos_generales.get('fecha'),
                status=datos_generales.get('status', 'Pendiente')
            )
            
            # Crear y guardar el proceso según el tipo
            if tipo_proceso == 'onboarding':
                proceso = Onboarding(
                    empleado=empleado,
                    submenu_onboarding=datos_especificos.get('submenu_onboarding', '')
                )
                exito = self.repository.guardar_onboarding(proceso)
                mensaje_exito = f"Onboarding guardado exitosamente. Número de caso: {empleado.numero_caso}"
                return exito, mensaje_exito if exito else "Error al guardar onboarding"
            
            elif tipo_proceso == 'offboarding':
                proceso = Offboarding(
                    empleado=empleado,
                    submenu_offboarding=datos_especificos.get('submenu_offboarding', '')
                )
                exito = self.repository.guardar_offboarding(proceso)
                mensaje_exito = f"Offboarding guardado exitosamente. Número de caso: {empleado.numero_caso}"
                return exito, mensaje_exito if exito else "Error al guardar offboarding"
            
            elif tipo_proceso == 'lateral':
                proceso = LateralMovement(
                    empleado=empleado,
                    empleo_anterior=datos_especificos.get('empleo_anterior', ''),
                    submenu_lateral=datos_especificos.get('submenu_lateral', '')
                )
                exito = self.repository.guardar_lateral_movement(proceso)
                mensaje_exito = f"Lateral movement guardado exitosamente. Número de caso: {empleado.numero_caso}"
                return exito, mensaje_exito if exito else "Error al guardar lateral movement"
            
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
    
    def buscar_por_sid(self, sid: str) -> List[Dict[str, Any]]:
        """Busca registros por SID"""
        return self.repository.buscar_por_sid(sid)
    
    def buscar_por_numero_caso(self, numero_caso: str) -> List[Dict[str, Any]]:
        """Busca registros por número de caso"""
        return self.repository.buscar_por_numero_caso(numero_caso)
    
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
