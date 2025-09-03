"""
Módulo consolidado de consultas de conciliación de accesos
"""
from typing import List, Dict, Any, Optional
import sys
import os

# Agregar el directorio database al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from config import get_db_path


class ReconciliationQueries:
    """Consultas para la conciliación de accesos"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        import sqlite3
        return sqlite3.connect(self.db_path)
    
    def get_person_info(self, sid: str) -> Optional[List]:
        """Obtiene información de una persona por SID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sid, sub_unidad, sub_unidad, cargo, 'email@example.com'
            FROM empleados
            WHERE sid = ?
        ''', (sid,))
        
        result = cursor.fetchone()
        conn.close()
        return [result] if result else None
    
    def get_current_accesses(self, sid: str) -> List[tuple]:
        """Obtiene los accesos actuales de una persona"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT app_name, role_name
            FROM accesos
            WHERE sid = ? AND status = 'Activo'
        ''', (sid,))
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_target_accesses(self, sid: str) -> List[tuple]:
        """Obtiene los accesos objetivo para una persona según su cargo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT am.app_name, am.role_name
            FROM empleados e
            JOIN authorized_matrix am ON e.cargo = am.cargo AND e.sub_unidad = am.subunit
            WHERE e.sid = ?
        ''', (sid,))
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_accesses_to_grant(self, sid: str) -> List[tuple]:
        """Obtiene los accesos que se deben otorgar"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT am.app_name, am.role_name, 'GRANT', 'Acceso requerido por cargo'
            FROM empleados e
            JOIN authorized_matrix am ON e.cargo = am.cargo AND e.sub_unidad = am.subunit
            LEFT JOIN accesos a ON e.sid = a.sid AND am.app_name = a.app_name
            WHERE e.sid = ? AND a.id IS NULL
        ''', (sid,))
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_accesses_to_revoke(self, sid: str) -> List[tuple]:
        """Obtiene los accesos que se deben revocar"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.app_name, a.role_name, 'REVOKE', 'Acceso no autorizado'
            FROM accesos a
            LEFT JOIN empleados e ON a.sid = e.sid
            LEFT JOIN authorized_matrix am ON e.cargo = am.cargo AND e.sub_unidad = am.subunit 
                AND a.app_name = am.app_name
            WHERE a.sid = ? AND a.status = 'Activo' AND am.id IS NULL
        ''', (sid,))
        
        result = cursor.fetchall()
        return result
    
    def get_all_persons(self) -> List[tuple]:
        """Obtiene todas las personas del sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sid, sub_unidad, sub_unidad, cargo, 'email@example.com'
            FROM empleados
            ORDER BY nombre
        ''')
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_access_summary_by_sid(self, sid: str) -> Dict[str, int]:
        """Obtiene un resumen de accesos para una persona"""
        current = len(self.get_current_accesses(sid))
        target = len(self.get_target_accesses(sid))
        to_grant = len(self.get_accesses_to_grant(sid))
        to_revoke = len(self.get_accesses_to_revoke(sid))
        
        return {
            'current': current,
            'target': target,
            'to_grant': to_grant,
            'to_revoke': to_revoke
        }
    
    def get_authorized_matrix_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen de la matriz de autorización"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT subunit, cargo, COUNT(*) as app_count
            FROM authorized_matrix
            GROUP BY subunit, cargo
            ORDER BY subunit, cargo
        ''')
        
        result = cursor.fetchall()
        conn.close()
        
        summary = {}
        for dept, role, count in result:
            if dept not in summary:
                summary[dept] = {}
            summary[dept][role] = count
        
        return summary
    
    def check_duplicate_ticket(self, sid: str, app_name: str, tipo: str) -> bool:
        """Verifica si ya existe un ticket reciente para evitar duplicados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM access_history
            WHERE sid = ? AND app_name = ? AND tipo = ?
            AND datetime(record_date) > datetime('now', '-24 hours')
        ''', (sid, app_name, tipo))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0


# Instancia global para usar en los servicios
reconciliation_queries = ReconciliationQueries()
