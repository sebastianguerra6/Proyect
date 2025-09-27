"""
Servicio para gestionar la lógica de negocio entre las tablas:
- headcount (personas)
- applications (aplicaciones y accesos)
- historico (historial de procesos)

Sistema optimizado para SQL Server únicamente.
"""
import pyodbc
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import sys
import os

# Importar configuración
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import get_database_connection


class AccessManagementService:
    """Servicio principal para gestionar accesos y procesos"""

    # ==============================
    # UTILIDADES INTERNAS
    # ==============================
    @staticmethod
    def _access_key(unit: Optional[str], subunit: Optional[str], position_role: Optional[str], logical_access_name: Optional[str]) -> Tuple[str, str, str, str]:
        """Crea una clave normalizada para comparar accesos por 4 campos.
        Orden: (unit, subunit, position_role, logical_access_name)
        """
        return (
            (unit or '').strip(),
            (subunit or '').strip(),
            (position_role or '').strip(),
            (logical_access_name or '').strip(),
        )

    @staticmethod
    def _triplet_key(unit: Optional[str], position_role: Optional[str], logical_access_name: Optional[str]) -> Tuple[str, str, str]:
        """Crea una clave normalizada para comparar accesos por 3 campos (ignora subunit).
        Orden: (unit, position_role, logical_access_name)
        """
        return (
            (unit or '').strip().upper(),
            (position_role or '').strip().upper(),
            (logical_access_name or '').strip().upper(),
        )

    def __init__(self):
        """Inicializa el servicio con conexión a SQL Server"""
        self.db_manager = get_database_connection()
        self._ensure_views_and_indexes()

    def get_connection(self) -> pyodbc.Connection:
        """Obtiene una conexión a la base de datos"""
        return self.db_manager.get_connection()

    def _ensure_views_and_indexes(self):
        """Asegura que existan los índices necesarios para SQL Server"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Crear índices para optimizar las consultas (sintaxis SQL Server)
            indexes = [
                "IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_applications_unit_position' AND object_id = OBJECT_ID('applications')) CREATE INDEX idx_applications_unit_position ON applications (unit, position_role)",
                "IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_historico_scotia_status' AND object_id = OBJECT_ID('historico')) CREATE INDEX idx_historico_scotia_status ON historico (scotia_id, status)",
                "IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_historico_process_status' AND object_id = OBJECT_ID('historico')) CREATE INDEX idx_historico_process_status ON historico (process_access, status)",
                "IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_headcount_unit_position' AND object_id = OBJECT_ID('headcount')) CREATE INDEX idx_headcount_unit_position ON headcount (unit, position)"
            ]
            
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                except Exception as e:
                    print(f"Advertencia: No se pudo crear índice: {e}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error creando vistas e índices: {e}")
            # No lanzar excepción para no interrumpir la inicialización

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
                 unit, start_date, ceco, skip_level, cafe_alcides, parents, personal_email, 
                 size, birthday, validacion, activo)
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
                employee_data.get('ceco'),
                employee_data.get('skip_level'),
                employee_data.get('cafe_alcides'),
                employee_data.get('parents'),
                employee_data.get('personal_email'),
                employee_data.get('size'),
                employee_data.get('birthday'),
                employee_data.get('validacion'),
                employee_data.get('activo', True)
            ))

            conn.commit()
            conn.close()

            return True, f"Empleado {employee_data.get('scotia_id')} creado exitosamente"

        except pyodbc.IntegrityError:
            return False, f"Error de integridad: El empleado {employee_data.get('scotia_id')} ya existe"
        except Exception as e:
            return False, f"Error creando empleado: {str(e)}"

    def get_employee_by_id(self, scotia_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por su scotia_id usando consulta directa"""
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
        """Obtiene todos los empleados activos usando consulta directa"""
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

    def update_employee(self, scotia_id: str, employee_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualiza todos los datos de un empleado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Construir query de actualización dinámicamente
            set_clauses = []
            params = []

            for campo, valor in employee_data.items():
                if campo != 'scotia_id':  # No actualizar el SID
                    set_clauses.append(f"{campo} = ?")
                    params.append(valor)

            if not set_clauses:
                return False, "No hay datos para actualizar"

            query = f"""
                UPDATE headcount 
                SET {', '.join(set_clauses)}
                WHERE scotia_id = ?
            """
            params.append(scotia_id)

            cursor.execute(query, params)

            if cursor.rowcount == 0:
                conn.close()
                return False, f"Empleado {scotia_id} no encontrado"

            conn.commit()
            conn.close()

            return True, f"Empleado {scotia_id} actualizado exitosamente"

        except Exception as e:
            return False, f"Error actualizando empleado: {str(e)}"

    def delete_employee(self, scotia_id: str) -> Tuple[bool, str]:
        """Elimina un empleado del headcount"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Verificar si el empleado existe
            cursor.execute('SELECT full_name FROM headcount WHERE scotia_id = ?', (scotia_id,))
            empleado = cursor.fetchone()

            if not empleado:
                conn.close()
                return False, f"Empleado {scotia_id} no encontrado"

            # Eliminar el empleado
            cursor.execute('DELETE FROM headcount WHERE scotia_id = ?', (scotia_id,))

            if cursor.rowcount == 0:
                conn.close()
                return False, f"No se pudo eliminar el empleado {scotia_id}"

            conn.commit()
            conn.close()

            return True, f"Empleado {scotia_id} eliminado exitosamente"

        except Exception as e:
            return False, f"Error eliminando empleado: {str(e)}"

    # ==============================
    # MÉTODOS PARA APPLICATIONS
    # ==============================

    def get_applications_by_position(self, position: str, unit: str, subunit: Optional[str] = None, title: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene las aplicaciones que debe tener un empleado según posición/unidad/subunidad/título.
        **Sin duplicados**: devuelve una fila por tripleta (unit, position_role, logical_access_name).
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Construir consulta dinámicamente
            query = 'SELECT logical_access_name, jurisdiction, unit, subunit, alias, path_email_url, position_role, exception_tracking, fulfillment_action, system_owner, role_name, access_type, category, additional_data, ad_code, access_status, last_update_date, require_licensing, description, authentication_method FROM applications WHERE 1=1'
            params = []
            
            if unit:
                query += ' AND UPPER(LTRIM(RTRIM(unit))) = UPPER(LTRIM(RTRIM(?)))'
                params.append(unit)
            
            if subunit:
                query += ' AND UPPER(LTRIM(RTRIM(subunit))) = UPPER(LTRIM(RTRIM(?)))'
                params.append(subunit)
            
            if position:
                query += ' AND UPPER(LTRIM(RTRIM(position_role))) = UPPER(LTRIM(RTRIM(?)))'
                params.append(position)
            
            if title:
                query += ' AND UPPER(LTRIM(RTRIM(role_name))) = UPPER(LTRIM(RTRIM(?)))'
                params.append(title)
            
            query += ' ORDER BY logical_access_name'
            
            cursor.execute(query, params)

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

    def _get_application_by_name(self, logical_access_name: str) -> Optional[Dict[str, Any]]:
        """Obtiene una aplicación por su logical_access_name"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT logical_access_name, jurisdiction, unit, subunit, 
                       alias, path_email_url, position_role, exception_tracking, 
                       fulfillment_action, system_owner, role_name, access_type, 
                       category, additional_data, ad_code, access_status, 
                       last_update_date, require_licensing, description, 
                       authentication_method
                FROM applications 
                WHERE logical_access_name = ?
                LIMIT 1
            ''', (logical_access_name,))

            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                app = dict(zip(columns, row))
                conn.close()
                return app

            conn.close()
            return None

        except Exception as e:
            print(f"Error obteniendo aplicación por nombre: {e}")
            return None

    def create_application(self, app_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea una nueva aplicación"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Validar datos requeridos
            if not app_data.get('logical_access_name'):
                return False, "Campo requerido faltante: logical_access_name"

            # Usar OUTPUT INSERTED.id para SQL Server
            cursor.execute('''
                INSERT INTO applications 
                (jurisdiction, unit, subunit, logical_access_name, alias, path_email_url, position_role, 
                 exception_tracking, fulfillment_action, system_owner, role_name, access_type, 
                 category, additional_data, ad_code, access_status, last_update_date, 
                 require_licensing, description, authentication_method)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                app_data.get('jurisdiction'),
                app_data.get('unit'),
                app_data.get('subunit'),
                app_data.get('logical_access_name'),
                app_data.get('alias'),
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
                app_data.get('require_licensing'),
                app_data.get('description'),
                app_data.get('authentication_method')
            ))
            app_id = cursor.fetchone()[0]

            conn.commit()
            conn.close()

            return True, f"Aplicación {app_data.get('logical_access_name')} creada exitosamente con ID {app_id}"

        except pyodbc.IntegrityError:
            return False, "Error de integridad: La aplicación ya existe"
        except Exception as e:
            return False, f"Error creando aplicación: {str(e)}"

    def update_application(self, app_id: int, app_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualiza una aplicación existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM applications WHERE id = ?', (app_id,))
            result = cursor.fetchone()
            if not result or result[0] == 0:
                return False, f"Aplicación con ID {app_id} no encontrada"

            set_clauses = []
            params = []

            for field, value in app_data.items():
                if field in ['jurisdiction', 'unit', 'subunit', 'logical_access_name', 'alias', 'path_email_url', 
                           'position_role', 'exception_tracking', 'fulfillment_action', 'system_owner', 
                           'role_name', 'access_type', 'category', 'additional_data', 'ad_code', 
                           'access_status', 'require_licensing', 'description', 'authentication_method']:
                    set_clauses.append(f"{field} = ?")
                    params.append(value)

            if not set_clauses:
                return False, "No hay campos válidos para actualizar"

            set_clauses.append("last_update_date = ?")
            params.append(datetime.now().isoformat())

            params.append(app_id)

            query = f"UPDATE applications SET {', '.join(set_clauses)} WHERE id = ?"
            cursor.execute(query, params)

            conn.commit()
            conn.close()

            return True, f"Aplicación {app_id} actualizada exitosamente"

        except Exception as e:
            return False, f"Error actualizando aplicación: {str(e)}"

    def delete_application(self, app_id: int) -> Tuple[bool, str]:
        """Elimina una aplicación"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT logical_access_name FROM applications WHERE id = ?', (app_id,))
            result = cursor.fetchone()
            if not result:
                return False, f"Aplicación con ID {app_id} no encontrada"

            app_name = result[0]

            cursor.execute('SELECT COUNT(*) FROM historico WHERE app_access_name = ?', (app_name,))
            historico_count = cursor.fetchone()[0]

            if historico_count > 0:
                return False, f"No se puede eliminar la aplicación porque tiene {historico_count} registros en el historial"

            cursor.execute('DELETE FROM applications WHERE id = ?', (app_id,))

            conn.commit()
            conn.close()

            return True, f"Aplicación {app_name} eliminada exitosamente"

        except Exception as e:
            return False, f"Error eliminando aplicación: {str(e)}"

    # ==============================
    # MÉTODOS PARA HISTORICO
    # ==============================

    def create_manual_access_record(self, scotia_id: str, app_name: str, 
                                   responsible: str = "Manual", 
                                   description: str = None) -> Tuple[bool, str]:
        """Crea un registro manual individual de acceso para una persona específica"""
        try:
            # Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado"
            
            # Generar case_id único
            case_id = f"MANUAL-{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{scotia_id}"
            
            # Crear descripción si no se proporciona
            if not description:
                description = f"Acceso manual a {app_name} para {employee.get('full_name', scotia_id)}"
            
            # Datos del registro manual
            record_data = {
                'scotia_id': scotia_id,
                'case_id': case_id,
                'responsible': responsible,
                'record_date': datetime.now().isoformat(),
                'request_date': datetime.now().strftime('%Y-%m-%d'),
                'process_access': 'manual_access',
                'sid': scotia_id,
                'area': employee.get('unit', 'Sin Unidad'),
                'subunit': employee.get('unit', 'Sin Unidad'),
                'event_description': description,
                'ticket_email': f"{responsible}@empresa.com",
                'app_access_name': app_name,
                'computer_system_type': 'Desktop',
                'status': 'Pendiente',
                'closing_date_app': None,
                'closing_date_ticket': None,
                'app_quality': None,
                'confirmation_by_user': None,
                'comment': f"Registro manual creado por {responsible}",
                'ticket_quality': None,
                'general_status': 'Pendiente',
                'average_time_open_ticket': None
            }
            
            # Crear el registro
            success, message = self.create_historical_record(record_data)
            
            if success:
                return True, f"Registro manual creado exitosamente para {scotia_id} - {app_name}"
            else:
                return False, f"Error creando registro manual: {message}"
                
        except Exception as e:
            return False, f"Error creando registro manual: {str(e)}"

    def create_historical_record(self, record_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Crea un registro en el historial con verificación anti-duplicados"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            required_fields = ['scotia_id', 'process_access']
            for field in required_fields:
                if not record_data.get(field):
                    return False, f"Campo requerido faltante: {field}"

            # Verificación anti-duplicados: evita más de un "Pendiente" por la misma app/empleado
            # PERO permite registros de offboarding incluso si ya existe un registro pendiente
            process_access = record_data.get('process_access', '')
            if process_access != 'offboarding':
                cursor.execute('''
                    SELECT COUNT(*) FROM historico
                    WHERE scotia_id = ?
                      AND status = 'Pendiente'
                      AND UPPER(TRIM(app_access_name)) = UPPER(TRIM(?))
                ''', (record_data['scotia_id'], record_data.get('app_access_name', '')))
                
                existing_count = cursor.fetchone()[0]
                if existing_count > 0:
                    conn.close()
                    return True, f"Registro ya pendiente; no se duplicó (existentes: {existing_count})"

            cursor.execute('''
                INSERT INTO historico 
                (scotia_id, case_id, responsible, record_date, request_date, process_access, sid, area, subunit, 
                 event_description, ticket_email, app_access_name, computer_system_type, status, 
                 closing_date_app, closing_date_ticket, app_quality, confirmation_by_user, comment, 
                 ticket_quality, general_status, average_time_open_ticket)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record_data.get('scotia_id'),
                record_data.get('case_id'),
                record_data.get('responsible'),
                record_data.get('record_date', datetime.now().isoformat()),
                record_data.get('request_date'),
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
        """Obtiene el historial de un empleado incluyendo metadatos de la app para comparación estricta.
        Evita duplicados usando subconsulta para obtener solo una app por logical_access_name.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 
                    h.*, 
                    a.logical_access_name AS app_logical_access_name,
                    a.description AS app_description,
                    a.unit AS app_unit,
                    a.subunit AS app_subunit,
                    a.position_role AS app_position_role
                FROM historico h
                LEFT JOIN (
                    SELECT 
                        logical_access_name,
                        description,
                        unit,
                        subunit,
                        position_role,
                        ROW_NUMBER() OVER (PARTITION BY logical_access_name ORDER BY id) as rn
                    FROM applications
                ) a ON h.app_access_name = a.logical_access_name AND a.rn = 1
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

    def get_employee_current_access(self, scotia_id: str) -> List[Dict[str, Any]]:
        """Obtiene los accesos actuales del empleado (completados y pendientes)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT DISTINCT
                    h.scotia_id,
                    h.area as unit,
                    h.subunit,
                    h.app_access_name as logical_access_name,
                    h.record_date,
                    h.status,
                    h.process_access,
                    a.position_role
                FROM historico h
                LEFT JOIN applications a ON h.app_access_name = a.logical_access_name
                WHERE h.scotia_id = ?
                AND h.status IN ('Completado', 'Pendiente', 'En Proceso')
                AND h.process_access IN ('onboarding', 'lateral_movement')
                AND h.app_access_name IS NOT NULL
                ORDER BY h.record_date DESC
            ''', (scotia_id,))

            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            current_access = [dict(zip(columns, row)) for row in rows]

            conn.close()
            return current_access

        except Exception as e:
            print(f"Error obteniendo accesos actuales del empleado: {e}")
            return []

    # ==============================
    # MÉTODOS DE LÓGICA DE NEGOCIO
    # ==============================

    def update_employee_status(self, scotia_id: str, active: bool) -> Tuple[bool, str]:
        """Actualiza el estado activo/inactivo de un empleado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar que el empleado existe
            cursor.execute('SELECT COUNT(*) FROM headcount WHERE scotia_id = ?', (scotia_id,))
            result = cursor.fetchone()
            if not result or result[0] == 0:
                conn.close()
                return False, f"Empleado {scotia_id} no encontrado"
            
            # Actualizar estado
            if active:
                cursor.execute('''
                    UPDATE headcount 
                    SET activo = 1, inactivation_date = NULL
                    WHERE scotia_id = ?
                ''', (scotia_id,))
                status_text = "activo"
            else:
                cursor.execute('''
                    UPDATE headcount 
                    SET activo = 0, inactivation_date = ?
                    WHERE scotia_id = ?
                ''', (datetime.now().isoformat(), scotia_id))
                status_text = "inactivo"
            
            conn.commit()
            conn.close()
            
            return True, f"Estado del empleado {scotia_id} cambiado a {status_text}"
            
        except Exception as e:
            return False, f"Error actualizando estado del empleado: {str(e)}"

    def process_employee_onboarding(self, scotia_id: str, position: str, unit: str, 
                                   responsible: str = "Sistema",
                                   subunit: Optional[str] = None) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa el onboarding de un empleado y determina qué accesos necesita.
        Crea registros por cada app que coincida con (unit, subunit?, position_role) **sin duplicados**.
        Actualiza la posición y unidad del empleado si están vacías.
        Cambia el estado del empleado de inactivo a activo automáticamente.
        """
        try:
            # 1. Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []

            # 2. Actualizar estado del empleado a activo
            success, message = self.update_employee_status(scotia_id, True)
            if success:
                print(f"✅ {message}")
            else:
                print(f"⚠️ {message}")

            # 3. Actualizar posición y unidad del empleado si están vacías
            current_position = employee.get('position', '').strip()
            current_unit = employee.get('unit', '').strip()
            
            if not current_position or not current_unit:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE headcount 
                    SET position = ?, unit = ?
                    WHERE scotia_id = ?
                ''', (position, unit, scotia_id))
                conn.commit()
                conn.close()
                print(f"✅ Posición y unidad actualizadas para {scotia_id}")

            # 4. Obtener aplicaciones requeridas para la posición (ya sin duplicados por clave)
            required_apps = self.get_applications_by_position(position, unit, subunit=subunit)
            if not required_apps:
                return False, f"No se encontraron aplicaciones para la posición {position} en {unit}", []

            # 5. Crear registros históricos para cada aplicación (dedupe por tripleta normalizada)
            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{scotia_id}"
            created_records = []
            seen_triplets = set()

            for app in required_apps:
                unit_n = (app.get('unit') or '').strip().upper()
                pos_n = (app.get('position_role') or '').strip().upper()
                lan_n = (app.get('logical_access_name') or '').strip().upper()

                tkey = (unit_n, pos_n, lan_n)
                if tkey in seen_triplets:
                    continue
                seen_triplets.add(tkey)

                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'onboarding',
                    'sid': scotia_id,
                    'area': app.get('unit'),
                    'subunit': app.get('subunit') or '',  # ya no afecta dedupe
                    'event_description': f"Otorgamiento de acceso para {app.get('logical_access_name')}",
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
        """Procesa el offboarding de un empleado (revoca todo lo que figure completado)."""
        try:
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []

            history = self.get_employee_history(scotia_id)
            # Considerar TODOS los accesos de onboarding y lateral_movement, independientemente del estado
            active_access = [h for h in history if h.get('process_access') in ('onboarding', 'lateral_movement')]

            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []

            for access in active_access:
                app_name = access.get('app_access_name') or access.get('app_logical_access_name')
                
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'offboarding',
                    'sid': scotia_id,
                    'area': 'out of the company',  # Área fija para offboarding
                    'subunit': 'out of the company',  # Subárea fija para offboarding
                    'event_description': f"Revocación de acceso para {app_name}",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': app_name,
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }

                success, message = self.create_historical_record(record_data)
                if success:
                    created_records.append(record_data)
                else:
                    print(f"Error creando registro de offboarding para {app_name}: {message}")

            # Marcar empleado como inactivo y registrar fecha de inactivación
            conn = self.get_connection()
            cursor = conn.cursor()
            inactivation_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                UPDATE headcount 
                SET activo = 0, inactivation_date = ? 
                WHERE scotia_id = ?
            ''', (inactivation_date, scotia_id))
            conn.commit()
            conn.close()

            return True, f"Offboarding procesado para {scotia_id}. {len(created_records)} accesos a revocar.", created_records

        except Exception as e:
            return False, f"Error procesando offboarding: {str(e)}", []

    def process_lateral_movement(self, scotia_id: str, new_position: str, new_unit: str, 
                                responsible: str = "Sistema", new_subunit: Optional[str] = None) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa un movimiento lateral: revoca accesos de posición anterior y otorga nuevos.
        
        Lógica mejorada:
        - REVOCA solo accesos específicos de la posición anterior que no son necesarios en la nueva
        - OTORGA nuevos accesos de la nueva posición
        - Evita duplicados comparando por logical_access_name y unidad
        """
        try:
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []

            old_position = (employee.get('position') or '').strip()
            old_unit = (employee.get('unit') or '').strip()

            # Obtener accesos actuales del empleado (solo los de la posición anterior)
            current_access = self.get_employee_current_access(scotia_id)
            
            # Obtener accesos requeridos para la nueva posición
            new_mesh_apps = self.get_applications_by_position(new_position, new_unit, subunit=new_subunit)
            
            # Crear índices para comparación más inteligente
            current_apps_by_name = {}
            for acc in current_access:
                app_name = acc.get('logical_access_name', '')
                unit = acc.get('unit', '')
                key = f"{app_name}_{unit}"
                current_apps_by_name[key] = acc
            
            new_apps_by_name = {}
            for app in new_mesh_apps:
                app_name = app.get('logical_access_name', '')
                unit = app.get('unit', '')
                key = f"{app_name}_{unit}"
                new_apps_by_name[key] = app

            # Calcular qué revocar y qué otorgar
            to_revoke = []
            to_grant = []
            
            # Revocar accesos de la posición anterior que no están en la nueva posición
            for key, acc in current_apps_by_name.items():
                if key not in new_apps_by_name:
                    to_revoke.append(acc)
            
            # Otorgar accesos de la nueva posición que no tiene actualmente
            for key, app in new_apps_by_name.items():
                if key not in current_apps_by_name:
                    to_grant.append(app)

            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []

            # 1. REVOCAR accesos de la posición anterior que ya no son necesarios
            for acc in to_revoke:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'offboarding',
                    'sid': scotia_id,
                    'area': acc.get('unit', ''),
                    'subunit': acc.get('subunit', ''),
                    'event_description': f"Revocación de acceso para {acc.get('logical_access_name', '')} (lateral movement - cambio de posición)",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': acc.get('logical_access_name', ''),
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                ok, _ = self.create_historical_record(record_data)
                if ok:
                    created_records.append(record_data)

            # 2. OTORGAR nuevos accesos de la nueva posición
            for app in to_grant:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'onboarding',
                    'sid': scotia_id,
                    'area': app.get('unit', ''),
                    'subunit': app.get('subunit', ''),
                    'event_description': f"Otorgamiento de acceso para {app.get('logical_access_name', '')} (lateral movement - nueva posición)",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': app.get('logical_access_name', ''),
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                ok, _ = self.create_historical_record(record_data)
                if ok:
                    created_records.append(record_data)

            # Actualizar posición/unidad del empleado
            success, message = self.update_employee_position(scotia_id, new_position, new_unit)
            if not success:
                return False, f"Error actualizando posición: {message}", []

            return True, (
                f"Movimiento lateral procesado para {scotia_id}. "
                f"{len(to_revoke)} accesos revocados (posición anterior), {len(to_grant)} accesos otorgados (nueva posición)."), created_records

        except Exception as e:
            return False, f"Error procesando movimiento lateral: {str(e)}", []

    def get_access_reconciliation_report(self, scotia_id: str) -> Dict[str, Any]:
        """Genera un reporte de conciliación mejorado que maneja mejor los cambios de posición."""
        try:
            # 1) Empleado
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return {"error": f"Empleado {scotia_id} no encontrado"}

            emp_unit = (employee.get('unit') or '').strip()
            emp_position = (employee.get('position') or '').strip()
            
            # 2) Obtener subunit del empleado desde el historial más reciente
            # o usar un valor por defecto si no hay historial
            history = self.get_employee_history(scotia_id)
            emp_subunit = ''
            if history:
                # Buscar el subunit más reciente del historial
                for h in history:
                    if h.get('area') == emp_unit and h.get('subunit'):
                        emp_subunit = h.get('subunit', '').strip()
                        break
            
            # Si no encontramos subunit, usar un valor por defecto basado en la unidad
            if not emp_subunit:
                emp_subunit = 'General'  # Valor por defecto

            # 3) Requeridos por malla de apps para la posición/unidad del empleado
            # Solo buscar por unit y position_role (comparación estricta)
            required_apps = self.get_applications_by_position(
                position=emp_position,
                unit=emp_unit,
                subunit=None,  # No filtrar por subunit para ser más inclusivo
                title=None,    # No tenemos title del empleado
            )

            # Filtrar aplicaciones que coincidan exactamente con unit y position_role
            filtered_required_apps = []
            for app in required_apps:
                app_unit = app.get('unit', '').strip()
                app_position = app.get('position_role', '').strip()
                
                # Solo incluir si coincide exactamente con unit y position
                if app_unit == emp_unit and app_position == emp_position:
                    filtered_required_apps.append(app)

            # Claves requeridas - usar tripleta normalizada: unit, position_role, logical_access_name (ignora subunit)
            required_keys = {
                self._triplet_key(app.get('unit'), app.get('position_role'), app.get('logical_access_name'))
                for app in filtered_required_apps
            }

            # Índice para detalles usando la misma clave normalizada
            req_index = {
                self._triplet_key(app.get('unit'), app.get('position_role'), app.get('logical_access_name')): app
                for app in filtered_required_apps
            }

            # 4) Historial/actuales: considerar registros de la unidad actual
            # MEJORA: Considerar todos los accesos de onboarding como actuales
            # Esto evita que aparezcan como "onboarding" cuando se cambia de unidad
            current_records = []
            for h in history:
                if h.get('process_access') in ('onboarding', 'lateral_movement'):
                    hist_unit = h.get('app_unit') or h.get('area', '')
                    hist_position = h.get('app_position_role') or h.get('position', '')
                    hist_name = h.get('app_logical_access_name') or h.get('app_access_name', '')
                    
                    # Considerar todos los registros de onboarding, independientemente de la unidad
                    if hist_name:
                        # Si no hay posición en el historial, usar la posición actual
                        if not hist_position:
                            hist_position = emp_position
                        
                        # Agregar el registro con la posición actualizada si es necesario
                        h_updated = h.copy()
                        h_updated['app_position_role'] = hist_position
                        h_updated['app_unit'] = hist_unit
                        h_updated['app_logical_access_name'] = hist_name
                        current_records.append(h_updated)

            # Claves actuales - usar tripleta normalizada: unit, position_role, logical_access_name (ignora subunit)
            # MEJORA: Considerar accesos de todas las unidades, pero normalizar posiciones
            current_keys = set()
            for h in current_records:
                app_unit = h.get('app_unit') or h.get('area', '')
                app_position = h.get('app_position_role') or h.get('position', '')
                app_name = h.get('app_logical_access_name') or h.get('app_access_name', '')
                
                # Si no hay position en el historial, usar la posición actual del empleado
                if not app_position:
                    app_position = emp_position
                
                # MEJORA: Si la posición del historial es diferente a la actual, 
                # usar la posición actual para la comparación (esto evita falsos positivos)
                if app_position != emp_position:
                    app_position = emp_position
                
                # Considerar todos los accesos, independientemente de la unidad
                if app_position and app_name:
                    current_keys.add(self._triplet_key(app_unit, app_position, app_name))

            # 4) Deltas estrictos por clave completa
            to_grant_keys = required_keys - current_keys
            to_revoke_keys = current_keys - required_keys

            # 5) Construcción de listas detalladas
            to_grant: List[Dict[str, Any]] = []
            for key in to_grant_keys:
                app = req_index.get(key, {})
                to_grant.append({
                    'unit': key[0],
                    'subunit': app.get('subunit', ''),  # subunit del app original
                    'position_role': key[1],
                    'app_name': key[2],
                    'role_name': app.get('role_name', ''),
                    'description': app.get('description', ''),
                })

            to_revoke: List[Dict[str, Any]] = []
            # Para revocar, buscamos el primer record que matchee esa clave para dar contexto (fecha, etc.)
            rec_index = {}
            for h in current_records:
                app_unit = h.get('app_unit') or h.get('area', '')
                app_position = h.get('app_position_role') or h.get('position', '')
                app_name = h.get('app_logical_access_name') or h.get('app_access_name', '')
                
                # Si no hay position en el historial, usar la posición actual del empleado
                if not app_position:
                    app_position = emp_position
                
                if app_unit and app_position and app_name:
                    key = self._triplet_key(app_unit, app_position, app_name)
                    rec_index[key] = h
            for key in to_revoke_keys:
                h = rec_index.get(key, {})
                to_revoke.append({
                    'unit': key[0],
                    'subunit': h.get('app_subunit', '') or h.get('subunit', ''),  # subunit del historial
                    'position_role': key[1],
                    'app_name': key[2],
                    'granted_date': h.get('record_date', ''),
                    'status': h.get('status', ''),
                })

            # 6) Construir lista de actuales deduplicada usando tripleta normalizada
            current_access: List[Dict[str, Any]] = []
            seen_keys = set()
            for h in current_records:
                # Solo agregar si coincide con la unidad actual del empleado
                if h.get('area') == emp_unit:
                    app_unit = h.get('app_unit') or h.get('area', '')
                    app_position = h.get('app_position_role') or h.get('position', '')
                    app_name = h.get('app_logical_access_name') or h.get('app_access_name', '')
                    
                    # Si no hay position en el historial, usar la posición actual del empleado
                    if not app_position:
                        app_position = emp_position
                    
                    if app_unit and app_position and app_name:
                        key = self._triplet_key(app_unit, app_position, app_name)
                        if key not in seen_keys:
                            seen_keys.add(key)
                            current_access.append({
                                'unit': key[0],
                                'subunit': h.get('app_subunit', '') or h.get('subunit', ''),  # subunit del historial
                                'position_role': key[1],
                                'app_name': key[2],
                                'granted_date': h.get('record_date'),
                                'status': h.get('status'),
                            })

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

    def delete_historical_record(self, scotia_id: str, case_id: str, app_access_name: str = None) -> bool:
        """Elimina un registro específico del historial por scotia_id, case_id y app_access_name"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Si se proporciona app_access_name, eliminar solo ese registro específico
                if app_access_name:
                    cursor.execute('SELECT id FROM historico WHERE scotia_id = ? AND case_id = ? AND app_access_name = ?', (scotia_id, case_id, app_access_name))
                    
                    if not cursor.fetchone():
                        return False
                    
                    # Eliminar solo el registro específico
                    cursor.execute(
                        "DELETE FROM historico WHERE scotia_id = ? AND case_id = ? AND app_access_name = ?",
                        (scotia_id, case_id, app_access_name)
                    )
                else:
                    # Si no se proporciona app_access_name, eliminar solo el primer registro encontrado
                    cursor.execute('SELECT TOP 1 id FROM historico WHERE scotia_id = ? AND case_id = ?', (scotia_id, case_id))
                    
                    if not cursor.fetchone():
                        return False
                    
                    # Eliminar solo el primer registro
                    cursor.execute(
                        "DELETE FROM historico WHERE scotia_id = ? AND case_id = ? LIMIT 1",
                        (scotia_id, case_id)
                    )
                
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error eliminando registro: {str(e)}")
            return False

    def get_headcount_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del headcount agrupadas por diferentes criterios"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            stats = {}
            
            # 1. Estadísticas por unidad
            cursor.execute('''
                SELECT unit as unidad, COUNT(*) as total_empleados,
                       COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                       COUNT(CASE WHEN activo = 0 THEN 1 END) as inactivos,
                       COUNT(CASE WHEN position IS NOT NULL AND position != '' THEN 1 END) as con_posicion,
                       COUNT(CASE WHEN start_date IS NOT NULL AND start_date != '' THEN 1 END) as con_fecha_inicio
                FROM headcount
                WHERE unit IS NOT NULL AND unit != ''
                GROUP BY unit
                ORDER BY total_empleados DESC
            ''')
            stats['por_unidad'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 2. Estadísticas por puesto
            cursor.execute('''
                SELECT position as puesto, unit as unidad, COUNT(*) as total_empleados,
                       COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                       COUNT(CASE WHEN activo = 0 THEN 1 END) as inactivos,
                       COUNT(CASE WHEN start_date IS NOT NULL AND start_date != '' THEN 1 END) as con_fecha_inicio
                FROM headcount
                WHERE position IS NOT NULL AND position != ''
                GROUP BY position, unit
                ORDER BY total_empleados DESC
            ''')
            stats['por_puesto'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 3. Estadísticas por manager
            cursor.execute('''
                SELECT manager, unit as unidad, COUNT(*) as total_empleados,
                       COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                       COUNT(CASE WHEN activo = 0 THEN 1 END) as inactivos
                FROM headcount
                WHERE manager IS NOT NULL AND manager != ''
                GROUP BY manager, unit
                ORDER BY total_empleados DESC
            ''')
            stats['por_manager'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 4. Estadísticas por senior manager
            cursor.execute('''
                SELECT senior_manager, unit as unidad, COUNT(*) as total_empleados,
                       COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                       COUNT(CASE WHEN activo = 0 THEN 1 END) as inactivos
                FROM headcount
                WHERE senior_manager IS NOT NULL AND senior_manager != ''
                GROUP BY senior_manager, unit
                ORDER BY total_empleados DESC
            ''')
            stats['por_senior_manager'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 5. Estadísticas por estado de activación
            cursor.execute('''
                SELECT 
                    CASE WHEN activo = 1 THEN 'Activo' ELSE 'Inactivo' END as estado,
                    COUNT(*) as total_empleados,
                    COUNT(CASE WHEN inactivation_date IS NOT NULL THEN 1 END) as con_fecha_inactivacion
                FROM headcount
                GROUP BY activo
                ORDER BY activo DESC
            ''')
            stats['por_estado'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 6. Estadísticas por año de inicio (si hay fecha de inicio)
            cursor.execute('''
                SELECT 
                    SUBSTR(start_date, 1, 4) as año_inicio,
                    COUNT(*) as total_empleados,
                    COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                    COUNT(CASE WHEN activo = 0 THEN 1 END) as inactivos
                FROM headcount
                WHERE start_date IS NOT NULL AND start_date != '' 
                AND LENGTH(start_date) >= 4
                GROUP BY SUBSTR(start_date, 1, 4)
                ORDER BY año_inicio DESC
            ''')
            stats['por_año_inicio'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 7. Resumen detallado por unidad (con lista de empleados)
            cursor.execute('''
                SELECT 
                    unit as unidad,
                    scotia_id,
                    full_name,
                    position as puesto,
                    manager,
                    senior_manager,
                    CASE WHEN activo = 1 THEN 'Activo' ELSE 'Inactivo' END as estado,
                    start_date,
                    inactivation_date
                FROM headcount
                WHERE unit IS NOT NULL AND unit != ''
                ORDER BY unit, full_name
            ''')
            stats['detalle_por_unidad'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 8. Estadísticas generales
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_empleados,
                    COUNT(CASE WHEN activo = 1 THEN 1 END) as activos,
                    COUNT(CASE WHEN activo = 0 THEN 1 END) as inactivos,
                    COUNT(CASE WHEN position IS NOT NULL AND position != '' THEN 1 END) as con_posicion,
                    COUNT(CASE WHEN start_date IS NOT NULL AND start_date != '' THEN 1 END) as con_fecha_inicio,
                    COUNT(CASE WHEN manager IS NOT NULL AND manager != '' THEN 1 END) as con_manager,
                    COUNT(CASE WHEN senior_manager IS NOT NULL AND senior_manager != '' THEN 1 END) as con_senior_manager,
                    COUNT(CASE WHEN inactivation_date IS NOT NULL THEN 1 END) as con_fecha_inactivacion
                FROM headcount
            ''')
            stats['generales'] = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
            
            conn.close()
            return stats
            
        except Exception as e:
            return {"error": f"Error obteniendo estadísticas del headcount: {str(e)}"}

    def get_available_applications(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de aplicaciones disponibles para registros manuales"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener aplicaciones únicas del historial y de la tabla applications
            cursor.execute('''
                SELECT DISTINCT app_access_name as application_name
                FROM historico 
                WHERE app_access_name IS NOT NULL AND app_access_name != ''
                UNION
                SELECT DISTINCT logical_access_name as application_name
                FROM applications 
                WHERE logical_access_name IS NOT NULL AND logical_access_name != ''
                ORDER BY application_name
            ''')
            
            applications = [{'name': row[0]} for row in cursor.fetchall()]
            conn.close()
            
            return applications
            
        except Exception as e:
            return []

    def get_historial_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del historial agrupadas por diferentes criterios"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            stats = {}
            
            # 1. Estadísticas por unidad
            cursor.execute('''
                SELECT h.area as unidad, COUNT(*) as total_registros,
                       COUNT(CASE WHEN h.status = 'Completado' THEN 1 END) as completados,
                       COUNT(CASE WHEN h.status = 'Pendiente' THEN 1 END) as pendientes,
                       COUNT(CASE WHEN h.status = 'En Proceso' THEN 1 END) as en_proceso,
                       COUNT(CASE WHEN h.status = 'Cancelado' THEN 1 END) as cancelados,
                       COUNT(CASE WHEN h.status = 'Rechazado' THEN 1 END) as rechazados
                FROM historico h
                WHERE h.area IS NOT NULL AND h.area != ''
                GROUP BY h.area
                ORDER BY total_registros DESC
            ''')
            stats['por_unidad'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 2. Estadísticas por subunidad
            cursor.execute('''
                SELECT h.subunit as subunidad, h.area as unidad, COUNT(*) as total_registros,
                       COUNT(CASE WHEN h.status = 'Completado' THEN 1 END) as completados,
                       COUNT(CASE WHEN h.status = 'Pendiente' THEN 1 END) as pendientes,
                       COUNT(CASE WHEN h.status = 'En Proceso' THEN 1 END) as en_proceso,
                       COUNT(CASE WHEN h.status = 'Cancelado' THEN 1 END) as cancelados,
                       COUNT(CASE WHEN h.status = 'Rechazado' THEN 1 END) as rechazados
                FROM historico h
                WHERE h.subunit IS NOT NULL AND h.subunit != ''
                GROUP BY h.subunit, h.area
                ORDER BY total_registros DESC
            ''')
            stats['por_subunidad'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 3. Estadísticas por puesto
            cursor.execute('''
                SELECT head.position as puesto, head.unit as unidad, COUNT(*) as total_registros,
                       COUNT(CASE WHEN h.status = 'Completado' THEN 1 END) as completados,
                       COUNT(CASE WHEN h.status = 'Pendiente' THEN 1 END) as pendientes,
                       COUNT(CASE WHEN h.status = 'En Proceso' THEN 1 END) as en_proceso,
                       COUNT(CASE WHEN h.status = 'Cancelado' THEN 1 END) as cancelados,
                       COUNT(CASE WHEN h.status = 'Rechazado' THEN 1 END) as rechazados
                FROM historico h
                INNER JOIN headcount head ON h.scotia_id = head.scotia_id
                WHERE head.position IS NOT NULL AND head.position != ''
                GROUP BY head.position, head.unit
                ORDER BY total_registros DESC
            ''')
            stats['por_puesto'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 4. Estadísticas por aplicación
            cursor.execute('''
                SELECT h.app_access_name as aplicacion, COUNT(*) as total_registros,
                       COUNT(CASE WHEN h.status = 'Completado' THEN 1 END) as completados,
                       COUNT(CASE WHEN h.status = 'Pendiente' THEN 1 END) as pendientes,
                       COUNT(CASE WHEN h.status = 'En Proceso' THEN 1 END) as en_proceso,
                       COUNT(CASE WHEN h.status = 'Cancelado' THEN 1 END) as cancelados,
                       COUNT(CASE WHEN h.status = 'Rechazado' THEN 1 END) as rechazados
                FROM historico h
                WHERE h.app_access_name IS NOT NULL AND h.app_access_name != ''
                GROUP BY h.app_access_name
                ORDER BY total_registros DESC
            ''')
            stats['por_aplicacion'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 5. Estadísticas por proceso
            cursor.execute('''
                SELECT h.process_access as proceso, COUNT(*) as total_registros,
                       COUNT(CASE WHEN h.status = 'Completado' THEN 1 END) as completados,
                       COUNT(CASE WHEN h.status = 'Pendiente' THEN 1 END) as pendientes,
                       COUNT(CASE WHEN h.status = 'En Proceso' THEN 1 END) as en_proceso,
                       COUNT(CASE WHEN h.status = 'Cancelado' THEN 1 END) as cancelados,
                       COUNT(CASE WHEN h.status = 'Rechazado' THEN 1 END) as rechazados
                FROM historico h
                WHERE h.process_access IS NOT NULL AND h.process_access != ''
                GROUP BY h.process_access
                ORDER BY total_registros DESC
            ''')
            stats['por_proceso'] = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            
            # 6. Estadísticas generales
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_registros,
                    COUNT(CASE WHEN h.status = 'Completado' THEN 1 END) as completados,
                    COUNT(CASE WHEN h.status = 'Pendiente' THEN 1 END) as pendientes,
                    COUNT(CASE WHEN h.status = 'En Proceso' THEN 1 END) as en_proceso,
                    COUNT(CASE WHEN h.status = 'Cancelado' THEN 1 END) as cancelados,
                    COUNT(CASE WHEN h.status = 'Rechazado' THEN 1 END) as rechazados
                FROM historico h
            ''')
            stats['generales'] = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
            
            conn.close()
            return stats
            
        except Exception as e:
            return {"error": f"Error obteniendo estadísticas: {str(e)}"}

    def buscar_procesos(self, filtros: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Busca procesos en el historial con filtros opcionales.
        
        Args:
            filtros: Diccionario con filtros de búsqueda
            
        Returns:
            Lista de registros del historial que coinciden con los filtros
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Query base
            query = '''
                SELECT h.*, a.logical_access_name, a.description as app_description
                FROM historico h
                LEFT JOIN (
                    SELECT 
                        logical_access_name,
                        description,
                        ROW_NUMBER() OVER (PARTITION BY logical_access_name ORDER BY id) as rn
                    FROM applications
                ) a ON h.app_access_name = a.logical_access_name AND a.rn = 1
            '''
            
            # Construir WHERE clause basado en filtros
            where_conditions = []
            params = []
            
            if filtros:
                for campo, valor in filtros.items():
                    if valor and valor.strip():
                        if campo == 'numero_caso':
                            where_conditions.append("h.case_id LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'sid':
                            where_conditions.append("h.scotia_id LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'proceso':
                            where_conditions.append("h.process_access LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'aplicacion':
                            where_conditions.append("h.app_access_name LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'estado':
                            where_conditions.append("h.status LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'fecha':
                            where_conditions.append("h.record_date LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'responsable':
                            where_conditions.append("h.responsible LIKE ?")
                            params.append(f"%{valor}%")
                        elif campo == 'descripcion':
                            where_conditions.append("h.event_description LIKE ?")
                            params.append(f"%{valor}%")
            
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            
            query += " ORDER BY h.record_date DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            # Convertir a diccionarios
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
            
        except Exception as e:
            print(f"Error en buscar_procesos: {e}")
            return []

    def assign_accesses(self, scotia_id: str, responsable: str = "Sistema") -> Tuple[bool, str, Dict[str, int]]:
        """
        Asigna accesos automáticamente según la unit y position del empleado.
        
        Args:
            scotia_id: ID del empleado
            responsable: Responsable del proceso (default: "Sistema")
            
        Returns:
            Tuple[bool, str, Dict[str, int]]: (success, message, counts)
            counts contiene: {'granted': int, 'revoked': int}
        """
        try:
            # Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", {'granted': 0, 'revoked': 0}
            
            # Verificar si ya hay registros pendientes para este empleado
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM historico WHERE scotia_id = ? AND status = \'Pendiente\'', (scotia_id,))
            existing_pending = cursor.fetchone()[0]
            
            if existing_pending > 0:
                conn.close()
                return False, f"Ya existen {existing_pending} registros pendientes para {scotia_id}. Complete los procesos pendientes antes de crear nuevos.", {'granted': 0, 'revoked': 0}
            
            # Obtener reporte de conciliación usando el procedimiento almacenado
            reconciliation_report = self.get_access_reconciliation_report(scotia_id)
            
            if not reconciliation_report.get('success', False):
                return False, reconciliation_report.get('message', 'Error obteniendo reporte de conciliación'), {'granted': 0, 'revoked': 0}
            
            data = reconciliation_report.get('data', {})
            to_grant = data.get('to_grant', [])
            to_revoke = data.get('to_revoke', [])
            
            # Contadores
            granted_count = 0
            revoked_count = 0
            
            # Generar un solo case_id para todo el proceso
            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            
            # Procesar accesos por otorgar
            for access_data in to_grant:
                app_name = access_data.get('app_name', '')
                if app_name:
                    # Crear registro histórico para otorgamiento
                    record_data = {
                        'scotia_id': scotia_id,
                        'case_id': case_id,
                        'responsible': responsable,
                        'process_access': 'onboarding',
                        'sid': scotia_id,
                        'area': access_data.get('unit', ''),
                        'subunit': access_data.get('subunit', ''),
                        'event_description': f"Otorgamiento automático de acceso para {app_name}",
                        'ticket_email': f"{responsable}@empresa.com",
                        'app_access_name': app_name,
                        'computer_system_type': 'Desktop',
                        'status': 'Pendiente',
                        'general_status': 'En Proceso'
                    }
                    
                    success, message = self.create_historical_record(record_data)
                    if success:
                        granted_count += 1
                    else:
                        print(f"Error creando registro de otorgamiento: {message}")
            
            # Procesar accesos por revocar
            for access_data in to_revoke:
                app_name = access_data.get('app_name', '')
                if app_name:
                    # Crear registro histórico para revocación
                    record_data = {
                        'scotia_id': scotia_id,
                        'case_id': case_id,
                        'responsible': responsable,
                        'process_access': 'offboarding',
                        'sid': scotia_id,
                        'area': access_data.get('unit', ''),
                        'subunit': access_data.get('subunit', ''),
                        'event_description': f"Revocación automática de acceso para {app_name}",
                        'ticket_email': f"{responsable}@empresa.com",
                        'app_access_name': app_name,
                        'computer_system_type': 'Desktop',
                        'status': 'Pendiente',
                        'general_status': 'En Proceso'
                    }
                    
                    success, message = self.create_historical_record(record_data)
                    if success:
                        revoked_count += 1
                    else:
                        print(f"Error creando registro de revocación: {message}")
            
            conn.close()
            
            counts = {'granted': granted_count, 'revoked': revoked_count}
            message = f"Proceso completado. Otorgados: {granted_count}, Revocados: {revoked_count}"
            
            return True, message, counts
            
        except Exception as e:
            return False, f"Error en assign_accesses: {str(e)}", {'granted': 0, 'revoked': 0}

    def get_access_reconciliation_report(self, scotia_id: str) -> Dict[str, Any]:
        """Obtiene el reporte de conciliación de accesos para un empleado usando procedimiento almacenado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Ejecutar procedimiento almacenado
            cursor.execute("EXEC sp_GetAccessReconciliationReport ?", (scotia_id,))
            results = cursor.fetchall()
            
            if not results:
                return {
                    'success': False,
                    'message': f'No se encontraron datos para el empleado {scotia_id}',
                    'data': {}
                }
            
            # Verificar si hay error
            first_row = results[0]
            if len(first_row) >= 2 and first_row[0] == 'error':
                return {
                    'success': False,
                    'message': first_row[1],
                    'data': {}
                }
            
            # Procesar resultados
            current_access = []
            to_grant = []
            to_revoke = []
            
            for row in results:
                access_type = row[0]
                app_name = row[1]
                unit = row[2]
                subunit = row[3]
                position_role = row[4]
                role_name = row[5]
                description = row[6]
                record_date = row[7]
                status = row[8]
                
                access_data = {
                    'app_name': app_name,
                    'unit': unit,
                    'subunit': subunit,
                    'position_role': position_role,
                    'role_name': role_name,
                    'description': description,
                    'status': status
                }
                
                if access_type == 'current':
                    access_data['date'] = record_date
                    current_access.append(access_data)
                elif access_type == 'to_grant':
                    to_grant.append(access_data)
                elif access_type == 'to_revoke':
                    access_data['date'] = record_date
                    to_revoke.append(access_data)
            
            # Obtener información del empleado
            employee = self.get_employee_by_id(scotia_id)
            
            conn.close()
            
            return {
                'success': True,
                'message': f'Reporte de conciliación generado para {scotia_id}',
                'data': {
                    'employee': employee,
                    'current_access': current_access,
                    'to_grant': to_grant,
                    'to_revoke': to_revoke,
                    'summary': {
                        'current_count': len(current_access),
                        'to_grant_count': len(to_grant),
                        'to_revoke_count': len(to_revoke),
                        'final_count': len(current_access) + len(to_grant) - len(to_revoke)
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error generando reporte de conciliación: {str(e)}',
                'data': {}
            }


# Instancia global del servicio
access_service = AccessManagementService()
