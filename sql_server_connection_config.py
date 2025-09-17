#!/usr/bin/env python3
"""
Configuración de conexión para SQL Server
Reemplaza la configuración de SQLite por SQL Server
"""
import pyodbc
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import sys
import os

# Configuración de conexión a SQL Server
SQL_SERVER_CONFIG = {
    'server': 'localhost',  # Cambiar por tu servidor SQL Server
    'database': 'GAMLO_Empleados',
    'username': 'sa',  # Cambiar por tu usuario
    'password': 'TuPassword123!',  # Cambiar por tu contraseña
    'driver': '{ODBC Driver 17 for SQL Server}',  # Ajustar según tu versión
    'trusted_connection': 'no',  # Cambiar a 'yes' si usas autenticación de Windows
    'timeout': 30
}

class SQLServerDatabaseManager:
    """Gestor de base de datos para SQL Server"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or SQL_SERVER_CONFIG
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        """Construye la cadena de conexión para SQL Server"""
        if self.config.get('trusted_connection', 'no').lower() == 'yes':
            # Autenticación de Windows
            return (
                f"DRIVER={self.config['driver']};"
                f"SERVER={self.config['server']};"
                f"DATABASE={self.config['database']};"
                f"Trusted_Connection=yes;"
                f"Timeout={self.config['timeout']};"
            )
        else:
            # Autenticación SQL Server
            return (
                f"DRIVER={self.config['driver']};"
                f"SERVER={self.config['server']};"
                f"DATABASE={self.config['database']};"
                f"UID={self.config['username']};"
                f"PWD={self.config['password']};"
                f"Timeout={self.config['timeout']};"
            )
    
    def get_connection(self) -> pyodbc.Connection:
        """Obtiene una conexión a la base de datos SQL Server"""
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            print(f"Error conectando a SQL Server: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Prueba la conexión a la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()
            return result[0] == 1
        except Exception as e:
            print(f"Error probando conexión: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            stats = {}
            
            # Ejecutar procedimiento almacenado para obtener estadísticas
            cursor.execute("EXEC sp_GetDatabaseStats")
            rows = cursor.fetchall()
            
            for row in rows:
                stats[row[0]] = row[1]
            
            conn.close()
            return stats
            
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def execute_query(self, query: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """Ejecuta una consulta y retorna los resultados como lista de diccionarios"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obtener nombres de columnas
            columns = [column[0] for column in cursor.description]
            
            # Obtener resultados
            rows = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            return []
    
    def execute_non_query(self, query: str, params: Tuple = None) -> bool:
        """Ejecuta una consulta que no retorna resultados (INSERT, UPDATE, DELETE)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            return False

# Función para migrar desde SQLite a SQL Server
def migrate_from_sqlite_to_sqlserver(sqlite_db_path: str, sql_server_config: Dict[str, Any] = None):
    """Migra datos desde SQLite a SQL Server"""
    try:
        import sqlite3
        
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Conectar a SQL Server
        sql_server_manager = SQLServerDatabaseManager(sql_server_config)
        sql_server_conn = sql_server_manager.get_connection()
        sql_server_cursor = sql_server_conn.cursor()
        
        # Migrar headcount
        print("Migrando tabla headcount...")
        sqlite_cursor.execute("SELECT * FROM headcount")
        headcount_rows = sqlite_cursor.fetchall()
        
        for row in headcount_rows:
            sql_server_cursor.execute("""
                INSERT INTO headcount 
                (scotia_id, employee, full_name, email, position, manager, senior_manager, 
                 unit, start_date, ceco, skip_level, cafe_alcides, parents, personal_email, 
                 size, birthday, validacion, activo, inactivation_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row)
        
        # Migrar applications
        print("Migrando tabla applications...")
        sqlite_cursor.execute("SELECT * FROM applications")
        applications_rows = sqlite_cursor.fetchall()
        
        for row in applications_rows:
            sql_server_cursor.execute("""
                INSERT INTO applications 
                (jurisdiction, unit, subunit, logical_access_name, alias, path_email_url, 
                 position_role, exception_tracking, fulfillment_action, system_owner, 
                 role_name, access_type, category, additional_data, ad_code, access_status, 
                 last_update_date, require_licensing, description, authentication_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row[1:])  # Saltar el ID autoincremental
        
        # Migrar historico
        print("Migrando tabla historico...")
        sqlite_cursor.execute("SELECT * FROM historico")
        historico_rows = sqlite_cursor.fetchall()
        
        for row in historico_rows:
            sql_server_cursor.execute("""
                INSERT INTO historico 
                (scotia_id, case_id, responsible, record_date, request_date, process_access, 
                 sid, area, subunit, event_description, ticket_email, app_access_name, 
                 computer_system_type, status, closing_date_app, closing_date_ticket, 
                 app_quality, confirmation_by_user, comment, ticket_quality, general_status, 
                 average_time_open_ticket)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row[1:])  # Saltar el ID autoincremental
        
        # Migrar procesos
        print("Migrando tabla procesos...")
        sqlite_cursor.execute("SELECT * FROM procesos")
        procesos_rows = sqlite_cursor.fetchall()
        
        for row in procesos_rows:
            sql_server_cursor.execute("""
                INSERT INTO procesos 
                (sid, nueva_sub_unidad, nuevo_cargo, status, request_date, ingreso_por, 
                 fecha_creacion, fecha_actualizacion, tipo_proceso, app_name, mail, 
                 closing_date_app, app_quality, confirmation_by_user, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row[1:])  # Saltar el ID autoincremental
        
        # Confirmar cambios
        sql_server_conn.commit()
        
        # Cerrar conexiones
        sqlite_conn.close()
        sql_server_conn.close()
        
        print("✅ Migración completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

# Función para actualizar el access_management_service.py para usar SQL Server
def update_access_service_for_sqlserver():
    """Actualiza el archivo access_management_service.py para usar SQL Server"""
    
    # Leer el archivo actual
    with open('services/access_management_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar las importaciones y configuración
    new_content = content.replace(
        'import sqlite3',
        'import pyodbc\nfrom sql_server_connection_config import SQLServerDatabaseManager'
    )
    
    new_content = new_content.replace(
        'from database_manager import DatabaseManager',
        '# from database_manager import DatabaseManager  # Comentado para SQL Server'
    )
    
    new_content = new_content.replace(
        'self.db_manager = DatabaseManager()',
        'self.db_manager = SQLServerDatabaseManager()'
    )
    
    new_content = new_content.replace(
        'def get_connection(self) -> sqlite3.Connection:',
        'def get_connection(self) -> pyodbc.Connection:'
    )
    
    new_content = new_content.replace(
        'return self.db_manager.get_connection()',
        'return self.db_manager.get_connection()'
    )
    
    # Escribir el archivo actualizado
    with open('services/access_management_service_sqlserver.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Archivo access_management_service_sqlserver.py creado")

if __name__ == "__main__":
    print("=== CONFIGURACIÓN DE SQL SERVER ===")
    
    # Probar conexión
    manager = SQLServerDatabaseManager()
    if manager.test_connection():
        print("✅ Conexión a SQL Server exitosa")
        
        # Mostrar estadísticas
        stats = manager.get_database_stats()
        print("\n📊 Estadísticas de la base de datos:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Error conectando a SQL Server")
        print("Verifica la configuración en SQL_SERVER_CONFIG")
    
    # Opcional: Migrar desde SQLite
    if len(sys.argv) > 1 and sys.argv[1] == '--migrate':
        sqlite_path = input("Ruta del archivo SQLite (empleados.db): ")
        if os.path.exists(sqlite_path):
            migrate_from_sqlite_to_sqlserver(sqlite_path)
        else:
            print("❌ Archivo SQLite no encontrado")
    
    # Actualizar archivo de servicio
    update_access_service_for_sqlserver()
