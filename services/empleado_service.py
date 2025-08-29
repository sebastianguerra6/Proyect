from typing import Dict, Any, List, Tuple
from models import Empleado

class EmpleadoService:
    """Servicio para manejar la lógica de negocio de empleados usando base de datos"""
    
    def __init__(self, repository):
        self.repository = repository
    
    def crear_empleado(self, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un empleado en el headcount"""
        try:
            # Validar datos obligatorios
            campos_obligatorios = ['nombre', 'apellido', 'email', 'departamento', 'cargo']
            campos_vacios = [campo for campo in campos_obligatorios if not datos.get(campo)]
            
            if campos_vacios:
                return False, f"Campos obligatorios faltantes: {', '.join(campos_vacios)}"
            
            # Generar número de caso si no existe
            if not datos.get('numero_caso'):
                empleado = Empleado(
                    sid=datos.get('sid', ''),
                    nueva_sub_unidad=datos.get('nueva_sub_unidad', ''),
                    nuevo_cargo=datos.get('nuevo_cargo', ''),
                    nombre=datos.get('nombre', ''),
                    apellido=datos.get('apellido', ''),
                    email=datos.get('email', ''),
                    departamento=datos.get('departamento', ''),
                    cargo=datos.get('cargo', '')
                )
                datos['numero_caso'] = empleado.numero_caso
            
            # Guardar en headcount
            exito, mensaje = self.repository.guardar_headcount(datos)
            return exito, mensaje
            
        except Exception as e:
            return False, f"Error creando empleado: {str(e)}"
    
    def guardar_proceso(self, tipo_proceso: str, datos_generales: Dict[str, Any], 
                        datos_especificos: Dict[str, Any]) -> Tuple[bool, str]:
        """Guarda un proceso (onboarding, offboarding, lateral movement)"""
        try:
            # Combinar datos generales con específicos
            datos_completos = {**datos_generales, **datos_especificos}
            datos_completos['tipo_proceso'] = tipo_proceso
            
            # Generar número de caso si no existe
            if not datos_completos.get('numero_caso'):
                empleado = Empleado(
                    sid=datos_completos.get('sid', ''),
                    nueva_sub_unidad=datos_completos.get('nueva_sub_unidad', ''),
                    nuevo_cargo=datos_completos.get('nuevo_cargo', ''),
                    ingreso_por=datos_completos.get('ingreso_por', ''),
                    request_date=datos_completos.get('request_date'),
                    fecha=datos_completos.get('fecha'),
                    status=datos_completos.get('status', 'Pendiente')
                )
                datos_completos['numero_caso'] = empleado.numero_caso
            
            # Guardar en la base de datos
            exito, mensaje = self.repository.guardar_proceso(datos_completos, tipo_proceso)
            return exito, mensaje
            
        except Exception as e:
            return False, f"Error guardando proceso: {str(e)}"
    
    def buscar_procesos(self, filtros: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Busca procesos según los filtros especificados"""
        try:
            return self.repository.buscar_procesos(filtros)
        except Exception as e:
            print(f"Error en búsqueda de procesos: {e}")
            return []
    
    def actualizar_proceso(self, numero_caso: str, datos_actualizados: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualiza un proceso existente"""
        try:
            return self.repository.actualizar_proceso(numero_caso, datos_actualizados)
        except Exception as e:
            return False, f"Error actualizando proceso: {str(e)}"
    
    def obtener_estadisticas(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        try:
            return self.repository.obtener_estadisticas()
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {'onboarding': 0, 'offboarding': 0, 'lateral_movement': 0, 'headcount': 0}
    
    def buscar_headcount_por_sid(self, sid: str) -> List[Dict[str, Any]]:
        """Busca personas en el headcount por SID"""
        try:
            return self.repository.buscar_headcount_por_sid(sid)
        except Exception as e:
            print(f"Error buscando headcount por SID: {e}")
            return []
    
    def obtener_todo_headcount(self) -> List[Dict[str, Any]]:
        """Obtiene todos los registros del headcount"""
        try:
            return self.repository.obtener_todo_headcount()
        except Exception as e:
            print(f"Error obteniendo todo el headcount: {e}")
            return []
