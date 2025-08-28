#!/usr/bin/env python3
"""
Script para inicializar la base de datos del Sistema de Gestión de Empleados
"""

import sqlite3
import os
from datetime import datetime

def crear_base_datos():
    """Crea la base de datos y todas las tablas necesarias"""
    
    # Asegurar que el directorio database existe
    os.makedirs('database', exist_ok=True)
    
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect('database/empleados.db')
    cursor = conn.cursor()
    
    try:
        # Crear tabla headcount
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS headcount (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_caso TEXT UNIQUE,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT,
                departamento TEXT NOT NULL,
                cargo TEXT NOT NULL,
                fecha_contratacion DATE NOT NULL,
                salario DECIMAL(10,2),
                estado TEXT DEFAULT 'Activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla procesos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procesos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_caso TEXT UNIQUE NOT NULL,
                tipo_proceso TEXT NOT NULL CHECK (tipo_proceso IN ('onboarding', 'offboarding', 'lateral_movement')),
                sid TEXT NOT NULL,
                nueva_sub_unidad TEXT NOT NULL,
                nuevo_cargo TEXT NOT NULL,
                request_date DATE NOT NULL,
                ingreso_por TEXT NOT NULL,
                fecha DATE NOT NULL,
                status TEXT DEFAULT 'Pendiente',
                mail TEXT,
                closing_date_app DATE,
                app_quality TEXT CHECK (app_quality IN ('Excelente', 'Buena', 'Regular', 'Mala', 'Pendiente')),
                confirmation_by_user TEXT CHECK (confirmation_by_user IN ('Sí', 'No', 'Pendiente')),
                comment TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla onboarding_detalles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS onboarding_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceso_id INTEGER NOT NULL,
                tipo_onboarding TEXT NOT NULL,
                FOREIGN KEY (proceso_id) REFERENCES procesos(id) ON DELETE CASCADE
            )
        ''')
        
        # Crear tabla offboarding_detalles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offboarding_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceso_id INTEGER NOT NULL,
                tipo_offboarding TEXT NOT NULL,
                FOREIGN KEY (proceso_id) REFERENCES procesos(id) ON DELETE CASCADE
            )
        ''')
        
        # Crear tabla lateral_movement_detalles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lateral_movement_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceso_id INTEGER NOT NULL,
                empleo_anterior TEXT,
                tipo_lateral TEXT NOT NULL,
                FOREIGN KEY (proceso_id) REFERENCES procesos(id) ON DELETE CASCADE
            )
        ''')
        
        # Crear índices para mejorar el rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_sid ON procesos(sid)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_numero_caso ON procesos(numero_caso)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_tipo ON procesos(tipo_proceso)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_status ON procesos(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_email ON headcount(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_departamento ON headcount(departamento)')
        
        # Crear triggers para actualizar automáticamente las fechas
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_procesos_timestamp 
                AFTER UPDATE ON procesos
                FOR EACH ROW
            BEGIN
                UPDATE procesos SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_headcount_timestamp 
                AFTER UPDATE ON headcount
                FOR EACH ROW
            BEGIN
                UPDATE headcount SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        # Insertar algunos datos de ejemplo
        insertar_datos_ejemplo(cursor)
        
        # Confirmar cambios
        conn.commit()
        print("✅ Base de datos creada exitosamente!")
        print("📁 Archivo: database/empleados.db")
        
        # Mostrar información de las tablas creadas
        mostrar_estructura_tablas(cursor)
        
    except sqlite3.Error as e:
        print(f"❌ Error al crear la base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

def insertar_datos_ejemplo(cursor):
    """Inserta algunos datos de ejemplo en la base de datos"""
    
    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM headcount")
    if cursor.fetchone()[0] > 0:
        print("ℹ️  La base de datos ya contiene datos, omitiendo inserción de ejemplos")
        return
    
    try:
        # Insertar ejemplo en headcount
        cursor.execute('''
            INSERT INTO headcount (numero_caso, nombre, apellido, email, telefono, departamento, cargo, fecha_contratacion, salario, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'HC-2024-001',
            'Juan',
            'Pérez',
            'juan.perez@empresa.com',
            '+57 300 123 4567',
            'Tecnología',
            'Desarrollador Senior',
            '2024-01-15',
            5000000.00,
            'Activo'
        ))
        
        # Insertar ejemplo en procesos (onboarding)
        cursor.execute('''
            INSERT INTO procesos (numero_caso, tipo_proceso, sid, nueva_sub_unidad, nuevo_cargo, request_date, ingreso_por, fecha, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'CASE-20240115120000-12345678',
            'onboarding',
            'EMP001',
            'Sub Unidad 1 - Desarrollo Frontend',
            'Desarrollador Frontend',
            '2024-01-15',
            'María García',
            '2024-01-15',
            'En Proceso'
        ))
        
        # Obtener el ID del proceso insertado
        proceso_id = cursor.lastrowid
        
        # Insertar detalle de onboarding
        cursor.execute('''
            INSERT INTO onboarding_detalles (proceso_id, tipo_onboarding)
            VALUES (?, ?)
        ''', (proceso_id, 'Nuevo Empleado'))
        
        print("✅ Datos de ejemplo insertados correctamente")
        
    except sqlite3.Error as e:
        print(f"⚠️  Error al insertar datos de ejemplo: {e}")

def mostrar_estructura_tablas(cursor):
    """Muestra la estructura de las tablas creadas"""
    
    print("\n📊 Estructura de la base de datos:")
    print("=" * 50)
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    
    for tabla in tablas:
        nombre_tabla = tabla[0]
        print(f"\n🔹 Tabla: {nombre_tabla}")
        
        # Obtener estructura de la tabla
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        columnas = cursor.fetchall()
        
        for columna in columnas:
            nombre = columna[1]
            tipo = columna[2]
            not_null = "NOT NULL" if columna[3] else ""
            default = f"DEFAULT {columna[4]}" if columna[4] else ""
            
            print(f"   • {nombre}: {tipo} {not_null} {default}".strip())

def verificar_conexion():
    """Verifica que la base de datos se pueda conectar correctamente"""
    
    try:
        conn = sqlite3.connect('database/empleados.db')
        cursor = conn.cursor()
        
        # Verificar que las tablas existen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        
        print(f"\n🔍 Verificación de conexión:")
        print(f"   ✅ Conexión exitosa a: database/empleados.db")
        print(f"   📋 Tablas encontradas: {len(tablas)}")
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla[0]}")
            count = cursor.fetchone()[0]
            print(f"      • {tabla[0]}: {count} registros")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Inicializando base de datos del Sistema de Gestión de Empleados")
    print("=" * 70)
    
    # Crear la base de datos
    crear_base_datos()
    
    # Verificar la conexión
    print("\n" + "=" * 70)
    verificar_conexion()
    
    print("\n✨ Base de datos lista para usar!")
    print("💡 Puedes ejecutar este script nuevamente para verificar el estado")
