#!/usr/bin/env python3
"""
Configuración del sistema
Permite elegir entre SQLite y SQL Server
"""
import os

# Configuración de la base de datos
# Cambiar a False para usar SQLite, True para usar SQL Server
USE_SQL_SERVER = False

# Configuración de SQL Server
SQL_SERVER_CONFIG = {
    'server': 'localhost',  # Cambiar por tu servidor SQL Server
    'database': 'GAMLO_Empleados',
    'username': 'sa',  # Cambiar por tu usuario
    'password': 'TuPassword123!',  # Cambiar por tu contraseña
    'driver': '{ODBC Driver 17 for SQL Server}',  # Ajustar según tu versión
    'trusted_connection': 'no',  # Cambiar a 'yes' si usas autenticación de Windows
    'timeout': 30
}

# Configuración de SQLite
SQLITE_CONFIG = {
    'database_path': 'database/empleados.db'
}

def get_database_config():
    """Retorna la configuración de la base de datos según la opción seleccionada"""
    if USE_SQL_SERVER:
        return SQL_SERVER_CONFIG
    else:
        return SQLITE_CONFIG

def is_sql_server():
    """Retorna True si se está usando SQL Server, False si se usa SQLite"""
    return USE_SQL_SERVER
