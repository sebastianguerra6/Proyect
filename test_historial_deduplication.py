#!/usr/bin/env python3
"""
Script para verificar que no se crean duplicados en el historial
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

from services.access_management_service import access_service

def test_historial_deduplication():
    """Prueba que no se crean duplicados en el historial"""
    print("🔍 Verificando deduplicación en el historial...")
    
    try:
        # Obtener un empleado de prueba
        employees = access_service.get_all_employees()
        if not employees:
            print("❌ No hay empleados para probar")
            return False
        
        test_employee = employees[0]
        scotia_id = test_employee['scotia_id']
        print(f"   Empleado de prueba: {scotia_id} - {test_employee['full_name']}")
        
        # Limpiar historial previo para este empleado
        print("\n1. Limpiando historial previo...")
        conn = access_service.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM historico WHERE scotia_id = ?", (scotia_id,))
        conn.commit()
        conn.close()
        
        # Verificar historial vacío
        historial_antes = access_service.get_employee_history(scotia_id)
        print(f"   Historial antes: {len(historial_antes)} registros")
        
        # Ejecutar asignación automática
        print("\n2. Ejecutando asignación automática...")
        success, message, counts = access_service.assign_accesses(scotia_id, "Sistema de Prueba")
        
        if not success:
            print(f"❌ Error en asignación: {message}")
            return False
        
        print(f"✅ {message}")
        print(f"   Otorgados: {counts['granted']}")
        print(f"   Revocados: {counts['revoked']}")
        
        # Verificar historial después
        print("\n3. Verificando historial después...")
        historial_despues = access_service.get_employee_history(scotia_id)
        print(f"   Historial después: {len(historial_despues)} registros")
        
        # Verificar duplicados por app_access_name
        print("\n4. Verificando duplicados...")
        app_names = [h.get('app_access_name') for h in historial_despues if h.get('app_access_name')]
        unique_app_names = set(app_names)
        
        print(f"   Total registros: {len(historial_despues)}")
        print(f"   Apps únicas: {len(unique_app_names)}")
        print(f"   Apps con duplicados: {len(app_names) - len(unique_app_names)}")
        
        if len(app_names) == len(unique_app_names):
            print("✅ No hay duplicados en el historial")
        else:
            print("❌ Hay duplicados en el historial")
            # Mostrar duplicados
            from collections import Counter
            app_counts = Counter(app_names)
            duplicates = {app: count for app, count in app_counts.items() if count > 1}
            for app, count in duplicates.items():
                print(f"   - {app}: {count} veces")
        
        # Verificar duplicados por (scotia_id, app_access_name, process_access, status)
        print("\n5. Verificando duplicados por clave completa...")
        conn = access_service.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT scotia_id, app_access_name, process_access, status, COUNT(*) as count
            FROM historico 
            WHERE scotia_id = ?
            GROUP BY scotia_id, app_access_name, process_access, status
            HAVING COUNT(*) > 1
        ''', (scotia_id,))
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"❌ Encontrados {len(duplicates)} duplicados por clave completa:")
            for dup in duplicates:
                print(f"   {dup[0]} - {dup[1]} ({dup[2]}, {dup[3]}): {dup[4]} veces")
        else:
            print("✅ No hay duplicados por clave completa")
        
        conn.close()
        
        # Mostrar resumen del historial
        print("\n6. Resumen del historial:")
        for h in historial_despues:
            print(f"   - {h.get('app_access_name')} ({h.get('process_access')}) - {h.get('status')}")
        
        print("\n✅ Verificación de deduplicación del historial completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_historial_deduplication()

