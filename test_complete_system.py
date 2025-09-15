#!/usr/bin/env python3
"""
Script de pruebas exhaustivas para verificar que todo el sistema funciona correctamente
"""
import sys
import os
import traceback

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

from services import access_service, export_service, history_service, search_service

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("=== Prueba 1: Conexión a Base de Datos ===")
    try:
        conn = access_service.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM headcount")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Conexión exitosa. Empleados en BD: {count}")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_employee_operations():
    """Prueba las operaciones con empleados"""
    print("\n=== Prueba 2: Operaciones con Empleados ===")
    try:
        # Obtener todos los empleados
        empleados = access_service.get_all_employees()
        print(f"✅ Empleados obtenidos: {len(empleados)}")
        
        if empleados:
            # Probar con el primer empleado
            empleado = empleados[0]
            sid = empleado.get('scotia_id')
            print(f"✅ Empleado de prueba: {sid} - {empleado.get('full_name')}")
            
            # Obtener empleado por ID
            empleado_por_id = access_service.get_employee_by_id(sid)
            if empleado_por_id:
                print(f"✅ Empleado obtenido por ID: {empleado_por_id.get('full_name')}")
            else:
                print("❌ No se pudo obtener empleado por ID")
                return False
        else:
            print("❌ No hay empleados en la base de datos")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error en operaciones de empleados: {e}")
        traceback.print_exc()
        return False

def test_applications_operations():
    """Prueba las operaciones con aplicaciones"""
    print("\n=== Prueba 3: Operaciones con Aplicaciones ===")
    try:
        # Obtener todas las aplicaciones
        aplicaciones = access_service.get_all_applications()
        print(f"✅ Aplicaciones obtenidas: {len(aplicaciones)}")
        
        if aplicaciones:
            # Probar con la primera aplicación
            app = aplicaciones[0]
            print(f"✅ Aplicación de prueba: {app.get('logical_access_name')} - {app.get('unit')}")
        else:
            print("❌ No hay aplicaciones en la base de datos")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error en operaciones de aplicaciones: {e}")
        traceback.print_exc()
        return False

def test_reconciliation_system():
    """Prueba el sistema de conciliación"""
    print("\n=== Prueba 4: Sistema de Conciliación ===")
    try:
        # Usar el empleado S7457774 que configuramos
        sid = 'S7457774'
        
        # Ejecutar conciliación
        reporte = access_service.get_access_reconciliation_report(sid)
        
        if "error" in reporte:
            print(f"❌ Error en conciliación: {reporte['error']}")
            return False
        
        # Verificar estructura del reporte
        required_keys = ['employee', 'current_access', 'to_grant', 'to_revoke', 'summary']
        for key in required_keys:
            if key not in reporte:
                print(f"❌ Falta clave en reporte: {key}")
                return False
        
        print(f"✅ Estructura del reporte correcta: {list(reporte.keys())}")
        
        # Verificar datos del empleado
        employee = reporte.get('employee', {})
        print(f"✅ Empleado: {employee.get('scotia_id')} - {employee.get('full_name')}")
        print(f"✅ Posición: {employee.get('position')} - Unidad: {employee.get('unit')}")
        
        # Verificar accesos
        current_access = reporte.get('current_access', [])
        to_grant = reporte.get('to_grant', [])
        to_revoke = reporte.get('to_revoke', [])
        
        print(f"✅ Accesos actuales: {len(current_access)}")
        for acceso in current_access:
            print(f"   - {acceso.get('app_name', 'N/A')} ({acceso.get('unit', 'N/A')})")
        
        print(f"✅ Accesos a otorgar: {len(to_grant)}")
        for acceso in to_grant:
            print(f"   - {acceso.get('app_name', 'N/A')} ({acceso.get('unit', 'N/A')})")
        
        print(f"✅ Accesos a revocar: {len(to_revoke)}")
        for acceso in to_revoke:
            print(f"   - {acceso.get('app_name', 'N/A')} ({acceso.get('unit', 'N/A')})")
        
        # Verificar que hay datos para mostrar
        if not current_access and not to_grant and not to_revoke:
            print("⚠️ No hay accesos para mostrar en la tabla")
            return False
        
        print("✅ Sistema de conciliación funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en sistema de conciliación: {e}")
        traceback.print_exc()
        return False

def test_export_functionality():
    """Prueba la funcionalidad de exportación"""
    print("\n=== Prueba 5: Funcionalidad de Exportación ===")
    try:
        # Obtener datos de conciliación
        sid = 'S7457774'
        reporte = access_service.get_access_reconciliation_report(sid)
        
        if "error" in reporte:
            print(f"❌ Error obteniendo reporte: {reporte['error']}")
            return False
        
        # Adaptar datos para exportación (simulando lo que hace la UI)
        employee = reporte.get('employee', {})
        current_access = reporte.get('current_access', [])
        to_grant = reporte.get('to_grant', [])
        to_revoke = reporte.get('to_revoke', [])
        
        adapted_data = {
            "person_info": {
                "sid": employee.get('scotia_id', ''),
                "area": employee.get('unit', ''),
                "subunit": employee.get('subunit', ''),
                "cargo": employee.get('position', '')
            },
            "current": current_access,
            "target": [],
            "to_grant": [{
                "sid": sid,
                "app_name": acceso.get('app_name', ''),
                "role_name": acceso.get('role_name', ''),
                "accion": "GRANT",
                "motivo": f"Acceso requerido para {acceso.get('app_name', '')}"
            } for acceso in to_grant],
            "to_revoke": [{
                "sid": sid,
                "app_name": acceso.get('app_name', ''),
                "role_name": acceso.get('role_name', ''),
                "accion": "REVOKE",
                "motivo": f"Acceso excesivo para {acceso.get('app_name', '')}"
            } for acceso in to_revoke]
        }
        
        # Exportar a Excel
        output_path = export_service.export_reconciliation_tickets(
            [adapted_data],
            "Sistema de Pruebas"
        )
        
        # Verificar que el archivo se creó
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Archivo Excel exportado exitosamente: {output_path}")
            print(f"✅ Tamaño del archivo: {file_size} bytes")
            return True
        else:
            print(f"❌ El archivo no se creó: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error en exportación: {e}")
        traceback.print_exc()
        return False

def test_history_service():
    """Prueba el servicio de historial"""
    print("\n=== Prueba 6: Servicio de Historial ===")
    try:
        # Obtener historial de un empleado
        sid = 'S7457774'
        historial = access_service.get_employee_history(sid)
        print(f"✅ Historial obtenido: {len(historial)} registros")
        
        if historial:
            for i, h in enumerate(historial[:3]):  # Mostrar primeros 3
                print(f"   {i+1}. {h.get('app_access_name', 'N/A')} - {h.get('area', 'N/A')} - {h.get('status', 'N/A')}")
        
        # Probar registro de tickets
        reporte = access_service.get_access_reconciliation_report(sid)
        if "error" not in reporte:
            resultado = history_service.register_reconciliation_tickets(
                reporte, "Sistema de Pruebas"
            )
            tickets_creados = resultado.get('tickets_created', 0)
            print(f"✅ Tickets registrados: {tickets_creados}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicio de historial: {e}")
        traceback.print_exc()
        return False

def test_search_service():
    """Prueba el servicio de búsqueda"""
    print("\n=== Prueba 7: Servicio de Búsqueda ===")
    try:
        # Buscar empleados
        empleados = search_service.obtener_todo_headcount()
        print(f"✅ Búsqueda de empleados: {len(empleados)} encontrados")
        
        if empleados:
            # Buscar por SID específico
            sid = 'S7457774'
            resultados = search_service.buscar_headcount_por_sid(sid)
            if resultados:
                print(f"✅ Búsqueda por SID exitosa: {resultados[0].get('full_name')}")
            else:
                print(f"❌ No se encontró empleado con SID: {sid}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicio de búsqueda: {e}")
        traceback.print_exc()
        return False

def test_ui_components():
    """Prueba los componentes de la UI (simulación)"""
    print("\n=== Prueba 8: Componentes de UI (Simulación) ===")
    try:
        # Simular datos que recibiría la UI
        sid = 'S7457774'
        reporte = access_service.get_access_reconciliation_report(sid)
        
        if "error" in reporte:
            print(f"❌ Error obteniendo datos para UI: {reporte['error']}")
            return False
        
        # Simular _mostrar_resultados_nuevos
        current_access = reporte.get('current_access', [])
        to_grant = reporte.get('to_grant', [])
        to_revoke = reporte.get('to_revoke', [])
        
        print(f"✅ Datos para tabla de conciliación:")
        print(f"   - Accesos actuales: {len(current_access)}")
        print(f"   - Accesos a otorgar: {len(to_grant)}")
        print(f"   - Accesos a revocar: {len(to_revoke)}")
        
        # Verificar que hay datos para mostrar
        total_items = len(current_access) + len(to_grant) + len(to_revoke)
        if total_items > 0:
            print(f"✅ La tabla tendría {total_items} elementos para mostrar")
        else:
            print("⚠️ La tabla estaría vacía")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en componentes de UI: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS EXHAUSTIVAS DEL SISTEMA")
    print("=" * 60)
    
    tests = [
        test_database_connection,
        test_employee_operations,
        test_applications_operations,
        test_reconciliation_system,
        test_export_functionality,
        test_history_service,
        test_search_service,
        test_ui_components
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error inesperado en {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"✅ Pruebas exitosas: {passed}")
    print(f"❌ Pruebas fallidas: {failed}")
    print(f"📈 Porcentaje de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema está funcionando correctamente.")
    else:
        print(f"\n⚠️ {failed} pruebas fallaron. Revisar los errores arriba.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
