"""
Módulo de conexión a la base de datos SQLite
"""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class DatabaseConnection:
    """Clase para manejar conexiones a la base de datos"""
    
    def __init__(self, db_path: str = "database/empleados.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una nueva conexión a la base de datos"""
        connection = sqlite3.connect(self.db_path)
        
        # Configurar PRAGMAs para mejor rendimiento
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")
        connection.execute("PRAGMA cache_size = 10000")
        connection.execute("PRAGMA temp_store = MEMORY")
        
        return connection
    
    @contextmanager
    def get_cursor(self):
        """Context manager para obtener un cursor con manejo automático de transacciones"""
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Ejecuta una consulta SELECT y retorna los resultados"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Ejecuta una consulta INSERT/UPDATE/DELETE y retorna el número de filas afectadas"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_many(self, query: str, params_list: list) -> int:
        """Ejecuta múltiples consultas con diferentes parámetros"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """Verifica si una tabla existe"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
    
    def view_exists(self, view_name: str) -> bool:
        """Verifica si una vista existe"""
        query = "SELECT name FROM sqlite_master WHERE type='view' AND name=?"
        result = self.execute_query(query, (view_name,))
        return len(result) > 0
    
    def get_table_info(self, table_name: str) -> list:
        """Obtiene información de las columnas de una tabla"""
        query = "PRAGMA table_info(?)"
        return self.execute_query(query, (table_name,))
    
    def get_table_count(self, table_name: str) -> int:
        """Obtiene el número de filas en una tabla"""
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query)
        return result[0][0] if result else 0


# Instancia global para usar en toda la aplicación
db_connection = DatabaseConnection()


def get_connection() -> sqlite3.Connection:
    """Función helper para obtener una conexión"""
    return db_connection.get_connection()


def get_cursor():
    """Función helper para obtener un cursor con context manager"""
    return db_connection.get_cursor()


def execute_query(query: str, params: tuple = ()) -> list:
    """Función helper para ejecutar consultas SELECT"""
    return db_connection.execute_query(query, params)


def execute_update(query: str, params: tuple = ()) -> int:
    """Función helper para ejecutar consultas INSERT/UPDATE/DELETE"""
    return db_connection.execute_update(query, params)

