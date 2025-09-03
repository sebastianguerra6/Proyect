"""
Gestor consolidado de base de datos que incluye:
- Configuración centralizada
- Inicialización y migración
- Sincronización de tablas
- Utilidades de base de datos
"""
import os
import sqlite3
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import shutil

# Configuración centralizada
DB_PATH = os.path.join(os.path.dirname(__file__), "empleados.db")
DB_CONFIG = {
    'path': DB_PATH,
    'timeout': 30,
    'check_same_thread': False
}

def get_db_path():
    """Retorna la ruta de la base de datos"""
    return DB_PATH

def get_db_config():
    """Retorna la configuración de la base de datos"""
    return DB_CONFIG.copy()


class DatabaseManager:
    """Gestor principal de la base de datos"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()
        self.db_path = Path(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30
        )
    
    def init_database(self) -> bool:
        """Inicializa la base de datos con todas las tablas necesarias"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Crear tabla empleados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sid TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    cargo TEXT NOT NULL,
                    sub_unidad TEXT NOT NULL,
                    estado TEXT DEFAULT 'Activo',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Crear tabla procesos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procesos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleado_sid TEXT NOT NULL,
                    tipo_proceso TEXT NOT NULL,
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_fin TIMESTAMP,
                    estado TEXT DEFAULT 'En Proceso',
                    FOREIGN KEY (empleado_sid) REFERENCES empleados (sid)
                )
            ''')
            
            # Crear tabla authorized_matrix
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS authorized_matrix (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cargo TEXT NOT NULL,
                    subunit TEXT NOT NULL,
                    app_name TEXT NOT NULL,
                    role_name TEXT NOT NULL,
                    is_required BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(cargo, subunit, app_name)
                )
            ''')
            
            # Crear tabla accesos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accesos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sid TEXT NOT NULL,
                    app_name TEXT NOT NULL,
                    role_name TEXT NOT NULL,
                    fecha_concesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estado TEXT DEFAULT 'Activo',
                    FOREIGN KEY (sid) REFERENCES empleados (sid)
                )
            ''')
            
            # Crear tabla access_history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sid TEXT NOT NULL,
                    app_name TEXT NOT NULL,
                    role_name TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ingresado_por TEXT,
                    status TEXT DEFAULT 'Pendiente',
                    comment TEXT,
                    FOREIGN KEY (sid) REFERENCES empleados (sid)
                )
            ''')
            
            # Crear índices para mejor rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_empleados_sid ON empleados (sid)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_authorized_matrix_cargo_subunit ON authorized_matrix (cargo, subunit)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_accesos_sid ON accesos (sid)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_history_sid ON access_history (sid)')
            
            conn.commit()
            conn.close()
            
            print("✅ Base de datos inicializada correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            return False
    
    def insert_sample_data(self) -> bool:
        """Inserta datos de ejemplo para pruebas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insertar empleados de ejemplo
            empleados_ejemplo = [
                ('EMP001', 'Juan Pérez', 'Desarrollador', 'Tecnología'),
                ('EMP002', 'María García', 'Analista', 'Tecnología'),
                ('EMP003', 'Carlos López', 'Gerente', 'Tecnología'),
                ('EMP004', 'Ana Rodríguez', 'Desarrollador Senior', 'Tecnología'),
                ('EMP005', 'Luis Martínez', 'Analista', 'Recursos Humanos'),
                ('EMP006', 'Carmen Silva', 'Gerente', 'Recursos Humanos')
            ]
            
            for sid, nombre, cargo, sub_unidad in empleados_ejemplo:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO empleados (sid, nombre, cargo, sub_unidad)
                        VALUES (?, ?, ?, ?)
                    ''', (sid, nombre, cargo, sub_unidad))
                except sqlite3.IntegrityError:
                    pass  # Ya existe
            
            # Insertar matriz de autorización
            matriz_autorizacion = [
                ('Desarrollador', 'Tecnología', 'Sistema de Gestión', 'Usuario'),
                ('Desarrollador', 'Tecnología', 'Portal de Recursos', 'Usuario'),
                ('Analista', 'Tecnología', 'Sistema de Gestión', 'Usuario'),
                ('Analista', 'Tecnología', 'Portal de Recursos', 'Usuario'),
                ('Gerente', 'Tecnología', 'Sistema de Gestión', 'Administrador'),
                ('Gerente', 'Tecnología', 'Portal de Recursos', 'Administrador'),
                ('Desarrollador Senior', 'Tecnología', 'Sistema de Gestión', 'Administrador'),
                ('Desarrollador Senior', 'Tecnología', 'Portal de Recursos', 'Usuario'),
                ('Analista', 'Recursos Humanos', 'Sistema de Gestión', 'Usuario'),
                ('Analista', 'Recursos Humanos', 'Portal de Recursos', 'Usuario'),
                ('Gerente', 'Recursos Humanos', 'Sistema de Gestión', 'Administrador'),
                ('Gerente', 'Recursos Humanos', 'Portal de Recursos', 'Administrador')
            ]
            
            for cargo, subunit, app_name, role_name in matriz_autorizacion:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO authorized_matrix (cargo, subunit, app_name, role_name)
                        VALUES (?, ?, ?, ?)
                    ''', (cargo, subunit, app_name, role_name))
                except sqlite3.IntegrityError:
                    pass  # Ya existe
            
            conn.commit()
            conn.close()
            
            print("✅ Datos de ejemplo insertados correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error insertando datos de ejemplo: {e}")
            return False
    
    def sync_employee_tables(self) -> bool:
        """Sincroniza las tablas de empleados y crea accesos automáticamente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener todos los empleados
            cursor.execute('SELECT sid, cargo, sub_unidad FROM empleados')
            empleados = cursor.fetchall()
            
            accesos_creados = 0
            
            for sid, cargo, sub_unidad in empleados:
                # Obtener accesos autorizados para este empleado
                cursor.execute('''
                    SELECT app_name, role_name FROM authorized_matrix
                    WHERE cargo = ? AND subunit = ?
                ''', (cargo, sub_unidad))
                
                accesos_autorizados = cursor.fetchall()
                
                for app_name, role_name in accesos_autorizados:
                    # Verificar si ya existe el acceso
                    cursor.execute('''
                        SELECT id FROM accesos
                        WHERE sid = ? AND app_name = ? AND estado = 'Activo'
                    ''', (sid, app_name))
                    
                    if not cursor.fetchone():
                        # Crear acceso automáticamente
                        cursor.execute('''
                            INSERT INTO accesos (sid, app_name, role_name, estado)
                            VALUES (?, ?, ?, 'Activo')
                        ''', (sid, app_name, role_name))
                        accesos_creados += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Sincronización completada. {accesos_creados} accesos creados automáticamente")
            return True
            
        except Exception as e:
            print(f"❌ Error en sincronización: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        try:
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
            cursor.execute('SELECT COUNT(DISTINCT app_name) FROM authorized_matrix')
            stats['aplicaciones'] = cursor.fetchone()[0]
            
            conn.close()
            return stats
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def backup_database(self, backup_path: str = None) -> bool:
        """Crea una copia de seguridad de la base de datos"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backup_empleados_{timestamp}.db"
            
            backup_path = os.path.join(os.path.dirname(self.db_path), backup_path)
            shutil.copy2(str(self.db_path), backup_path)
            
            print(f"✅ Copia de seguridad creada: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando copia de seguridad: {e}")
            return False
    
    def cleanup_old_backups(self, keep_days: int = 7) -> int:
        """Elimina copias de seguridad antiguas"""
        try:
            backup_dir = os.path.dirname(self.db_path)
            current_time = datetime.now()
            backups_removed = 0
            
            for filename in os.listdir(backup_dir):
                if filename.startswith("backup_empleados_") and filename.endswith(".db"):
                    file_path = os.path.join(backup_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if (current_time - file_time).days > keep_days:
                        os.remove(file_path)
                        backups_removed += 1
            
            if backups_removed > 0:
                print(f"✅ {backups_removed} copias de seguridad antiguas eliminadas")
            
            return backups_removed
            
        except Exception as e:
            print(f"❌ Error limpiando copias de seguridad: {e}")
            return 0


# Funciones helper para uso directo
def init_database() -> bool:
    """Función helper para inicializar la base de datos"""
    manager = DatabaseManager()
    return manager.init_database()

def insert_sample_data() -> bool:
    """Función helper para insertar datos de ejemplo"""
    manager = DatabaseManager()
    return manager.insert_sample_data()

def sync_employee_tables() -> bool:
    """Función helper para sincronizar tablas de empleados"""
    manager = DatabaseManager()
    return manager.sync_employee_tables()

def get_database_stats() -> Dict[str, int]:
    """Función helper para obtener estadísticas"""
    manager = DatabaseManager()
    return manager.get_database_stats()

def backup_database(backup_path: str = None) -> bool:
    """Función helper para crear copia de seguridad"""
    manager = DatabaseManager()
    return manager.backup_database(backup_path)

def cleanup_old_backups(keep_days: int = 7) -> int:
    """Función helper para limpiar copias antiguas"""
    manager = DatabaseManager()
    return manager.cleanup_old_backups(keep_days)


# Instancia global para usar en toda la aplicación
db_manager = DatabaseManager()


if __name__ == "__main__":
    """Script principal para inicializar la base de datos"""
    print("🚀 Inicializando base de datos...")
    
    if init_database():
        if insert_sample_data():
            if sync_employee_tables():
                stats = get_database_stats()
                print(f"\n📊 Estadísticas de la base de datos:")
                for key, value in stats.items():
                    print(f"   {key}: {value}")
                
                print("\n✅ Base de datos completamente configurada!")
            else:
                print("❌ Error en sincronización de tablas")
        else:
            print("❌ Error insertando datos de ejemplo")
    else:
        print("❌ Error inicializando base de datos")
