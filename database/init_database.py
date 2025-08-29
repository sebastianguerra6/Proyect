#!/usr/bin/env python3
"""
Script para inicializar la base de datos del Sistema de Gestión de Empleados
"""

import sqlite3
import os
import random
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
                sid TEXT NOT NULL,
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
                app_name TEXT NOT NULL,
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
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_app_name ON procesos(app_name)')
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
    
    # Lista de nombres de aplicaciones para asignar aleatoriamente
    nombres_apps = [
        "Sistema de Gestión de Empleados",
        "Portal de Recursos Humanos",
        "Aplicación de Nómina",
        "Sistema de Control de Asistencia",
        "Portal de Beneficios",
        "Aplicación de Capacitación",
        "Sistema de Evaluación de Desempeño",
        "Portal de Comunicaciones Internas",
        "Aplicación de Gestión de Proyectos",
        "Sistema de Reportes Gerenciales",
        "Portal de Autogestión",
        "Aplicación de Gestión de Permisos",
        "Sistema de Seguridad y Accesos",
        "Portal de Documentación",
        "Aplicación de Gestión de Inventarios"
    ]
    
    try:
        # Insertar ejemplos en headcount
        empleados_ejemplo = [
            ('HC-2024-001', 'EMP001', 'Juan', 'Pérez', 'juan.perez@empresa.com', '+57 300 123 4567', 'Tecnología', 'Desarrollador Senior', '2024-01-15', 5000000.00, 'Activo'),
            ('HC-2024-002', 'EMP002', 'María', 'García', 'maria.garcia@empresa.com', '+57 300 234 5678', 'Recursos Humanos', 'Analista Senior', '2024-02-01', 4500000.00, 'Activo'),
            ('HC-2024-003', 'EMP003', 'Carlos', 'López', 'carlos.lopez@empresa.com', '+57 300 345 6789', 'Finanzas', 'Contador', '2024-01-20', 3800000.00, 'Activo'),
            ('HC-2024-004', 'EMP004', 'Ana', 'Rodríguez', 'ana.rodriguez@empresa.com', '+57 300 456 7890', 'Marketing', 'Especialista Digital', '2024-02-15', 4200000.00, 'Activo'),
            ('HC-2024-005', 'EMP005', 'Luis', 'Martínez', 'luis.martinez@empresa.com', '+57 300 567 8901', 'Operaciones', 'Coordinador', '2024-01-10', 3500000.00, 'Activo')
        ]
        
        for empleado in empleados_ejemplo:
            cursor.execute('''
                INSERT INTO headcount (numero_caso, sid, nombre, apellido, email, telefono, departamento, cargo, fecha_contratacion, salario, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', empleado)
        
        # Insertar ejemplos en procesos
        procesos_ejemplo = [
            ('CASE-20240115120000-12345678', 'onboarding', 'EMP001', 'Sub Unidad 1 - Desarrollo Frontend', 'Desarrollador Frontend', '2024-01-15', 'María García', '2024-01-15', 'En Proceso'),
            ('CASE-20240201130000-23456789', 'onboarding', 'EMP002', 'Sub Unidad 6 - Gestión de Proyectos', 'Analista Senior', '2024-02-01', 'Juan Pérez', '2024-02-01', 'Completado'),
            ('CASE-20240120140000-34567890', 'lateral_movement', 'EMP003', 'Sub Unidad 4 - QA y Testing', 'Analista de Calidad', '2024-01-20', 'Ana Rodríguez', '2024-01-20', 'Pendiente'),
            ('CASE-20240215150000-45678901', 'offboarding', 'EMP004', 'Sub Unidad 5 - Diseño UX/UI', 'Diseñador UX', '2024-02-15', 'Luis Martínez', '2024-02-15', 'En Proceso'),
            ('CASE-20240110160000-56789012', 'onboarding', 'EMP005', 'Sub Unidad 3 - DevOps e Infraestructura', 'DevOps Engineer', '2024-01-10', 'Carlos López', '2024-01-10', 'Completado')
        ]
        
        for proceso in procesos_ejemplo:
            # Asignar nombre de aplicación aleatorio
            app_name = random.choice(nombres_apps)
            
            cursor.execute('''
                INSERT INTO procesos (numero_caso, tipo_proceso, sid, nueva_sub_unidad, nuevo_cargo, request_date, ingreso_por, fecha, status, app_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', proceso + (app_name,))
            
            proceso_id = cursor.lastrowid
            
            # Insertar detalles según el tipo de proceso
            if proceso[1] == 'onboarding':
                tipos_onboarding = ['Nuevo Empleado', 'Recontratación', 'Transferencia Interna', 'Promoción']
                cursor.execute('''
                    INSERT INTO onboarding_detalles (proceso_id, tipo_onboarding)
                    VALUES (?, ?)
                ''', (proceso_id, random.choice(tipos_onboarding)))
                
            elif proceso[1] == 'offboarding':
                tipos_offboarding = ['Salida Definitiva', 'Reducción de Personal', 'Fin de Proyecto', 'Cambio de Empresa']
                cursor.execute('''
                    INSERT INTO offboarding_detalles (proceso_id, tipo_offboarding)
                    VALUES (?, ?)
                ''', (proceso_id, random.choice(tipos_offboarding)))
                
            elif proceso[1] == 'lateral_movement':
                tipos_lateral = ['Movimiento Horizontal', 'Reasignación de Proyecto', 'Cambio de Equipo', 'Rotación de Funciones']
                cursor.execute('''
                    INSERT INTO lateral_movement_detalles (proceso_id, empleo_anterior, tipo_lateral)
                    VALUES (?, ?, ?)
                ''', (proceso_id, 'Contador', random.choice(tipos_lateral)))
        
        print("✅ Datos de ejemplo insertados correctamente")
        print(f"   📊 {len(empleados_ejemplo)} empleados en headcount")
        print(f"   📊 {len(procesos_ejemplo)} procesos creados")
        print(f"   📱 Nombres de aplicaciones asignados aleatoriamente")
        
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
        
        # Mostrar algunos datos de ejemplo si es la tabla procesos
        if nombre_tabla == 'procesos':
            cursor.execute("SELECT numero_caso, sid, app_name, status FROM procesos LIMIT 3")
            ejemplos = cursor.fetchall()
            if ejemplos:
                print(f"   📱 Ejemplos de APP names:")
                for ejemplo in ejemplos:
                    print(f"      • {ejemplo[0]} - {ejemplo[1]} - {ejemplo[2]} - {ejemplo[3]}")

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
