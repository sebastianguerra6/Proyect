#!/usr/bin/env python3
"""
Script para cambiar entre SQLite y SQL Server
"""
import os

def cambiar_base_datos():
    """Permite cambiar entre SQLite y SQL Server"""
    
    print("=== CONFIGURACIÓN DE BASE DE DATOS ===")
    print("1. SQLite (por defecto, no requiere instalación)")
    print("2. SQL Server (requiere instalación y configuración)")
    
    while True:
        opcion = input("\nSelecciona una opción (1 o 2): ").strip()
        
        if opcion == "1":
            configurar_sqlite()
            break
        elif opcion == "2":
            configurar_sql_server()
            break
        else:
            print("❌ Opción inválida. Por favor selecciona 1 o 2.")

def configurar_sqlite():
    """Configura la aplicación para usar SQLite"""
    print("\n=== CONFIGURANDO SQLITE ===")
    
    # Leer archivo config.py
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cambiar USE_SQL_SERVER = True a False
    new_content = content.replace('USE_SQL_SERVER = True', 'USE_SQL_SERVER = False')
    
    # Escribir archivo actualizado
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Configuración actualizada para usar SQLite")
    print("✅ La aplicación usará la base de datos SQLite existente")
    print("✅ No se requiere instalación adicional")

def configurar_sql_server():
    """Configura la aplicación para usar SQL Server"""
    print("\n=== CONFIGURANDO SQL SERVER ===")
    
    # Verificar si pyodbc está instalado
    try:
        import pyodbc
        print("✅ pyodbc está instalado")
    except ImportError:
        print("❌ pyodbc no está instalado")
        print("   Instala con: pip install pyodbc")
        return
    
    # Leer archivo config.py
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cambiar USE_SQL_SERVER = False a True
    new_content = content.replace('USE_SQL_SERVER = False', 'USE_SQL_SERVER = True')
    
    # Escribir archivo actualizado
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Configuración actualizada para usar SQL Server")
    print("⚠️  IMPORTANTE: Debes configurar la conexión en config.py")
    print("⚠️  IMPORTANTE: Debes ejecutar sql_server_setup.sql en SQL Server")
    print("⚠️  IMPORTANTE: Debes instalar ODBC Driver 17 for SQL Server")

def verificar_configuracion():
    """Verifica la configuración actual"""
    print("\n=== CONFIGURACIÓN ACTUAL ===")
    
    try:
        from config import is_sql_server, get_database_config
        
        if is_sql_server():
            print("📊 Base de datos: SQL Server")
            config = get_database_config()
            print(f"   Servidor: {config['server']}")
            print(f"   Base de datos: {config['database']}")
            print(f"   Usuario: {config['username']}")
        else:
            print("📊 Base de datos: SQLite")
            config = get_database_config()
            print(f"   Archivo: {config['database_path']}")
            
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")

def probar_conexion():
    """Prueba la conexión a la base de datos"""
    print("\n=== PROBANDO CONEXIÓN ===")
    
    try:
        from services.access_management_service import AccessManagementService
        
        service = AccessManagementService()
        conn = service.get_connection()
        
        # Probar consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        
        conn.close()
        
        print("✅ Conexión exitosa")
        print(f"✅ Consulta de prueba: {result[0]}")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🔧 CONFIGURADOR DE BASE DE DATOS")
    print("=" * 40)
    
    verificar_configuracion()
    
    while True:
        print("\n=== MENÚ ===")
        print("1. Cambiar a SQLite")
        print("2. Cambiar a SQL Server")
        print("3. Verificar configuración actual")
        print("4. Probar conexión")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            configurar_sqlite()
        elif opcion == "2":
            configurar_sql_server()
        elif opcion == "3":
            verificar_configuracion()
        elif opcion == "4":
            probar_conexion()
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Por favor selecciona 1-5.")
