"""
Configuración centralizada para la base de datos
"""
import os

# Ruta de la base de datos principal
DB_PATH = os.path.join(os.path.dirname(__file__), "empleados.db")

# Configuración de la base de datos
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
