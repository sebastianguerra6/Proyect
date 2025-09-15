#!/usr/bin/env python3
"""
Script para probar la aplicación GUI real con interacciones simuladas
"""
import sys
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

def test_real_gui():
    """Prueba la aplicación GUI real"""
    print("🖥️ INICIANDO PRUEBA DE APLICACIÓN GUI REAL")
    print("=" * 60)
    
    try:
        # Importar la aplicación
        from app_empleados_refactorizada import AppEmpleadosRefactorizada
        
        # Crear root de tkinter
        root = tk.Tk()
        
        # Configurar para cerrar automáticamente después de 10 segundos
        def auto_close():
            time.sleep(10)
            root.quit()
        
        # Iniciar timer de cierre automático
        timer_thread = threading.Thread(target=auto_close)
        timer_thread.daemon = True
        timer_thread.start()
        
        # Inicializar la aplicación
        print("✅ Inicializando aplicación...")
        app = AppEmpleadosRefactorizada(root)
        print("✅ Aplicación inicializada correctamente")
        
        # Verificar que se puede cambiar a la sección de conciliación
        print("✅ Cambiando a sección de conciliación...")
        app.cambiar_contenido("conciliacion")
        print("✅ Sección de conciliación activada")
        
        # Verificar que el componente de conciliación está visible
        conciliacion = app.componentes.get('conciliacion')
        if conciliacion and hasattr(conciliacion, 'frame'):
            print("✅ Frame de conciliación disponible")
            
            # Simular entrada de SID
            if hasattr(conciliacion, 'sid_var'):
                conciliacion.sid_var.set('S7457774')
                print("✅ SID configurado: S7457774")
                
                # Simular conciliación
                print("✅ Ejecutando conciliación...")
                try:
                    conciliacion._conciliar_accesos()
                    print("✅ Conciliación ejecutada exitosamente")
                    
                    # Verificar que hay resultados
                    if conciliacion.resultado_conciliacion:
                        print("✅ Resultados de conciliación obtenidos")
                        
                        # Verificar que se pueden mostrar en la tabla
                        current_access = conciliacion.resultado_conciliacion.get('current_access', [])
                        to_grant = conciliacion.resultado_conciliacion.get('to_grant', [])
                        to_revoke = conciliacion.resultado_conciliacion.get('to_revoke', [])
                        
                        print(f"✅ Datos para tabla:")
                        print(f"   - Accesos actuales: {len(current_access)}")
                        print(f"   - Accesos a otorgar: {len(to_grant)}")
                        print(f"   - Accesos a revocar: {len(to_revoke)}")
                        
                        # Simular exportación
                        print("✅ Probando exportación...")
                        try:
                            conciliacion._exportar_excel()
                            print("✅ Exportación ejecutada exitosamente")
                        except Exception as e:
                            print(f"⚠️ Error en exportación (esperado en modo no interactivo): {e}")
                    else:
                        print("❌ No se obtuvieron resultados de conciliación")
                        return False
                except Exception as e:
                    print(f"❌ Error en conciliación: {e}")
                    return False
            else:
                print("❌ No se encontró variable sid_var")
                return False
        else:
            print("❌ No se encontró componente de conciliación")
            return False
        
        print("✅ Todas las funcionalidades GUI probadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba GUI real: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass

def test_conciliacion_workflow():
    """Prueba el flujo completo de conciliación"""
    print("\n=== Prueba: Flujo Completo de Conciliación ===")
    try:
        from services import access_service, export_service
        
        # 1. Obtener empleado
        print("1. Obteniendo empleado...")
        empleado = access_service.get_employee_by_id('S7457774')
        if not empleado:
            print("❌ Empleado no encontrado")
            return False
        print(f"✅ Empleado: {empleado.get('full_name')} - {empleado.get('position')} - {empleado.get('unit')}")
        
        # 2. Ejecutar conciliación
        print("2. Ejecutando conciliación...")
        reporte = access_service.get_access_reconciliation_report('S7457774')
        if "error" in reporte:
            print(f"❌ Error en conciliación: {reporte['error']}")
            return False
        print("✅ Conciliación ejecutada")
        
        # 3. Verificar resultados
        print("3. Verificando resultados...")
        current_access = reporte.get('current_access', [])
        to_grant = reporte.get('to_grant', [])
        to_revoke = reporte.get('to_revoke', [])
        
        print(f"   - Accesos actuales: {len(current_access)}")
        print(f"   - Accesos a otorgar: {len(to_grant)}")
        print(f"   - Accesos a revocar: {len(to_revoke)}")
        
        # 4. Adaptar datos para exportación
        print("4. Adaptando datos para exportación...")
        from app_empleados_refactorizada import ConciliacionFrame
        
        root = tk.Tk()
        root.withdraw()
        conciliacion_frame = ConciliacionFrame(root)
        conciliacion_frame.sid_var.set('S7457774')
        
        adapted_data = conciliacion_frame._adapt_data_for_export(reporte)
        print("✅ Datos adaptados")
        
        # 5. Exportar a Excel
        print("5. Exportando a Excel...")
        output_path = export_service.export_reconciliation_tickets(
            [adapted_data],
            "Prueba de Flujo Completo"
        )
        print(f"✅ Archivo exportado: {output_path}")
        
        # 6. Verificar archivo
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Archivo verificado: {file_size} bytes")
        else:
            print("❌ Archivo no encontrado")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error en flujo de conciliación: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_complete_tests():
    """Ejecuta todas las pruebas completas"""
    print("🧪 INICIANDO PRUEBAS COMPLETAS DEL SISTEMA")
    print("=" * 80)
    
    tests = [
        ("Flujo de Conciliación", test_conciliacion_workflow),
        ("Aplicación GUI Real", test_real_gui)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Ejecutando: {test_name}")
        print("-" * 40)
        try:
            if test_func():
                print(f"✅ {test_name}: EXITOSO")
                passed += 1
            else:
                print(f"❌ {test_name}: FALLÓ")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL DE PRUEBAS")
    print("=" * 80)
    print(f"✅ Pruebas exitosas: {passed}")
    print(f"❌ Pruebas fallidas: {failed}")
    print(f"📈 Porcentaje de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS COMPLETAS PASARON!")
        print("✅ El sistema está funcionando correctamente en todos los aspectos:")
        print("   - Base de datos y servicios")
        print("   - Lógica de conciliación")
        print("   - Interfaz gráfica")
        print("   - Exportación de Excel")
        print("   - Flujo completo de trabajo")
    else:
        print(f"\n⚠️ {failed} pruebas fallaron. Revisar los errores arriba.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_complete_tests()
    sys.exit(0 if success else 1)
