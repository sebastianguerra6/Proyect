"""
Servicio para gestionar la lógica de negocio entre las tablas:
- headcount (personas)
- applications (aplicaciones y accesos)
- historico (historial de procesos)
"""
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import sys
import os

# Agregar el directorio database al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from database_manager import DatabaseManager


class AccessManagementService:
    """Servicio principal para gestionar accesos y procesos"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        return self.db_manager.get_connection()
    
    # ==============================
    # MÉTODOS PARA HEADCOUNT
    # ==============================
    
    def create_employee(self, employee_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un nuevo empleado en headcount"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Validar datos requeridos
            required_fields = ['scotia_id', 'employee', 'full_name', 'email']
            for field in required_fields:
                if not employee_data.get(field):
                    return False, f"Campo requerido faltante: {field}"
            
            # Insertar empleado
            cursor.execute('''
                INSERT INTO headcount 
                (scotia_id, employee, full_name, email, position, manager, senior_manager, 
                 unit, start_date, coca, skip_level, coleadores, parents, personal_email, 
                 size, birthday, ubicacion, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                employee_data.get('scotia_id'),
                employee_data.get('employee'),
                employee_data.get('full_name'),
                employee_data.get('email'),
                employee_data.get('position'),
                employee_data.get('manager'),
                employee_data.get('senior_manager'),
                employee_data.get('unit'),
                employee_data.get('start_date'),
                employee_data.get('coca'),
                employee_data.get('skip_level'),
                employee_data.get('coleadores'),
                employee_data.get('parents'),
                employee_data.get('personal_email'),
                employee_data.get('size'),
                employee_data.get('birthday'),
                employee_data.get('ubicacion'),
                employee_data.get('activo', True)
            ))
            
            conn.commit()
            conn.close()
            
            return True, f"Empleado {employee_data.get('scotia_id')} creado exitosamente"
            
        except sqlite3.IntegrityError as e:
            return False, f"Error de integridad: El empleado {employee_data.get('scotia_id')} ya existe"
        except Exception as e:
            return False, f"Error creando empleado: {str(e)}"
    
    def get_employee_by_id(self, scotia_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por su scotia_id"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM headcount WHERE scotia_id = ?', (scotia_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                employee = dict(zip(columns, row))
                conn.close()
                return employee
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"Error obteniendo empleado: {e}")
            return None
    
    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Obtiene todos los empleados activos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM headcount WHERE activo = 1 ORDER BY full_name')
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            employees = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            return employees
            
        except Exception as e:
            print(f"Error obteniendo empleados: {e}")
            return []
    
    def update_employee_position(self, scotia_id: str, new_position: str, new_unit: str) -> Tuple[bool, str]:
        """Actualiza la posición y unidad de un empleado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE headcount 
                SET position = ?, unit = ?
                WHERE scotia_id = ?
            ''', (new_position, new_unit, scotia_id))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, f"Empleado {scotia_id} no encontrado"
            
            conn.commit()
            conn.close()
            
            return True, f"Posición actualizada para {scotia_id}"
            
        except Exception as e:
            return False, f"Error actualizando posición: {str(e)}"
    
    # ==============================
    # MÉTODOS PARA APPLICATIONS
    # ==============================
    
    def get_applications_by_position(self, position: str, unit: str) -> List[Dict[str, Any]]:
        """Obtiene las aplicaciones que debe tener un empleado según su posición y unidad"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM applications 
                WHERE position_role = ? AND unit = ?
                ORDER BY logical_access_name
            ''', (position, unit))
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            applications = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            return applications
            
        except Exception as e:
            print(f"Error obteniendo aplicaciones por posición: {e}")
            return []
    
    def get_all_applications(self) -> List[Dict[str, Any]]:
        """Obtiene todas las aplicaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM applications ORDER BY logical_access_name')
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            applications = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            return applications
            
        except Exception as e:
            print(f"Error obteniendo aplicaciones: {e}")
            return []
    
    def create_application(self, app_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea una nueva aplicación"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Validar datos requeridos
            if not app_data.get('logical_access_name'):
                return False, "Campo requerido faltante: logical_access_name"
            
            cursor.execute('''
                INSERT INTO applications 
                (jurisdiction, unit, subunit, logical_access_name, path_email_url, position_role, 
                 exception_tracking, fulfillment_action, system_owner, role_name, access_type, 
                 category, additional_data, ad_code, access_status, last_update_date, 
                 requirement_licensing, description, authentication_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                app_data.get('jurisdiction'),
                app_data.get('unit'),
                app_data.get('subunit'),
                app_data.get('logical_access_name'),
                app_data.get('path_email_url'),
                app_data.get('position_role'),
                app_data.get('exception_tracking'),
                app_data.get('fulfillment_action'),
                app_data.get('system_owner'),
                app_data.get('role_name'),
                app_data.get('access_type'),
                app_data.get('category'),
                app_data.get('additional_data'),
                app_data.get('ad_code'),
                app_data.get('access_status', 'Activo'),
                datetime.now().isoformat(),
                app_data.get('requirement_licensing'),
                app_data.get('description'),
                app_data.get('authentication_method')
            ))
            
            conn.commit()
            conn.close()
            
            return True, f"Aplicación {app_data.get('logical_access_name')} creada exitosamente"
            
        except sqlite3.IntegrityError as e:
            return False, f"Error de integridad: La aplicación ya existe"
        except Exception as e:
            return False, f"Error creando aplicación: {str(e)}"
    
    # ==============================
    # MÉTODOS PARA HISTORICO
    # ==============================
    
    def create_historical_record(self, record_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un registro en el historial"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Validar datos requeridos
            required_fields = ['scotia_id', 'process_access']
            for field in required_fields:
                if not record_data.get(field):
                    return False, f"Campo requerido faltante: {field}"
            
            cursor.execute('''
                INSERT INTO historico 
                (scotia_id, case_id, responsible, record_date, process_access, sid, area, subunit, 
                 event_description, ticket_email, app_access_name, computer_system_type, status, 
                 closing_date_app, closing_date_ticket, app_quality, confirmation_by_user, comment, 
                 ticket_quality, general_status, average_time_open_ticket)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record_data.get('scotia_id'),
                record_data.get('case_id'),
                record_data.get('responsible'),
                record_data.get('record_date', datetime.now().isoformat()),
                record_data.get('process_access'),
                record_data.get('sid'),
                record_data.get('area'),
                record_data.get('subunit'),
                record_data.get('event_description'),
                record_data.get('ticket_email'),
                record_data.get('app_access_name'),
                record_data.get('computer_system_type'),
                record_data.get('status', 'Pendiente'),
                record_data.get('closing_date_app'),
                record_data.get('closing_date_ticket'),
                record_data.get('app_quality'),
                record_data.get('confirmation_by_user'),
                record_data.get('comment'),
                record_data.get('ticket_quality'),
                record_data.get('general_status'),
                record_data.get('average_time_open_ticket')
            ))
            
            conn.commit()
            conn.close()
            
            return True, "Registro histórico creado exitosamente"
            
        except Exception as e:
            return False, f"Error creando registro histórico: {str(e)}"
    
    def get_employee_history(self, scotia_id: str) -> List[Dict[str, Any]]:
        """Obtiene el historial de un empleado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT h.*, a.logical_access_name, a.description as app_description
                FROM historico h
                LEFT JOIN applications a ON h.app_access_name = a.logical_access_name
                WHERE h.scotia_id = ?
                ORDER BY h.record_date DESC
            ''', (scotia_id,))
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            history = [dict(zip(columns, row)) for row in rows]
            
            conn.close()
            return history
            
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []
    
    # ==============================
    # MÉTODOS DE LÓGICA DE NEGOCIO
    # ==============================
    
    def process_employee_onboarding(self, scotia_id: str, position: str, unit: str, 
                                  responsible: str = "Sistema") -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa el onboarding de un empleado y determina qué accesos necesita"""
        try:
            # 1. Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []
            
            # 2. Obtener aplicaciones requeridas para la posición
            required_apps = self.get_applications_by_position(position, unit)
            
            if not required_apps:
                return False, f"No se encontraron aplicaciones para la posición {position} en {unit}", []
            
            # 3. Crear registros históricos para cada aplicación
            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []
            
            for app in required_apps:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'onboarding',
                    'sid': scotia_id,
                    'area': unit,
                    'subunit': app.get('subunit', ''),
                    'event_description': f"Acceso requerido para {app.get('logical_access_name')}",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': app.get('logical_access_name'),
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                
                success, message = self.create_historical_record(record_data)
                if success:
                    created_records.append(record_data)
                else:
                    print(f"Error creando registro para {app.get('logical_access_name')}: {message}")
            
            return True, f"Onboarding procesado para {scotia_id}. {len(created_records)} accesos requeridos.", created_records
            
        except Exception as e:
            return False, f"Error procesando onboarding: {str(e)}", []
    
    def process_employee_offboarding(self, scotia_id: str, responsible: str = "Sistema") -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa el offboarding de un empleado"""
        try:
            # 1. Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []
            
            # 2. Obtener historial de accesos del empleado
            history = self.get_employee_history(scotia_id)
            active_access = [h for h in history if h.get('status') == 'Completado' and h.get('process_access') == 'onboarding']
            
            # 3. Crear registros de offboarding para cada acceso activo
            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []
            
            for access in active_access:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'offboarding',
                    'sid': scotia_id,
                    'area': access.get('area', ''),
                    'subunit': access.get('subunit', ''),
                    'event_description': f"Revocación de acceso para {access.get('app_access_name')}",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': access.get('app_access_name'),
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                
                success, message = self.create_historical_record(record_data)
                if success:
                    created_records.append(record_data)
                else:
                    print(f"Error creando registro de offboarding para {access.get('app_access_name')}: {message}")
            
            # 4. Marcar empleado como inactivo
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE headcount SET activo = 0 WHERE scotia_id = ?', (scotia_id,))
            conn.commit()
            conn.close()
            
            return True, f"Offboarding procesado para {scotia_id}. {len(created_records)} accesos a revocar.", created_records
            
        except Exception as e:
            return False, f"Error procesando offboarding: {str(e)}", []
    
    def process_lateral_movement(self, scotia_id: str, new_position: str, new_unit: str, 
                               responsible: str = "Sistema") -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa un movimiento lateral de empleado"""
        try:
            # 1. Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []
            
            old_position = employee.get('position', '')
            old_unit = employee.get('unit', '')
            
            # 2. Obtener accesos actuales y nuevos requeridos
            current_apps = self.get_applications_by_position(old_position, old_unit)
            new_apps = self.get_applications_by_position(new_position, new_unit)
            
            # 3. Determinar accesos a revocar y otorgar
            current_app_names = {app.get('logical_access_name') for app in current_apps}
            new_app_names = {app.get('logical_access_name') for app in new_apps}
            
            to_revoke = current_app_names - new_app_names
            to_grant = new_app_names - current_app_names
            
            # 4. Crear registros históricos
            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []
            
            # Revocar accesos
            for app_name in to_revoke:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'lateral_movement',
                    'sid': scotia_id,
                    'area': new_unit,
                    'subunit': '',
                    'event_description': f"Revocación de acceso para {app_name} (movimiento lateral)",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': app_name,
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                
                success, message = self.create_historical_record(record_data)
                if success:
                    created_records.append(record_data)
            
            # Otorgar nuevos accesos
            for app_name in to_grant:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'lateral_movement',
                    'sid': scotia_id,
                    'area': new_unit,
                    'subunit': '',
                    'event_description': f"Otorgamiento de acceso para {app_name} (movimiento lateral)",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': app_name,
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                
                success, message = self.create_historical_record(record_data)
                if success:
                    created_records.append(record_data)
            
            # 5. Actualizar posición del empleado
            success, message = self.update_employee_position(scotia_id, new_position, new_unit)
            if not success:
                return False, f"Error actualizando posición: {message}", []
            
            return True, f"Movimiento lateral procesado para {scotia_id}. {len(to_revoke)} accesos a revocar, {len(to_grant)} accesos a otorgar.", created_records
            
        except Exception as e:
            return False, f"Error procesando movimiento lateral: {str(e)}", []
    
    def get_access_reconciliation_report(self, scotia_id: str) -> Dict[str, Any]:
        """Genera un reporte de conciliación de accesos para un empleado"""
        try:
            # 1. Obtener datos del empleado
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return {"error": f"Empleado {scotia_id} no encontrado"}
            
            # 2. Obtener accesos requeridos según posición
            required_apps = self.get_applications_by_position(employee.get('position', ''), employee.get('unit', ''))
            
            # 3. Obtener historial de accesos
            history = self.get_employee_history(scotia_id)
            
            # 4. Determinar accesos actuales (completados)
            current_access = []
            for record in history:
                if record.get('status') == 'Completado' and record.get('process_access') in ['onboarding', 'lateral_movement']:
                    current_access.append({
                        'app_name': record.get('app_access_name'),
                        'role_name': record.get('app_description', ''),
                        'granted_date': record.get('record_date')
                    })
            
            # 5. Determinar accesos faltantes y excesivos
            current_app_names = {access.get('app_name') for access in current_access}
            required_app_names = {app.get('logical_access_name') for app in required_apps}
            
            to_grant = []
            for app in required_apps:
                if app.get('logical_access_name') not in current_app_names:
                    to_grant.append({
                        'app_name': app.get('logical_access_name'),
                        'role_name': app.get('role_name', ''),
                        'description': app.get('description', '')
                    })
            
            to_revoke = []
            for access in current_access:
                if access.get('app_name') not in required_app_names:
                    to_revoke.append(access)
            
            return {
                "employee": employee,
                "current_access": current_access,
                "to_grant": to_grant,
                "to_revoke": to_revoke,
                "summary": {
                    "total_current": len(current_access),
                    "total_required": len(required_apps),
                    "to_grant_count": len(to_grant),
                    "to_revoke_count": len(to_revoke)
                }
            }
            
        except Exception as e:
            return {"error": f"Error generando reporte: {str(e)}"}


# Instancia global del servicio
access_service = AccessManagementService()
