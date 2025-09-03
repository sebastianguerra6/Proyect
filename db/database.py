"""
Módulo consolidado de base de datos que incluye:
- Conexiones a la base de datos
- Esquemas y creación de tablas
- Consultas básicas del sistema
"""
import sqlite3
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from datetime import datetime

# Agregar el directorio database al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from config import get_db_path


class DatabaseConnection:
    """Clase para manejar conexiones a la base de datos"""
    
    def __init__(self, db_path: str = None):
        self.db_path = Path(db_path or get_db_path())
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30
        )
    
    @contextmanager
    def get_cursor(self):
        """Context manager para obtener un cursor de la base de datos"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Ejecuta una consulta y retorna los resultados"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Ejecuta una actualización y retorna el número de filas afectadas"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """Verifica si una tabla existe"""
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
    
    def get_table_info(self, table_name: str) -> list:
        """Obtiene información de la estructura de una tabla"""
        query = "PRAGMA table_info(?)"
        return self.execute_query(query, (table_name,))
    
    def backup_database(self, backup_path: str) -> bool:
        """Crea una copia de seguridad de la base de datos"""
        try:
            import shutil
            shutil.copy2(str(self.db_path), backup_path)
            return True
        except Exception:
            return False


class DatabaseSchema:
    """Clase para manejar el esquema de la base de datos"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()
    
    def create_tables(self, connection: sqlite3.Connection) -> None:
        """Crea las tablas si no existen (idempotente)"""
        
        # Tabla person (personas del sistema)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sid TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                department TEXT,
                position TEXT,
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla authorized_matrix (matriz de autorizaciones)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS authorized_matrix (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                department TEXT NOT NULL,
                application TEXT NOT NULL,
                access_level TEXT NOT NULL,
                is_required BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(role, department, application)
            )
        ''')
        
        # Tabla access_history (historial de accesos)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS access_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_sid TEXT NOT NULL,
                application TEXT NOT NULL,
                access_level TEXT NOT NULL,
                granted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                revoked_date TIMESTAMP,
                granted_by TEXT,
                revoked_by TEXT,
                status TEXT DEFAULT 'Active',
                FOREIGN KEY (person_sid) REFERENCES person (sid)
            )
        ''')
        
        # Tabla accesos (accesos actuales)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS accesos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_sid TEXT NOT NULL,
                aplicacion TEXT NOT NULL,
                nivel_acceso TEXT NOT NULL,
                fecha_concesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'Activo',
                FOREIGN KEY (empleado_sid) REFERENCES empleados (sid)
            )
        ''')
        
        # Crear índices para mejor rendimiento
        connection.execute('CREATE INDEX IF NOT EXISTS idx_person_sid ON person (sid)')
        connection.execute('CREATE INDEX IF NOT EXISTS idx_authorized_matrix_role_dept ON authorized_matrix (role, department)')
        connection.execute('CREATE INDEX IF NOT EXISTS idx_access_history_person ON access_history (person_sid)')
        connection.execute('CREATE INDEX IF NOT EXISTS idx_accesos_empleado ON accesos (empleado_sid)')
    
    def create_views(self, connection: sqlite3.Connection) -> None:
        """Crea las vistas para facilitar consultas"""
        
        # Vista de asignaciones actuales
        connection.execute('''
            CREATE VIEW IF NOT EXISTS current_assignments AS
            SELECT 
                p.sid,
                p.name,
                p.department,
                p.position,
                ah.application,
                ah.access_level,
                ah.granted_date,
                ah.status
            FROM person p
            LEFT JOIN access_history ah ON p.sid = ah.person_sid
            WHERE ah.status = 'Active' OR ah.status IS NULL
        ''')
        
        # Vista de asignaciones que deberían ser
        connection.execute('''
            CREATE VIEW IF NOT EXISTS should_be_assignments AS
            SELECT 
                p.sid,
                p.name,
                p.department,
                p.position,
                am.application,
                am.access_level,
                am.is_required
            FROM person p
            CROSS JOIN authorized_matrix am
            WHERE p.department = am.department 
            AND p.position = am.role
            AND am.is_required = 1
        ''')
    
    def init_database(self, db_path: str = None) -> sqlite3.Connection:
        """Inicializa la base de datos con todas las tablas y vistas"""
        connection = sqlite3.connect(db_path or self.db_path)
        
        try:
            self.create_tables(connection)
            self.create_views(connection)
            connection.commit()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            connection.rollback()
            raise
        finally:
            connection.close()
        
        return connection
    
    def insert_sample_data(self, connection: sqlite3.Connection) -> None:
        """Inserta datos de ejemplo para pruebas"""
        
        # Insertar matriz de autorización de ejemplo
        sample_matrix = [
            ('Desarrollador', 'Tecnología', 'Sistema de Gestión', 'Usuario'),
            ('Desarrollador', 'Tecnología', 'Portal de Recursos', 'Usuario'),
            ('Analista', 'Tecnología', 'Sistema de Gestión', 'Usuario'),
            ('Analista', 'Tecnología', 'Portal de Recursos', 'Usuario'),
            ('Gerente', 'Tecnología', 'Sistema de Gestión', 'Administrador'),
            ('Gerente', 'Tecnología', 'Portal de Recursos', 'Administrador'),
            ('Desarrollador Senior', 'Tecnología', 'Sistema de Gestión', 'Administrador'),
            ('Desarrollador Senior', 'Tecnología', 'Portal de Recursos', 'Usuario'),
        ]
        
        for role, dept, app, level in sample_matrix:
            try:
                connection.execute('''
                    INSERT OR IGNORE INTO authorized_matrix (role, department, application, access_level)
                    VALUES (?, ?, ?, ?)
                ''', (role, dept, app, level))
            except sqlite3.IntegrityError:
                pass  # Ya existe
        
        connection.commit()
        print("✅ Datos de ejemplo insertados")


class DatabaseQueries:
    """Clase con consultas SQL comunes"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    # Consultas de empleados
    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Obtiene todos los empleados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sid, nombre, cargo, sub_unidad, estado, fecha_creacion
            FROM empleados
            ORDER BY nombre
        ''')
        
        empleados = []
        for row in cursor.fetchall():
            empleados.append({
                'sid': row[0],
                'nombre': row[1],
                'cargo': row[2],
                'sub_unidad': row[3],
                'estado': row[4],
                'fecha_creacion': row[5]
            })
        
        conn.close()
        return empleados
    
    def get_employee_by_sid(self, sid: str) -> Optional[Dict[str, Any]]:
        """Obtiene un empleado por SID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sid, nombre, cargo, sub_unidad, estado, fecha_creacion
            FROM empleados
            WHERE sid = ?
        ''', (sid,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'sid': row[0],
                'nombre': row[1],
                'cargo': row[2],
                'sub_unidad': row[3],
                'estado': row[4],
                'fecha_creacion': row[5]
            }
        return None
    
    def search_employees(self, search_term: str) -> List[Dict[str, Any]]:
        """Busca empleados por término de búsqueda"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sid, nombre, cargo, sub_unidad, estado, fecha_creacion
            FROM empleados
            WHERE sid LIKE ? OR nombre LIKE ? OR cargo LIKE ? OR sub_unidad LIKE ?
            ORDER BY nombre
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        empleados = []
        for row in cursor.fetchall():
            empleados.append({
                'sid': row[0],
                'nombre': row[1],
                'cargo': row[2],
                'sub_unidad': row[3],
                'estado': row[4],
                'fecha_creacion': row[5]
            })
        
        conn.close()
        return empleados
    
    # Consultas de accesos
    def get_employee_accesses(self, sid: str) -> List[Dict[str, Any]]:
        """Obtiene los accesos de un empleado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT aplicacion, nivel_acceso, fecha_concesion, estado
            FROM accesos
            WHERE empleado_sid = ? AND estado = 'Activo'
            ORDER BY fecha_concesion DESC
        ''', (sid,))
        
        accesos = []
        for row in cursor.fetchall():
            accesos.append({
                'aplicacion': row[0],
                'nivel_acceso': row[1],
                'fecha_concesion': row[2],
                'estado': row[3]
            })
        
        conn.close()
        return accesos
    
    def get_authorized_accesses(self, cargo: str, sub_unidad: str) -> List[Dict[str, Any]]:
        """Obtiene los accesos autorizados para un cargo y sub-unidad"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT application, access_level, is_required
            FROM authorized_matrix
            WHERE role = ? AND department = ?
            ORDER BY application
        ''', (cargo, sub_unidad))
        
        accesos = []
        for row in cursor.fetchall():
            accesos.append({
                'aplicacion': row[0],
                'nivel_acceso': row[1],
                'requerido': bool(row[2])
            })
        
        conn.close()
        return accesos
    
    # Consultas de procesos
    def get_employee_processes(self, sid: str) -> List[Dict[str, Any]]:
        """Obtiene los procesos de un empleado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tipo_proceso, fecha_inicio, fecha_fin, estado
            FROM procesos
            WHERE empleado_sid = ?
            ORDER BY fecha_inicio DESC
        ''', (sid,))
        
        procesos = []
        for row in cursor.fetchall():
            procesos.append({
                'tipo_proceso': row[0],
                'fecha_inicio': row[1],
                'fecha_fin': row[2],
                'estado': row[3]
            })
        
        conn.close()
        return procesos
    
    # Consultas de estadísticas
    def get_database_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Contar empleados
        cursor.execute('SELECT COUNT(*) FROM empleados')
        stats['empleados'] = cursor.fetchone()[0]
        
        # Contar accesos activos
        cursor.execute('SELECT COUNT(*) FROM accesos WHERE estado = "Activo"')
        stats['accesos_activos'] = cursor.fetchone()[0]
        
        # Contar procesos
        cursor.execute('SELECT COUNT(*) FROM procesos')
        stats['procesos'] = cursor.fetchone()[0]
        
        # Contar aplicaciones en matriz de autorización
        cursor.execute('SELECT COUNT(DISTINCT application) FROM authorized_matrix')
        stats['aplicaciones'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def get_access_reconciliation(self, sid: str) -> Dict[str, Any]:
        """Obtiene información de conciliación de accesos para un empleado"""
        empleado = self.get_employee_by_sid(sid)
        if not empleado:
            return None
        
        accesos_actuales = self.get_employee_accesses(sid)
        accesos_autorizados = self.get_authorized_accesses(empleado['cargo'], empleado['sub_unidad'])
        
        # Encontrar accesos faltantes
        aplicaciones_actuales = {acc['aplicacion'] for acc in accesos_actuales}
        aplicaciones_autorizadas = {acc['aplicacion'] for acc in accesos_autorizados}
        
        accesos_faltantes = aplicaciones_autorizadas - aplicaciones_actuales
        accesos_extra = aplicaciones_actuales - aplicaciones_autorizadas
        
        return {
            'empleado': empleado,
            'accesos_actuales': accesos_actuales,
            'accesos_autorizados': accesos_autorizados,
            'accesos_faltantes': list(accesos_faltantes),
            'accesos_extra': list(accesos_extra),
            'coincidencia': len(aplicaciones_actuales & aplicaciones_autorizadas) / len(aplicaciones_autorizadas) if aplicaciones_autorizadas else 0
        }


# Instancias globales para usar en toda la aplicación
db_connection = DatabaseConnection()
db_schema = DatabaseSchema()
db_queries = DatabaseQueries()


# Funciones helper para uso directo
def get_connection(db_path: str = None) -> sqlite3.Connection:
    """Función helper para obtener una conexión directa"""
    db = DatabaseConnection(db_path)
    return db.get_connection()


def execute_query(query: str, params: tuple = (), db_path: str = None) -> list:
    """Función helper para ejecutar consultas"""
    db = DatabaseConnection(db_path)
    return db.execute_query(query, params)


def execute_update(query: str, params: tuple = (), db_path: str = None) -> int:
    """Función helper para ejecutar actualizaciones"""
    db = DatabaseConnection(db_path)
    return db.execute_update(query, params)


def get_all_employees(db_path: str = None) -> List[Dict[str, Any]]:
    """Función helper para obtener todos los empleados"""
    queries = DatabaseQueries(db_path)
    return queries.get_all_employees()


def get_employee_accesses(sid: str, db_path: str = None) -> List[Dict[str, Any]]:
    """Función helper para obtener accesos de un empleado"""
    queries = DatabaseQueries(db_path)
    return queries.get_employee_accesses(sid)


def get_access_reconciliation(sid: str, db_path: str = None) -> Dict[str, Any]:
    """Función helper para obtener conciliación de accesos"""
    queries = DatabaseQueries(db_path)
    return queries.get_access_reconciliation(sid)
