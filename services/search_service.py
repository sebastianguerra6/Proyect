"""
Servicio de búsqueda para el sistema de gestión de empleados
Sistema optimizado para SQL Server únicamente
"""
import pyodbc
from typing import List, Dict, Any, Optional
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import get_database_connection


class SearchService:
    """Servicio para realizar búsquedas en la base de datos"""
    
    def __init__(self):
        self.db_manager = get_database_connection()
    
    def get_connection(self) -> pyodbc.Connection:
        """Obtiene una conexión a la base de datos"""
        return self.db_manager.get_connection()
    
    def buscar_procesos(self, filtros: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Busca procesos en la tabla histórico con filtros opcionales
        
        Args:
            filtros: Diccionario con filtros de búsqueda
            
        Returns:
            Lista de procesos encontrados
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Query base - seleccionar todos los campos relevantes
            query = """
                SELECT case_id, sid, scotia_id, process_access, record_date, 
                       status, comment, responsible, area, subunit, event_description,
                       ticket_email, app_access_name, closing_date_app, app_quality,
                       confirmation_by_user
                FROM historico
            """
            
            conditions = []
            params = []
            
            if filtros:
                if filtros.get('case_id'):
                    conditions.append("case_id LIKE ?")
                    params.append(f"%{filtros['case_id']}%")
                
                if filtros.get('sid'):
                    conditions.append("sid LIKE ?")
                    params.append(f"%{filtros['sid']}%")
                
                if filtros.get('scotia_id'):
                    conditions.append("scotia_id LIKE ?")
                    params.append(f"%{filtros['scotia_id']}%")
                
                if filtros.get('process_access'):
                    conditions.append("process_access LIKE ?")
                    params.append(f"%{filtros['process_access']}%")
                
                if filtros.get('status'):
                    conditions.append("status = ?")
                    params.append(filtros['status'])
                
                if filtros.get('fecha_desde'):
                    conditions.append("record_date >= ?")
                    params.append(filtros['fecha_desde'])
                
                if filtros.get('fecha_hasta'):
                    conditions.append("record_date <= ?")
                    params.append(filtros['fecha_hasta'])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY record_date DESC"
            
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                result_dict = dict(zip(columns, row))
                results.append(result_dict)
            
            return results
            
        except Exception as e:
            print(f"Error en buscar_procesos: {e}")
            return []
    
    def buscar_headcount_por_sid(self, sid: str) -> List[Dict[str, Any]]:
        """
        Busca empleados en headcount por SID
        
        Args:
            sid: SID del empleado
            
        Returns:
            Lista de empleados encontrados
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT scotia_id, employee, full_name, email, position, manager, 
                       senior_manager, unit, unidad_subunidad, start_date, ceco, skip_level, 
                       cafe_alcides, parents, personal_email, size, birthday, 
                       validacion, activo
                FROM headcount
                WHERE employee LIKE ?
                ORDER BY full_name
            """
            
            cursor.execute(query, (f"%{sid}%",))
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                result_dict = dict(zip(columns, row))
                results.append(result_dict)
            
            return results
            
        except Exception as e:
            print(f"Error en buscar_headcount_por_sid: {e}")
            return []
    
    def obtener_todo_headcount(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los empleados de headcount
        
        Returns:
            Lista de todos los empleados
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT scotia_id, employee, full_name, email, position, manager, 
                       senior_manager, unit, unidad_subunidad, start_date, ceco, skip_level, 
                       cafe_alcides, parents, personal_email, size, birthday, 
                       validacion, activo
                FROM headcount
                ORDER BY full_name
            """
            
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                result_dict = dict(zip(columns, row))
                results.append(result_dict)
            
            return results
            
        except Exception as e:
            print(f"Error en obtener_todo_headcount: {e}")
            return []
    
    def actualizar_proceso(self, case_id: str, datos_actualizados: Dict[str, Any]) -> tuple[bool, str]:
        """
        Actualiza un proceso en la tabla histórico
        
        Args:
            case_id: ID del caso a actualizar
            datos_actualizados: Diccionario con los datos a actualizar
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener el scotia_id del registro para obtener el email del headcount
            cursor.execute('SELECT scotia_id FROM historico WHERE case_id = ?', (case_id,))
            scotia_id_result = cursor.fetchone()
            if scotia_id_result:
                scotia_id = scotia_id_result[0]
                # Obtener el email del empleado desde headcount
                cursor.execute('SELECT email FROM headcount WHERE scotia_id = ?', (scotia_id,))
                email_result = cursor.fetchone()
                if email_result:
                    datos_actualizados['employee_email'] = email_result[0]
            
            # Construir query de actualización dinámicamente
            set_clauses = []
            params = []
            
            for campo, valor in datos_actualizados.items():
                if campo != 'case_id':  # No actualizar el ID del caso
                    set_clauses.append(f"{campo} = ?")
                    params.append(valor)
            
            if not set_clauses:
                return False, "No hay datos para actualizar"
            
            # Agregar fecha de actualización
            set_clauses.append("record_date = datetime('now')")
            
            query = f"""
                UPDATE historico 
                SET {', '.join(set_clauses)}
                WHERE case_id = ?
            """
            params.append(case_id)
            
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, f"Proceso {case_id} actualizado exitosamente"
            else:
                return False, f"No se encontró el proceso {case_id}"
                
        except Exception as e:
            print(f"Error en actualizar_proceso: {e}")
            return False, f"Error al actualizar: {str(e)}"


# Instancia global del servicio
search_service = SearchService()
