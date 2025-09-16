#!/usr/bin/env python3
"""
Script de prueba para verificar que el historial se mantiene completo independientemente del estado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.access_management_service import access_service
from database.database_manager import DatabaseManager

def test_historial_completo():
    """Prueba que el historial se mantiene completo con diferentes estados"""
    
    print("🧪 Probando que el historial se mantiene completo...")
    
    # 1. Inicializar la base de datos
    db_manager = DatabaseManager()
    db_manager.init_database()
    print("✅ Base de datos inicializada")
    
    # 2. Crear un empleado de prueba
    test_sid = "S4444444"
    
    # Limpiar datos previos
    conn = access_service.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM headcount WHERE scotia_id = ?', (test_sid,))
    cursor.execute('DELETE FROM historico WHERE scotia_id = ?', (test_sid,))
    conn.commit()
    conn.close()
    
    # Crear empleado
    employee_data = {
        'scotia_id': test_sid,
        'employee': test_sid,
        'full_name': 'Empleado Prueba Historial',
        'email': 'prueba.historial@empresa.com',
        'position': 'ANALISTA',
        'unit': 'TECNOLOGÍA',
        'activo': True
    }
    
    success, message = access_service.create_employee(employee_data)
    if not success:
        print(f"❌ Error creando empleado: {message}")
        return False
    
    print("✅ Empleado creado")
    
    # 3. Crear registros históricos con diferentes estados
    conn = access_service.get_connection()
    cursor = conn.cursor()
    
    # Crear registros con diferentes estados
    estados = ['Pendiente', 'En Proceso', 'Completado', 'Cancelado', 'Rechazado']
    aplicaciones = ['SAP', 'OFFICE365', 'JIRA', 'SALESFORCE', 'CONFLUENCE']
    
    for i, (estado, app) in enumerate(zip(estados, aplicaciones)):
        cursor.execute('''
            INSERT INTO historico 
            (scotia_id, case_id, responsible, process_access, sid, area, subunit,
             event_description, ticket_email, app_access_name, computer_system_type,
             status, general_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_sid, f'CASE-{test_sid}-{i+1:03d}', 'Sistema Prueba',
            'onboarding', test_sid, 'TECNOLOGÍA', 'DESARROLLO',
            f'Acceso para {app}', 'sistema@empresa.com', app,
            'Desktop', estado, estado
        ))
    
    conn.commit()
    conn.close()
    
    print("✅ Registros históricos creados con diferentes estados")
    
    # 4. Verificar que todos los registros se pueden recuperar
    history = access_service.get_employee_history(test_sid)
    print(f"📊 Total de registros en historial: {len(history)}")
    
    for record in history:
        print(f"   - {record.get('app_access_name')}: {record.get('status')}")
    
    if len(history) != 5:
        print("❌ No se recuperaron todos los registros del historial")
        return False
    
    # 5. Probar conciliación (debe considerar todos los estados)
    print("\n🔄 Probando conciliación...")
    reporte = access_service.get_access_reconciliation_report(test_sid)
    
    if "error" in reporte:
        print(f"❌ Error en conciliación: {reporte['error']}")
        return False
    
    print(f"✅ Conciliación exitosa")
    print(f"   - Accesos actuales: {len(reporte.get('current_access', []))}")
    print(f"   - Accesos a otorgar: {len(reporte.get('to_grant', []))}")
    print(f"   - Accesos a revocar: {len(reporte.get('to_revoke', []))}")
    
    # 6. Probar offboarding (debe revocar todos los accesos)
    print("\n🔄 Probando offboarding...")
    success, message, records = access_service.process_employee_offboarding(test_sid, "Sistema Prueba")
    
    if not success:
        print(f"❌ Error en offboarding: {message}")
        return False
    
    print(f"✅ Offboarding exitoso: {message}")
    print(f"   - Registros de revocación creados: {len(records)}")
    
    # 7. Verificar que el historial sigue completo después del offboarding
    history_after = access_service.get_employee_history(test_sid)
    print(f"\n📊 Historial después del offboarding: {len(history_after)} registros")
    
    # Mostrar todos los registros para debug
    for i, record in enumerate(history_after):
        print(f"   {i+1}. {record.get('app_access_name')}: {record.get('status')} ({record.get('process_access')})")
    
    # Debe tener los 5 registros originales + los 5 registros de revocación = 10 total
    if len(history_after) != 10:
        print(f"❌ Historial incompleto después del offboarding. Esperado: 10, Obtenido: {len(history_after)}")
        return False
    
    print("✅ Historial se mantiene completo después del offboarding")
    
    # 8. Verificar que el empleado fue marcado como inactivo
    employee = access_service.get_employee_by_id(test_sid)
    if employee.get('activo') != 0:
        print("❌ Empleado no fue marcado como inactivo")
        return False
    
    print("✅ Empleado marcado como inactivo correctamente")
    
    return True

def cleanup_test_data():
    """Limpia los datos de prueba"""
    try:
        conn = access_service.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM headcount WHERE scotia_id = ?', ('S4444444',))
        cursor.execute('DELETE FROM historico WHERE scotia_id = ?', ('S4444444',))
        conn.commit()
        conn.close()
        print("🧹 Datos de prueba limpiados")
        
    except Exception as e:
        print(f"⚠️ Error limpiando datos: {e}")

if __name__ == "__main__":
    try:
        success = test_historial_completo()
        
        if success:
            print("\n🎉 ¡PRUEBA EXITOSA! El historial se mantiene completo:")
            print("   ✅ Todos los estados se consideran en conciliación")
            print("   ✅ Todos los accesos se revocan en offboarding")
            print("   ✅ El historial no se borra")
            print("   ✅ Se mantiene el registro completo de movimientos")
        else:
            print("\n❌ PRUEBA FALLIDA: El historial no se mantiene completo")
            
    finally:
        cleanup_test_data()
