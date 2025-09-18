#!/usr/bin/env python3
"""
Script para probar la configuración de SQL Server
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from access_management_service import AccessManagementService
from config import is_sql_server, get_database_config

def test_sql_server_config():
    """Prueba la configuración de SQL Server"""
    
    print("=== PRUEBA DE CONFIGURACIÓN DE SQL SERVER ===")
    
    # Verificar configuración
    print(f"\n1. CONFIGURACIÓN ACTUAL:")
    print(f"   Usando SQL Server: {is_sql_server()}")
    config = get_database_config()
    print(f"   Configuración: {config}")
    
    # Probar conexión
    print(f"\n2. PROBANDO CONEXIÓN:")
    try:
        service = AccessManagementService()
        print("   ✅ AccessManagementService creado exitosamente")
        
        # Probar conexión
        conn = service.get_connection()
        print("   ✅ Conexión a la base de datos exitosa")
        
        # Probar consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"   ✅ Consulta de prueba exitosa: {result[0]}")
        
        conn.close()
        print("   ✅ Conexión cerrada correctamente")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Probar funcionalidad básica
    print(f"\n3. PROBANDO FUNCIONALIDAD BÁSICA:")
    try:
        # Obtener estadísticas
        stats = service.db_manager.get_database_stats()
        print(f"   ✅ Estadísticas obtenidas: {stats}")
        
        # Obtener empleados
        employees = service.get_all_employees()
        print(f"   ✅ Empleados obtenidos: {len(employees)} registros")
        
        # Obtener aplicaciones
        applications = service.get_all_applications()
        print(f"   ✅ Aplicaciones obtenidas: {len(applications)} registros")
        
    except Exception as e:
        print(f"   ❌ Error en funcionalidad básica: {e}")
        return False
    
    print(f"\n4. RESULTADO FINAL:")
    print("   ✅ Configuración de SQL Server funcionando correctamente")
    print("   ✅ Todas las pruebas pasaron exitosamente")
    
    return True

if __name__ == "__main__":
    success = test_sql_server_config()
    if success:
        print("\n🎉 ¡Configuración de SQL Server lista para usar!")
    else:
        print("\n❌ Hay problemas con la configuración de SQL Server")
