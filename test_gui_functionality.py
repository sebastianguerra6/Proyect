#!/usr/bin/env python3
"""
Script para probar la funcionalidad de la GUI sin abrir la ventana
"""
import sys
import os
import tkinter as tk
from unittest.mock import patch

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

def test_gui_initialization():
    """Prueba la inicialización de la GUI"""
    print("=== Prueba GUI: Inicialización ===")
    try:
        # Importar la aplicación principal
        from app_empleados_refactorizada import AppEmpleadosRefactorizada, ConciliacionFrame
        
        # Crear root de tkinter (sin mostrarlo)
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana
        
        # Inicializar la aplicación
        app = AppEmpleadosRefactorizada(root)
        print("✅ Aplicación principal inicializada correctamente")
        
        # Verificar que los componentes se crearon
        if hasattr(app, 'componentes'):
            print(f"✅ Componentes creados: {list(app.componentes.keys())}")
        else:
            print("❌ No se encontraron componentes")
            return False
        
        # Verificar componente de conciliación
        if 'conciliacion' in app.componentes:
            conciliacion = app.componentes['conciliacion']
            print("✅ Componente de conciliación creado")
            
            # Verificar que tiene los métodos necesarios
            required_methods = ['_conciliar_accesos', '_exportar_excel', '_mostrar_resultados_nuevos']
            for method in required_methods:
                if hasattr(conciliacion, method):
                    print(f"✅ Método {method} existe")
                else:
                    print(f"❌ Falta método {method}")
                    return False
        else:
            print("❌ No se encontró componente de conciliación")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en inicialización de GUI: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conciliacion_frame():
    """Prueba específica del frame de conciliación"""
    print("\n=== Prueba GUI: Frame de Conciliación ===")
    try:
        from app_empleados_refactorizada import ConciliacionFrame
        
        # Crear root de tkinter (sin mostrarlo)
        root = tk.Tk()
        root.withdraw()
        
        # Crear frame de conciliación
        conciliacion_frame = ConciliacionFrame(root)
        print("✅ Frame de conciliación creado")
        
        # Verificar que tiene las variables necesarias
        if hasattr(conciliacion_frame, 'sid_var'):
            print("✅ Variable sid_var existe")
        else:
            print("❌ Falta variable sid_var")
            return False
        
        if hasattr(conciliacion_frame, 'resultado_conciliacion'):
            print("✅ Variable resultado_conciliacion existe")
        else:
            print("❌ Falta variable resultado_conciliacion")
            return False
        
        # Verificar que tiene el treeview
        if hasattr(conciliacion_frame, 'tree_resultados'):
            print("✅ Treeview de resultados existe")
        else:
            print("❌ Falta treeview de resultados")
            return False
        
        # Simular conciliación
        conciliacion_frame.sid_var.set('S7457774')
        print("✅ SID configurado para prueba")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en frame de conciliación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conciliacion_logic():
    """Prueba la lógica de conciliación sin GUI"""
    print("\n=== Prueba GUI: Lógica de Conciliación ===")
    try:
        from app_empleados_refactorizada import ConciliacionFrame
        from services import access_service
        
        # Crear root de tkinter (sin mostrarlo)
        root = tk.Tk()
        root.withdraw()
        
        # Crear frame de conciliación
        conciliacion_frame = ConciliacionFrame(root)
        
        # Simular datos de entrada
        conciliacion_frame.sid_var.set('S7457774')
        
        # Obtener reporte de conciliación
        reporte = access_service.get_access_reconciliation_report('S7457774')
        
        if "error" in reporte:
            print(f"❌ Error en reporte: {reporte['error']}")
            return False
        
        # Simular mostrar resultados
        conciliacion_frame.resultado_conciliacion = reporte
        
        # Verificar que se pueden obtener los datos para la tabla
        current_access = reporte.get('current_access', [])
        to_grant = reporte.get('to_grant', [])
        to_revoke = reporte.get('to_revoke', [])
        
        print(f"✅ Datos para tabla obtenidos:")
        print(f"   - Accesos actuales: {len(current_access)}")
        print(f"   - Accesos a otorgar: {len(to_grant)}")
        print(f"   - Accesos a revocar: {len(to_revoke)}")
        
        # Simular adaptación de datos para exportación
        employee = reporte.get('employee', {})
        adapted_data = conciliacion_frame._adapt_data_for_export(reporte)
        
        if 'person_info' in adapted_data:
            print("✅ Datos adaptados para exportación correctamente")
        else:
            print("❌ Error adaptando datos para exportación")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en lógica de conciliación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_export_adaptation():
    """Prueba la adaptación de datos para exportación"""
    print("\n=== Prueba GUI: Adaptación para Exportación ===")
    try:
        from app_empleados_refactorizada import ConciliacionFrame
        from services import access_service, export_service
        
        # Crear root de tkinter (sin mostrarlo)
        root = tk.Tk()
        root.withdraw()
        
        # Crear frame de conciliación
        conciliacion_frame = ConciliacionFrame(root)
        conciliacion_frame.sid_var.set('S7457774')
        
        # Obtener reporte
        reporte = access_service.get_access_reconciliation_report('S7457774')
        
        if "error" in reporte:
            print(f"❌ Error en reporte: {reporte['error']}")
            return False
        
        # Adaptar datos
        adapted_data = conciliacion_frame._adapt_data_for_export(reporte)
        
        # Verificar estructura adaptada
        required_keys = ['person_info', 'current', 'target', 'to_grant', 'to_revoke']
        for key in required_keys:
            if key not in adapted_data:
                print(f"❌ Falta clave en datos adaptados: {key}")
                return False
        
        print("✅ Estructura de datos adaptados correcta")
        
        # Verificar datos del empleado
        person_info = adapted_data['person_info']
        if person_info.get('sid') == 'S7457774':
            print("✅ Datos del empleado correctos")
        else:
            print("❌ Datos del empleado incorrectos")
            return False
        
        # Probar exportación con datos adaptados
        output_path = export_service.export_reconciliation_tickets(
            [adapted_data],
            "Prueba GUI"
        )
        
        if os.path.exists(output_path):
            print(f"✅ Exportación exitosa: {output_path}")
        else:
            print(f"❌ Error en exportación: {output_path}")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en adaptación para exportación: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_gui_tests():
    """Ejecuta todas las pruebas de GUI"""
    print("🖥️ INICIANDO PRUEBAS DE INTERFAZ GRÁFICA")
    print("=" * 60)
    
    tests = [
        test_gui_initialization,
        test_conciliacion_frame,
        test_conciliacion_logic,
        test_export_adaptation
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
    print("📊 RESUMEN DE PRUEBAS GUI")
    print("=" * 60)
    print(f"✅ Pruebas exitosas: {passed}")
    print(f"❌ Pruebas fallidas: {failed}")
    print(f"📈 Porcentaje de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS GUI PASARON! La interfaz está funcionando correctamente.")
    else:
        print(f"\n⚠️ {failed} pruebas GUI fallaron. Revisar los errores arriba.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_gui_tests()
    sys.exit(0 if success else 1)
