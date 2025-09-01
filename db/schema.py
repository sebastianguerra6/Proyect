"""
Esquema de base de datos para el sistema de conciliación de accesos
"""
import sqlite3
from datetime import datetime
from typing import Optional


def create_tables(connection: sqlite3.Connection) -> None:
    """Crea las tablas si no existen (idempotente)"""
    
    # Tabla de personas
    connection.execute("""
        CREATE TABLE IF NOT EXISTS person (
            sid TEXT PRIMARY KEY,
            area TEXT,
            subunit TEXT,
            cargo TEXT,
            email TEXT,
            updated_at TEXT
        )
    """)
    
    # Tabla de matriz de autorizaciones por puesto
    connection.execute("""
        CREATE TABLE IF NOT EXISTS authorized_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subunit TEXT NOT NULL,
            cargo TEXT NOT NULL,
            app_name TEXT NOT NULL,
            role_name TEXT,
            UNIQUE(subunit, cargo, app_name, role_name) ON CONFLICT IGNORE
        )
    """)
    
    # Tabla de historial de accesos
    connection.execute("""
        CREATE TABLE IF NOT EXISTS access_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sid TEXT NOT NULL,
            app_name TEXT NOT NULL,
            role_name TEXT,
            tipo TEXT NOT NULL CHECK(tipo IN ('onboarding','offboarding')),
            record_date TEXT NOT NULL,
            ingresado_por TEXT,
            status TEXT,
            comment TEXT,
            FOREIGN KEY (sid) REFERENCES person(sid)
        )
    """)
    
    # Crear índices para mejorar rendimiento
    connection.execute("CREATE INDEX IF NOT EXISTS idx_access_history_sid ON access_history(sid)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_access_history_app ON access_history(app_name)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_access_history_date ON access_history(record_date)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_authorized_matrix_subunit_cargo ON authorized_matrix(subunit, cargo)")
    
    connection.commit()


def create_views(connection: sqlite3.Connection) -> None:
    """Crea las vistas necesarias para la conciliación"""
    
    # Vista de accesos actuales (último record_date por sid, app_name)
    connection.execute("""
        CREATE VIEW IF NOT EXISTS vw_current_assignments AS
        WITH latest_access AS (
            SELECT 
                sid, 
                app_name, 
                role_name,
                tipo,
                record_date,
                ROW_NUMBER() OVER (
                    PARTITION BY sid, app_name 
                    ORDER BY record_date DESC
                ) as rn
            FROM access_history
        )
        SELECT 
            sid,
            app_name,
            role_name,
            CASE 
                WHEN tipo = 'onboarding' THEN 1 
                WHEN tipo = 'offboarding' THEN 0 
                ELSE 0 
            END as has_access,
            record_date
        FROM latest_access 
        WHERE rn = 1
    """)
    
    # Vista de accesos objetivo (lo que debería tener según su puesto)
    connection.execute("""
        CREATE VIEW IF NOT EXISTS vw_should_assignments AS
        SELECT 
            p.sid,
            am.app_name,
            am.role_name,
            p.subunit,
            p.cargo
        FROM person p
        JOIN authorized_matrix am ON p.subunit = am.subunit AND p.cargo = am.cargo
    """)
    
    connection.commit()


def insert_sample_data(connection: sqlite3.Connection) -> None:
    """Inserta datos de ejemplo para pruebas"""
    
    # Insertar personas de ejemplo
    persons = [
        ('EMP001', 'Tecnología', 'Desarrollo', 'Desarrollador Senior', 'juan.perez@empresa.com'),
        ('EMP002', 'Tecnología', 'Desarrollo', 'Desarrollador Junior', 'maria.garcia@empresa.com'),
        ('EMP003', 'Finanzas', 'Contabilidad', 'Contador', 'carlos.lopez@empresa.com')
    ]
    
    for person in persons:
        connection.execute("""
            INSERT OR REPLACE INTO person (sid, area, subunit, cargo, email, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (*person, datetime.now().isoformat()))
    
    # Insertar matriz de autorizaciones
    authorizations = [
        ('Desarrollo', 'Desarrollador Senior', 'GitLab', 'Developer'),
        ('Desarrollo', 'Desarrollador Senior', 'Jira', 'Developer'),
        ('Desarrollo', 'Desarrollador Senior', 'Confluence', 'Editor'),
        ('Desarrollo', 'Desarrollador Junior', 'GitLab', 'Developer'),
        ('Desarrollo', 'Desarrollador Junior', 'Jira', 'Viewer'),
        ('Contabilidad', 'Contador', 'SAP', 'User'),
        ('Contabilidad', 'Contador', 'Excel', 'Editor')
    ]
    
    for auth in authorizations:
        connection.execute("""
            INSERT OR IGNORE INTO authorized_matrix (subunit, cargo, app_name, role_name)
            VALUES (?, ?, ?, ?)
        """, auth)
    
    # Insertar historial de accesos de ejemplo
    access_history = [
        ('EMP001', 'GitLab', 'Developer', 'onboarding', '2024-01-15T09:00:00', 'Admin', 'Completado', 'Acceso inicial'),
        ('EMP001', 'Jira', 'Developer', 'onboarding', '2024-01-15T09:00:00', 'Admin', 'Completado', 'Acceso inicial'),
        ('EMP002', 'GitLab', 'Developer', 'onboarding', '2024-01-20T10:00:00', 'Admin', 'Completado', 'Acceso inicial'),
        ('EMP003', 'SAP', 'User', 'onboarding', '2024-01-10T08:00:00', 'Admin', 'Completado', 'Acceso inicial')
    ]
    
    for access in access_history:
        connection.execute("""
            INSERT OR IGNORE INTO access_history (sid, app_name, role_name, tipo, record_date, ingresado_por, status, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, access)
    
    connection.commit()


def init_database(db_path: str = "database/empleados.db") -> sqlite3.Connection:
    """Inicializa la base de datos con todas las tablas y vistas"""
    connection = sqlite3.connect(db_path)
    
    # Configurar PRAGMAs para mejor rendimiento
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    connection.execute("PRAGMA cache_size = 10000")
    
    # Crear tablas y vistas
    create_tables(connection)
    create_views(connection)
    
    # Insertar datos de ejemplo (opcional)
    try:
        insert_sample_data(connection)
    except Exception as e:
        print(f"Advertencia: No se pudieron insertar datos de ejemplo: {e}")
    
    return connection


if __name__ == "__main__":
    # Prueba de inicialización
    conn = init_database()
    print("Base de datos inicializada correctamente")
    
    # Verificar que las vistas se crearon
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    views = cursor.fetchall()
    print(f"Vistas creadas: {[v[0] for v in views]}")
    
    conn.close()

