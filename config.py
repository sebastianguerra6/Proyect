#!/usr/bin/env python3
"""
Configuración unificada del sistema
Permite elegir entre SQLite y SQL Server con gestión completa de conexiones
"""
import os
import pyodbc
import sqlite3
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

# =====================================================
# CONFIGURACIÓN PRINCIPAL
# =====================================================

# Configuración de la base de datos
# Cambiar a False para usar SQLite, True para usar SQL Server
USE_SQL_SERVER = False

# Configuración de SQL Server
SQL_SERVER_CONFIG = {
    'server': 'localhost',  # Cambiar por tu servidor SQL Server
    'database': 'GAMLO_Empleados',
    'username': '',  # No necesario con Windows Authentication
    'password': '',  # No necesario con Windows Authentication
    'driver': '{ODBC Driver 17 for SQL Server}',  # Ajustar según tu versión
    'trusted_connection': 'yes',  # Usar Windows Authentication
    'timeout': 30
}

# Configuración de SQLite
SQLITE_CONFIG = {
    'database_path': 'database/empleados.db'
}

# =====================================================
# GESTORES DE BASE DE DATOS
# =====================================================

class SQLServerConnection:
    """Clase simple para conexiones a SQL Server"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or SQL_SERVER_CONFIG
        self.connection_string = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        """Construye la cadena de conexión para SQL Server"""
        if self.config.get('trusted_connection', 'no').lower() == 'yes':
            # Autenticación de Windows (Trusted Connection)
            return (
                f"DRIVER={self.config['driver']};"
                f"SERVER={self.config['server']};"
                f"DATABASE={self.config['database']};"
                f"Trusted_Connection=yes;"
                f"Timeout={self.config['timeout']};"
            )
        else:
            # Autenticación SQL Server con usuario y contraseña
            if not self.config.get('username') or not self.config.get('password'):
                raise ValueError("Username y password son requeridos para autenticación SQL Server")
            
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

class SQLiteConnection:
    """Clase simple para conexiones a SQLite"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or SQLITE_CONFIG
        self.database_path = self.config['database_path']
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos SQLite"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
            return sqlite3.connect(self.database_path)
        except sqlite3.Error as e:
            print(f"Error conectando a SQLite: {e}")
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

# =====================================================
# FUNCIONES DE CONFIGURACIÓN
# =====================================================

def get_database_config():
    """Retorna la configuración de la base de datos según la opción seleccionada"""
    if USE_SQL_SERVER:
        return SQL_SERVER_CONFIG
    else:
        return SQLITE_CONFIG

def is_sql_server():
    """Retorna True si se está usando SQL Server, False si se usa SQLite"""
    return USE_SQL_SERVER

def get_database_connection():
    """Retorna la clase de conexión apropiada según la configuración"""
    if USE_SQL_SERVER:
        return SQLServerConnection()
    else:
        return SQLiteConnection()

def switch_to_sql_server():
    """Cambia la configuración para usar SQL Server con Windows Authentication"""
    global USE_SQL_SERVER
    USE_SQL_SERVER = True
    print("✅ Configuración cambiada a SQL Server con Windows Authentication")
    print("🔐 Se usará la autenticación de Windows del usuario actual")

def switch_to_sqlite():
    """Cambia la configuración para usar SQLite"""
    global USE_SQL_SERVER
    USE_SQL_SERVER = False
    print("✅ Configuración cambiada a SQLite")
    print("📁 Base de datos local: database/empleados.db")

def test_database_connection():
    """Prueba la conexión a la base de datos configurada"""
    connection = get_database_connection()
    return connection.test_connection()

# =====================================================
# FUNCIONES DE UTILIDAD
# =====================================================

def get_connection_info():
    """Retorna información sobre la configuración de conexión actual"""
    if USE_SQL_SERVER:
        config = SQL_SERVER_CONFIG
        return {
            'type': 'SQL Server',
            'server': config['server'],
            'database': config['database'],
            'authentication': 'Windows Authentication' if config['trusted_connection'] == 'yes' else 'SQL Server Authentication',
            'driver': config['driver']
        }
    else:
        config = SQLITE_CONFIG
        return {
            'type': 'SQLite',
            'database_path': config['database_path']
        }

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

if __name__ == "__main__":
    print("=== CONFIGURACIÓN DE CONEXIÓN ===")
    print(f"Base de datos configurada: {'SQL Server' if USE_SQL_SERVER else 'SQLite'}")
    
    if USE_SQL_SERVER:
        config = SQL_SERVER_CONFIG
        print(f"🔐 Autenticación: {'Windows Authentication' if config['trusted_connection'] == 'yes' else 'SQL Server Authentication'}")
        print(f"🖥️  Servidor: {config['server']}")
        print(f"🗄️  Base de datos: {config['database']}")
        print(f"⏱️  Timeout: {config['timeout']} segundos")
    else:
        config = SQLITE_CONFIG
        print(f"📁 Archivo de base de datos: {config['database_path']}")
    
    print("\n" + "="*50)
    
    # Probar conexión
    print("🔍 Probando conexión...")
    if test_database_connection():
        print("✅ Conexión a la base de datos exitosa")
        print("🎯 Sistema listo para usar")
    else:
        print("❌ Error conectando a la base de datos")
        print("\n🔧 Soluciones posibles:")
        if USE_SQL_SERVER:
            print("   - Verificar que SQL Server esté ejecutándose")
            print("   - Verificar que el usuario tenga permisos en la base de datos")
            print("   - Verificar la configuración del servidor y base de datos")
        else:
            print("   - Verificar que el archivo database/empleados.db exista")
            print("   - Verificar permisos de escritura en el directorio database/")
        
        print("\n💡 Para cambiar a SQLite: switch_to_sqlite()")
        print("💡 Para cambiar a SQL Server: switch_to_sql_server()")
