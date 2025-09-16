#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de registros manuales
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.access_management_service import access_service
from database.database_manager import DatabaseManager

def test_registro_manual():
    """Prueba la funcionalidad de registros manuales"""
    
    print("🧪 Probando funcionalidad de registros manuales...")
    
    # 1. Inicializar la base de datos
    db_manager = DatabaseManager()
    db_manager.init_database()
    print("✅ Base de datos inicializada")
    
    # 2. Crear empleado de prueba
    test_sid = "S9999999"
    
    # Limpiar datos previos
    conn = access_service.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM headcount WHERE scotia_id = ?', (test_sid,))
    cursor.execute('DELETE FROM historico WHERE scotia_id = ?', (test_sid,))
    conn.commit()
    conn.close()
    
    # Crear empleado de prueba
    empleado = {
        'scotia_id': test_sid,
        'employee': test_sid,
        'full_name': 'Empleado Prueba Manual',
        'email': 'prueba.manual@empresa.com',
        'position': 'ANALISTA',
        'unit': 'TECNOLOGÍA',
        'activo': True
    }
    
    success, message = access_service.create_employee(empleado)
    if not success:
        print(f"❌ Error creando empleado de prueba: {message}")
        return False
    
    print("✅ Empleado de prueba creado")
    
    # 3. Probar creación de registro manual
    print("\n📝 Probando creación de registro manual...")
    
    success, message = access_service.create_manual_access_record(
        scotia_id=test_sid,
        app_name="SAP_TEST",
        responsible="Usuario Prueba",
        description="Acceso de prueba para verificar funcionalidad manual"
    )
    
    if success:
        print("✅ Registro manual creado exitosamente")
        print(f"   Mensaje: {message}")
    else:
        print(f"❌ Error creando registro manual: {message}")
        return False
    
    # 4. Verificar que el registro se creó en el historial
    print("\n🔍 Verificando registro en el historial...")
    
    history = access_service.get_employee_history(test_sid)
    manual_records = [h for h in history if h.get('process_access') == 'manual_access']
    
    if manual_records:
        print(f"✅ Se encontraron {len(manual_records)} registros manuales")
        for record in manual_records:
            print(f"   - Aplicación: {record.get('app_access_name', 'N/A')}")
            print(f"   - Estado: {record.get('status', 'N/A')}")
            print(f"   - Descripción: {record.get('event_description', 'N/A')}")
    else:
        print("❌ No se encontraron registros manuales en el historial")
        return False
    
    # 5. Probar obtención de aplicaciones disponibles
    print("\n📋 Probando obtención de aplicaciones disponibles...")
    
    applications = access_service.get_available_applications()
    if applications:
        print(f"✅ Se encontraron {len(applications)} aplicaciones disponibles")
        print("   Aplicaciones (primeras 5):")
        for app in applications[:5]:
            print(f"   - {app.get('name', 'N/A')}")
    else:
        print("⚠️ No se encontraron aplicaciones disponibles")
    
    # 6. Probar validación de empleado inexistente
    print("\n❌ Probando validación con empleado inexistente...")
    
    success, message = access_service.create_manual_access_record(
        scotia_id="S0000000",  # Empleado que no existe
        app_name="SAP_TEST",
        responsible="Usuario Prueba"
    )
    
    if not success and "no encontrado" in message.lower():
        print("✅ Validación funcionando correctamente - empleado inexistente rechazado")
    else:
        print(f"❌ Error en validación: {message}")
        return False
    
    return True

def cleanup_test_data():
    """Limpia los datos de prueba"""
    try:
        conn = access_service.get_connection()
        cursor = conn.cursor()
        
        test_sid = "S9999999"
        cursor.execute('DELETE FROM headcount WHERE scotia_id = ?', (test_sid,))
        cursor.execute('DELETE FROM historico WHERE scotia_id = ?', (test_sid,))
        
        conn.commit()
        conn.close()
        print("🧹 Datos de prueba limpiados")
        
    except Exception as e:
        print(f"⚠️ Error limpiando datos: {e}")

if __name__ == "__main__":
    try:
        success = test_registro_manual()
        
        if success:
            print("\n🎉 ¡PRUEBA EXITOSA! La funcionalidad de registros manuales funciona correctamente:")
            print("   ✅ Creación de registros manuales")
            print("   ✅ Validación de empleados")
            print("   ✅ Obtención de aplicaciones disponibles")
            print("   ✅ Registro en historial con tipo 'manual_access'")
            print("   ✅ Validación de empleados inexistentes")
        else:
            print("\n❌ PRUEBA FALLIDA: La funcionalidad de registros manuales no funciona correctamente")
            
    finally:
        cleanup_test_data()
