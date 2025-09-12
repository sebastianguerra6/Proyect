"""
Servicio para gestionar la lógica de negocio entre las tablas:
- headcount (personas)
- applications (aplicaciones y accesos)
- historico (historial de procesos)

Cambios clave:
- Reconciliación estricta por (unit, subunit, position_role, logical_access_name).
- Nuevas utilidades para construir claves de acceso y comparar conjuntos.
- get_employee_history ahora trae unit/subunit/position_role de la app para poder comparar correctamente.
- process_lateral_movement y get_access_reconciliation_report usan la clave completa para decidir mantener/quitar/otorgar.
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

        except sqlite3.IntegrityError:
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

            # Construir condiciones WHERE con normalización
            where_conditions = [
                "UPPER(TRIM(position_role)) = UPPER(TRIM(?))",
                "UPPER(TRIM(unit)) = UPPER(TRIM(?))"
            ]
            params = [position, unit]

            if subunit is not None and subunit != '':
                where_conditions.append("UPPER(TRIM(subunit)) = UPPER(TRIM(?))")
                params.append(subunit)

            if title is not None and title != '':
                where_conditions.append("UPPER(TRIM(role_name)) = UPPER(TRIM(?))")
                params.append(title)

            # Query principal con deduplicación por tripleta normalizada
            query = f"""
                SELECT 
                    a.logical_access_name, a.jurisdiction, a.unit, a.subunit, 
                    a.alias, a.path_email_url, a.position_role, a.exception_tracking, 
                    a.fulfillment_action, a.system_owner, a.role_name, a.access_type, 
                    a.category, a.additional_data, a.ad_code, a.access_status, 
                    a.last_update_date, a.require_licensing, a.description, 
                    a.authentication_method
                FROM applications a
                WHERE {' AND '.join(where_conditions)}
                GROUP BY 
                    UPPER(TRIM(a.unit)), 
                    UPPER(TRIM(a.position_role)), 
                    UPPER(TRIM(a.logical_access_name))
                ORDER BY a.logical_access_name
            """

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

    def debug_applications_by_position(self, position: str, unit: str, subunit: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
        """Método de debug para verificar la deduplicación de aplicaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Query sin deduplicación para comparar
            where_conditions = [
                "UPPER(TRIM(position_role)) = UPPER(TRIM(?))",
                "UPPER(TRIM(unit)) = UPPER(TRIM(?))"
            ]
            params = [position, unit]

            if subunit is not None and subunit != '':
                where_conditions.append("UPPER(TRIM(subunit)) = UPPER(TRIM(?))")
                params.append(subunit)

            if title is not None and title != '':
                where_conditions.append("UPPER(TRIM(role_name)) = UPPER(TRIM(?))")
                params.append(title)

            # Query sin GROUP BY para ver duplicados
            query_all = f"""
                SELECT 
                    a.logical_access_name, a.unit, a.subunit, a.position_role,
                    UPPER(TRIM(a.unit)) as unit_norm,
                    UPPER(TRIM(a.position_role)) as pos_norm,
                    UPPER(TRIM(a.logical_access_name)) as app_norm
                FROM applications a
                WHERE {' AND '.join(where_conditions)}
                ORDER BY a.logical_access_name
            """

            cursor.execute(query_all, params)
            all_rows = cursor.fetchall()

            # Query con GROUP BY para ver deduplicados
            query_dedup = f"""
                SELECT 
                    a.logical_access_name, a.unit, a.subunit, a.position_role,
                    UPPER(TRIM(a.unit)) as unit_norm,
                    UPPER(TRIM(a.position_role)) as pos_norm,
                    UPPER(TRIM(a.logical_access_name)) as app_norm
                FROM applications a
                WHERE {' AND '.join(where_conditions)}
                GROUP BY 
                    UPPER(TRIM(a.unit)), 
                    UPPER(TRIM(a.position_role)), 
                    UPPER(TRIM(a.logical_access_name))
                ORDER BY a.logical_access_name
            """

            cursor.execute(query_dedup, params)
            dedup_rows = cursor.fetchall()

            conn.close()

            return {
                "total_without_dedup": len(all_rows),
                "total_with_dedup": len(dedup_rows),
                "all_rows": all_rows,
                "dedup_rows": dedup_rows,
                "duplicates_found": len(all_rows) - len(dedup_rows)
            }

        except Exception as e:
            print(f"Error en debug: {e}")
            return {"error": str(e)}

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

            cursor.execute('''
                INSERT INTO applications 
                (jurisdiction, unit, subunit, logical_access_name, alias, path_email_url, position_role, 
                 exception_tracking, fulfillment_action, system_owner, role_name, access_type, 
                 category, additional_data, ad_code, access_status, last_update_date, 
                 require_licensing, description, authentication_method)
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

            app_id = cursor.lastrowid

            conn.commit()
            conn.close()

            return True, f"Aplicación {app_data.get('logical_access_name')} creada exitosamente con ID {app_id}"

        except sqlite3.IntegrityError:
            return False, "Error de integridad: La aplicación ya existe"
        except Exception as e:
            return False, f"Error creando aplicación: {str(e)}"

    def update_application(self, app_id: int, app_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualiza una aplicación existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM applications WHERE id = ?', (app_id,))
            if not cursor.fetchone():
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
            cursor.execute('''
                SELECT 1 FROM historico
                WHERE scotia_id = ?
                  AND process_access IN ('onboarding','offboarding')
                  AND status = 'Pendiente'
                  AND UPPER(TRIM(app_access_name)) = UPPER(TRIM(?))
                  AND UPPER(TRIM(COALESCE(area,''))) = UPPER(TRIM(COALESCE(?,'')))
                  -- si deseas ignorar subunit en la duplicidad, comenta esta línea:
                  AND UPPER(TRIM(COALESCE(subunit,''))) = UPPER(TRIM(COALESCE(?,'')))
                LIMIT 1
            ''', (record_data['scotia_id'], record_data.get('app_access_name', ''),
                  record_data.get('area',''), record_data.get('subunit','')))
            
            if cursor.fetchone():
                conn.close()
                return True, "Registro ya pendiente; no se duplicó"

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
                    a.description         AS app_description,
                    a.unit                AS app_unit,
                    a.subunit             AS app_subunit,
                    a.position_role       AS app_position_role
                FROM historico h
                LEFT JOIN (
                    SELECT DISTINCT 
                        logical_access_name,
                        description,
                        unit,
                        subunit,
                        position_role
                    FROM applications
                ) a ON h.app_access_name = a.logical_access_name
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
                                   responsible: str = "Sistema",
                                   subunit: Optional[str] = None) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa el onboarding de un empleado y determina qué accesos necesita.
        Crea registros por cada app que coincida con (unit, subunit?, position_role) **sin duplicados**.
        """
        try:
            # 1. Verificar que el empleado existe
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []

            # 2. Obtener aplicaciones requeridas para la posición (ya sin duplicados por clave)
            required_apps = self.get_applications_by_position(position, unit, subunit=subunit)
            if not required_apps:
                return False, f"No se encontraron aplicaciones para la posición {position} en {unit}", []

            # 3. Crear registros históricos para cada aplicación (dedupe por tripleta normalizada)
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
            active_access = [h for h in history if h.get('status') == 'Completado' and h.get('process_access') in ('onboarding', 'lateral_movement')]

            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []

            for access in active_access:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'offboarding',
                    'sid': scotia_id,
                    'area': 'out of the company',  # Área fija para offboarding
                    'subunit': 'out of the company',  # Subárea fija para offboarding
                    'event_description': f"Revocación de acceso para {access.get('app_access_name') or access.get('app_logical_access_name')}",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': access.get('app_access_name') or access.get('app_logical_access_name'),
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }

                success, message = self.create_historical_record(record_data)
                if success:
                    created_records.append(record_data)
                else:
                    print(f"Error creando registro de offboarding: {message}")

            # Marcar empleado como inactivo
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE headcount SET activo = 0 WHERE scotia_id = ?', (scotia_id,))
            conn.commit()
            conn.close()

            return True, f"Offboarding procesado para {scotia_id}. {len(created_records)} accesos a revocar.", created_records

        except Exception as e:
            return False, f"Error procesando offboarding: {str(e)}", []

    def process_lateral_movement(self, scotia_id: str, new_position: str, new_unit: str, 
                                responsible: str = "Sistema", new_subunit: Optional[str] = None) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Procesa un movimiento lateral comparando por clave (unit, subunit, position_role, logical_access_name)."""
        try:
            employee = self.get_employee_by_id(scotia_id)
            if not employee:
                return False, f"Empleado {scotia_id} no encontrado", []

            old_position = (employee.get('position') or '').strip()
            old_unit = (employee.get('unit') or '').strip()

            # Accesos definidos por malla (no el historial), antes y después
            current_mesh_apps = self.get_applications_by_position(old_position, old_unit)
            new_mesh_apps = self.get_applications_by_position(new_position, new_unit, subunit=new_subunit)

            current_keys = {self._access_key(app.get('unit'), app.get('subunit'), app.get('position_role'), app.get('logical_access_name')) for app in current_mesh_apps}
            new_keys = {self._access_key(app.get('unit'), app.get('subunit'), app.get('position_role'), app.get('logical_access_name')) for app in new_mesh_apps}

            to_revoke_keys = current_keys - new_keys
            to_grant_keys = new_keys - current_keys

            # Mapear para generar descripciones
            app_index = {self._access_key(app.get('unit'), app.get('subunit'), app.get('position_role'), app.get('logical_access_name')): app for app in (current_mesh_apps + new_mesh_apps)}

            case_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{scotia_id}"
            created_records = []

            # Revocar
            for (unit, subunit, position_role, lan) in to_revoke_keys:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'offboarding',
                    'sid': scotia_id,
                    'area': unit,
                    'subunit': subunit,
                    'event_description': f"Revocación de acceso para {lan} (lateral movement)",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': lan,
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                ok, _ = self.create_historical_record(record_data)
                if ok:
                    created_records.append(record_data)

            # Otorgar
            for (unit, subunit, position_role, lan) in to_grant_keys:
                record_data = {
                    'scotia_id': scotia_id,
                    'case_id': case_id,
                    'responsible': responsible,
                    'process_access': 'onboarding',
                    'sid': scotia_id,
                    'area': unit,
                    'subunit': subunit,
                    'event_description': f"Otorgamiento de acceso para {lan} (lateral movement)",
                    'ticket_email': f"{responsible}@empresa.com",
                    'app_access_name': lan,
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                }
                ok, _ = self.create_historical_record(record_data)
                if ok:
                    created_records.append(record_data)

            # Actualizar posición/unidad
            success, message = self.update_employee_position(scotia_id, new_position, new_unit)
            if not success:
                return False, f"Error actualizando posición: {message}", []

            return True, (
                f"Movimiento lateral procesado para {scotia_id}. "
                f"{len(to_revoke_keys)} accesos a revocar, {len(to_grant_keys)} accesos a otorgar."), created_records

        except Exception as e:
            return False, f"Error procesando movimiento lateral: {str(e)}", []

    def get_access_reconciliation_report(self, scotia_id: str) -> Dict[str, Any]:
        """Genera un reporte de conciliación estricta por (unit, subunit, position_role, logical_access_name)."""
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

            # 4) Historial/actuales: considerar solo completados (onboarding o lateral)
            # Y que coincidan con la unidad actual del empleado
            current_records = [
                h for h in history
                if (h.get('status') == 'Completado' and 
                    h.get('process_access') in ('onboarding', 'lateral_movement') and
                    h.get('area') == emp_unit)  # Solo comparar por unidad
            ]

            # Claves actuales - usar tripleta normalizada: unit, position_role, logical_access_name (ignora subunit)
            # Solo considerar registros que coincidan con la unidad actual del empleado
            current_keys = set()
            for h in current_records:
                # Usar datos de la aplicación si están disponibles, sino usar datos del historial
                app_unit = h.get('app_unit') or h.get('area', '')
                app_position = h.get('app_position_role') or h.get('position', '')
                app_name = h.get('app_logical_access_name') or h.get('app_access_name', '')
                
                # Solo agregar si coincide con la unidad actual del empleado y tiene position válido
                if (app_unit == emp_unit and app_position and app_name):
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
                    cursor.execute(
                        "SELECT id FROM historico WHERE scotia_id = ? AND case_id = ? AND app_access_name = ?",
                        (scotia_id, case_id, app_access_name)
                    )
                    
                    if not cursor.fetchone():
                        return False
                    
                    # Eliminar solo el registro específico
                    cursor.execute(
                        "DELETE FROM historico WHERE scotia_id = ? AND case_id = ? AND app_access_name = ?",
                        (scotia_id, case_id, app_access_name)
                    )
                else:
                    # Si no se proporciona app_access_name, eliminar solo el primer registro encontrado
                    cursor.execute(
                        "SELECT id FROM historico WHERE scotia_id = ? AND case_id = ? LIMIT 1",
                        (scotia_id, case_id)
                    )
                    
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
    


# Instancia global del servicio
access_service = AccessManagementService()
