import sqlite3
import os

def actualizar_base_datos():
    """Actualiza la base de datos existente para agregar la columna SID"""
    db_path = "database/empleados.db"
    
    if not os.path.exists(db_path):
        print("❌ La base de datos no existe. Ejecute primero init_database.py")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Actualizando base de datos...")
        
        # Verificar si la columna sid ya existe
        cursor.execute("PRAGMA table_info(headcount)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        if 'sid' not in columnas:
            print("📝 Agregando columna SID a la tabla headcount...")
            
            # Agregar columna sid
            cursor.execute("ALTER TABLE headcount ADD COLUMN sid TEXT")
            
            # Actualizar registros existentes con un SID por defecto
            cursor.execute("UPDATE headcount SET sid = 'SID_' || id WHERE sid IS NULL")
            
            print("✅ Columna SID agregada exitosamente")
        else:
            print("ℹ️ La columna SID ya existe")
        
        # Verificar si la columna sid existe en la tabla procesos
        cursor.execute("PRAGMA table_info(procesos)")
        columnas_procesos = [col[1] for col in cursor.fetchall()]
        
        if 'sid' not in columnas_procesos:
            print("📝 Agregando columna SID a la tabla procesos...")
            
            # Agregar columna sid
            cursor.execute("ALTER TABLE procesos ADD COLUMN sid TEXT")
            
            # Actualizar registros existentes con un SID por defecto
            cursor.execute("UPDATE procesos SET sid = 'SID_' || id WHERE sid IS NULL")
            
            print("✅ Columna SID agregada a procesos exitosamente")
        else:
            print("ℹ️ La columna SID ya existe en procesos")
        
        # Verificar si existen las columnas adicionales en procesos
        columnas_adicionales = [
            'mail', 'closing_date_app', 'app_quality', 'confirmation_by_user', 'comment'
        ]
        
        for columna in columnas_adicionales:
            if columna not in columnas_procesos:
                print(f"📝 Agregando columna {columna} a la tabla procesos...")
                
                if columna in ['closing_date_app']:
                    cursor.execute(f"ALTER TABLE procesos ADD COLUMN {columna} DATE")
                else:
                    cursor.execute(f"ALTER TABLE procesos ADD COLUMN {columna} TEXT")
                
                print(f"✅ Columna {columna} agregada exitosamente")
            else:
                print(f"ℹ️ La columna {columna} ya existe en procesos")
        
        conn.commit()
        print("🎉 Base de datos actualizada exitosamente")
        
        # Mostrar estructura actualizada
        print("\n📊 Estructura actualizada de las tablas:")
        
        print("\nTabla headcount:")
        cursor.execute("PRAGMA table_info(headcount)")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
        print("\nTabla procesos:")
        cursor.execute("PRAGMA table_info(procesos)")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error actualizando la base de datos: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando actualización de base de datos...")
    if actualizar_base_datos():
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Proceso falló")
