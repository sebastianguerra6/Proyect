"""
Consultas SQL centralizadas para el sistema de conciliación de accesos
"""
from typing import List, Dict, Any, Tuple
from db.connection import execute_query


class ReconciliationQueries:
    """Clase que contiene todas las consultas SQL para la conciliación"""
    
    @staticmethod
    def get_person_info(sid: str) -> List[Tuple]:
        """Obtiene información de una persona por SID"""
        query = """
            SELECT sid, area, subunit, cargo, email, updated_at
            FROM person 
            WHERE sid = ?
        """
        return execute_query(query, (sid,))
    
    @staticmethod
    def get_current_accesses(sid: str) -> List[Tuple]:
        """Obtiene los accesos actuales de una persona"""
        query = """
            SELECT app_name, role_name, has_access, record_date
            FROM vw_current_assignments
            WHERE sid = ? AND has_access = 1
            ORDER BY app_name
        """
        return execute_query(query, (sid,))
    
    @staticmethod
    def get_target_accesses(sid: str) -> List[Tuple]:
        """Obtiene los accesos objetivo de una persona según su puesto"""
        query = """
            SELECT app_name, role_name, subunit, cargo
            FROM vw_should_assignments
            WHERE sid = ?
            ORDER BY app_name
        """
        return execute_query(query, (sid,))
    
    @staticmethod
    def get_accesses_to_grant(sid: str) -> List[Tuple]:
        """Obtiene los accesos que se deben otorgar (objetivo - actuales)"""
        query = """
            WITH target AS (
                SELECT app_name, role_name
                FROM vw_should_assignments
                WHERE sid = ?
            ),
            current AS (
                SELECT app_name, role_name
                FROM vw_current_assignments
                WHERE sid = ? AND has_access = 1
            )
            SELECT 
                t.app_name,
                t.role_name,
                'GRANT' as accion,
                'Falta acceso' as motivo
            FROM target t
            LEFT JOIN current c ON t.app_name = c.app_name AND 
                                 (t.role_name = c.role_name OR (t.role_name IS NULL AND c.role_name IS NULL))
            WHERE c.app_name IS NULL
            ORDER BY t.app_name
        """
        return execute_query(query, (sid, sid))
    
    @staticmethod
    def get_accesses_to_revoke(sid: str) -> List[Tuple]:
        """Obtiene los accesos que se deben revocar (actuales - objetivo)"""
        query = """
            WITH target AS (
                SELECT app_name, role_name
                FROM vw_should_assignments
                WHERE sid = ?
            ),
            current AS (
                SELECT app_name, role_name
                FROM vw_current_assignments
                WHERE sid = ? AND has_access = 1
            )
            SELECT 
                c.app_name,
                c.role_name,
                'REVOKE' as accion,
                'No autorizado' as motivo
            FROM current c
            LEFT JOIN target t ON c.app_name = t.app_name AND 
                                 (c.role_name = t.role_name OR (c.role_name IS NULL AND t.role_name IS NULL))
            WHERE t.app_name IS NULL
            ORDER BY c.app_name
        """
        return execute_query(query, (sid, sid))
    
    @staticmethod
    def get_all_persons() -> List[Tuple]:
        """Obtiene todas las personas en el sistema"""
        query = """
            SELECT sid, area, subunit, cargo, email, updated_at
            FROM person
            ORDER BY sid
        """
        return execute_query(query)
    
    @staticmethod
    def get_access_history_by_sid(sid: str, limit: int = 100) -> List[Tuple]:
        """Obtiene el historial de accesos de una persona"""
        query = """
            SELECT 
                app_name,
                role_name,
                tipo,
                record_date,
                ingresado_por,
                status,
                comment
            FROM access_history
            WHERE sid = ?
            ORDER BY record_date DESC
            LIMIT ?
        """
        return execute_query(query, (sid, limit))
    
    @staticmethod
    def get_recent_access_history(limit: int = 50) -> List[Tuple]:
        """Obtiene el historial reciente de accesos de todas las personas"""
        query = """
            SELECT 
                sid,
                app_name,
                role_name,
                tipo,
                record_date,
                ingresado_por,
                status,
                comment
            FROM access_history
            ORDER BY record_date DESC
            LIMIT ?
        """
        return execute_query(query, (limit,))
    
    @staticmethod
    def get_authorized_matrix_summary() -> List[Tuple]:
        """Obtiene un resumen de la matriz de autorizaciones"""
        query = """
            SELECT 
                subunit,
                cargo,
                COUNT(*) as total_apps,
                GROUP_CONCAT(app_name, ', ') as apps
            FROM authorized_matrix
            GROUP BY subunit, cargo
            ORDER BY subunit, cargo
        """
        return execute_query(query)
    
    @staticmethod
    def get_access_summary_by_sid(sid: str) -> Dict[str, Any]:
        """Obtiene un resumen completo de accesos para una persona"""
        current = execute_query("""
            SELECT COUNT(*) FROM vw_current_assignments 
            WHERE sid = ? AND has_access = 1
        """, (sid,))
        
        target = execute_query("""
            SELECT COUNT(*) FROM vw_should_assignments 
            WHERE sid = ?
        """, (sid,))
        
        to_grant = execute_query("""
            SELECT COUNT(*) FROM (
                WITH target AS (
                    SELECT app_name, role_name
                    FROM vw_should_assignments
                    WHERE sid = ?
                ),
                current AS (
                    SELECT app_name, role_name
                    FROM vw_current_assignments
                    WHERE sid = ? AND has_access = 1
                )
                SELECT t.app_name
                FROM target t
                LEFT JOIN current c ON t.app_name = c.app_name AND 
                                     (t.role_name = c.role_name OR (t.role_name IS NULL AND c.role_name IS NULL))
                WHERE c.app_name IS NULL
            )
        """, (sid, sid))
        
        to_revoke = execute_query("""
            SELECT COUNT(*) FROM (
                WITH target AS (
                    SELECT app_name, role_name
                    FROM vw_should_assignments
                    WHERE sid = ?
                ),
                current AS (
                    SELECT app_name, role_name
                    FROM vw_current_assignments
                    WHERE sid = ? AND has_access = 1
                )
                SELECT c.app_name
                FROM current c
                LEFT JOIN target t ON c.app_name = t.app_name AND 
                                     (c.role_name = t.role_name OR (c.role_name IS NULL AND t.role_name IS NULL))
                WHERE t.app_name IS NULL
            )
        """, (sid, sid))
        
        return {
            'current': current[0][0] if current else 0,
            'target': target[0][0] if target else 0,
            'to_grant': to_grant[0][0] if to_grant else 0,
            'to_revoke': to_revoke[0][0] if to_revoke else 0
        }
    
    @staticmethod
    def check_duplicate_ticket(sid: str, app_name: str, tipo: str, minutes_threshold: int = 5) -> bool:
        """Verifica si ya existe un ticket similar en los últimos N minutos"""
        query = """
            SELECT COUNT(*)
            FROM access_history
            WHERE sid = ? 
              AND app_name = ? 
              AND tipo = ?
              AND datetime(record_date) > datetime('now', '-{} minutes')
        """.format(minutes_threshold)
        
        result = execute_query(query, (sid, app_name, tipo))
        return result[0][0] > 0 if result else False


# Instancia global para usar en toda la aplicación
reconciliation_queries = ReconciliationQueries()

