#!/usr/bin/env python3
"""
Script completo para crear la base de datos del Sistema de Gestión de Empleados y Conciliación de Accesos
Este archivo contiene toda la lógica necesaria para crear la base de datos completa
"""

import sqlite3
import os
import random
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

class DatabaseManager:
    """Clase principal para gestionar la creación completa de la base de datos"""
    
    def __init__(self, db_path: str = "database/empleados.db"):
        self.db_path = db_path
        self.connection = None
        
    def create_database(self):
        """Crea la base de datos completa con todas las tablas"""
        
        # Asegurar que el directorio database existe
        os.makedirs('database', exist_ok=True)
        
        # Conectar a la base de datos (se crea si no existe)
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        try:
            print("🚀 Iniciando creación de base de datos completa...")
            
            # Configurar PRAGMAs para mejor rendimiento
            self._configure_pragmas()
            
            # Crear todas las tablas
            self._create_employee_tables(cursor)
            self._create_reconciliation_tables(cursor)
            self._create_additional_tables(cursor)
            
            # Crear índices para mejorar rendimiento
            self._create_indexes(cursor)
            
            # Crear triggers para actualización automática
            self._create_triggers(cursor)
            
            # Crear vistas para consultas optimizadas
            self._create_views(cursor)
            
            # Insertar datos de ejemplo
            self._insert_sample_data(cursor)
            
            # Confirmar cambios
            self.connection.commit()
            print("✅ Base de datos creada exitosamente!")
            print(f"📁 Archivo: {self.db_path}")
            
            # Mostrar información de las tablas creadas
            self._show_database_structure(cursor)
            
        except sqlite3.Error as e:
            print(f"❌ Error al crear la base de datos: {e}")
            self.connection.rollback()
        finally:
            if self.connection:
                self.connection.close()
    
    def _configure_pragmas(self):
        """Configura PRAGMAs para optimizar la base de datos"""
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = NORMAL")
        self.connection.execute("PRAGMA cache_size = 10000")
        self.connection.execute("PRAGMA temp_store = MEMORY")
    
    def _create_employee_tables(self, cursor):
        """Crea las tablas relacionadas con gestión de empleados"""
        print("📋 Creando tablas de gestión de empleados...")
        
        # Tabla headcount (plantilla de empleados)
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
        
        # Tabla procesos (historial de procesos de empleados)
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
        
        # Tabla onboarding_detalles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS onboarding_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceso_id INTEGER NOT NULL,
                tipo_onboarding TEXT NOT NULL,
                FOREIGN KEY (proceso_id) REFERENCES procesos(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla offboarding_detalles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offboarding_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceso_id INTEGER NOT NULL,
                tipo_offboarding TEXT NOT NULL,
                FOREIGN KEY (proceso_id) REFERENCES procesos(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla lateral_movement_detalles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lateral_movement_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proceso_id INTEGER NOT NULL,
                empleo_anterior TEXT,
                tipo_lateral TEXT NOT NULL,
                FOREIGN KEY (proceso_id) REFERENCES procesos(id) ON DELETE CASCADE
            )
        ''')
        
        print("   ✅ Tablas de empleados creadas")
    
    def _create_reconciliation_tables(self, cursor):
        """Crea las tablas relacionadas con conciliación de accesos"""
        print("📋 Creando tablas de conciliación de accesos...")
        
        # Tabla de personas para conciliación
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS person (
                sid TEXT PRIMARY KEY,
                area TEXT,
                subunit TEXT,
                cargo TEXT,
                email TEXT,
                updated_at TEXT
            )
        ''')
        
        # Tabla de matriz de autorizaciones por puesto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authorized_matrix (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subunit TEXT NOT NULL,
                cargo TEXT NOT NULL,
                app_name TEXT NOT NULL,
                role_name TEXT,
                UNIQUE(subunit, cargo, app_name, role_name) ON CONFLICT IGNORE
            )
        ''')
        
        # Tabla de historial de accesos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sid TEXT NOT NULL,
                app_name TEXT NOT NULL,
                role_name TEXT,
                tipo TEXT NOT NULL CHECK(tipo IN ('onboarding','offboarding')),
                record_date TEXT NOT NULL,
                ingresado_por TEXT,
                status TEXT,
                comment TEXT,
                FOREIGN KEY (sid) REFERENCES person(sid)
            )
        ''')
        
        print("   ✅ Tablas de conciliación creadas")
    
    def _create_additional_tables(self, cursor):
        """Crea tablas adicionales para funcionalidades extendidas"""
        print("📋 Creando tablas adicionales...")
        
        # Tabla de aplicaciones del sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT UNIQUE NOT NULL,
                description TEXT,
                category TEXT,
                owner TEXT,
                status TEXT DEFAULT 'Activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de roles y permisos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT NOT NULL,
                app_name TEXT NOT NULL,
                description TEXT,
                permissions TEXT,
                FOREIGN KEY (app_name) REFERENCES applications(app_name)
            )
        ''')
        
        # Tabla de auditoría de cambios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                old_values TEXT,
                new_values TEXT,
                user_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("   ✅ Tablas adicionales creadas")
    
    def _create_indexes(self, cursor):
        """Crea índices para mejorar el rendimiento"""
        print("📊 Creando índices de rendimiento...")
        
        # Índices para tablas de empleados
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_sid ON procesos(sid)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_numero_caso ON procesos(numero_caso)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_tipo ON procesos(tipo_proceso)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_status ON procesos(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procesos_app_name ON procesos(app_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_email ON headcount(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_departamento ON headcount(departamento)')
        
        # Índices para tablas de conciliación
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_history_sid ON access_history(sid)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_history_app ON access_history(app_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_history_date ON access_history(record_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_authorized_matrix_subunit_cargo ON authorized_matrix(subunit, cargo)')
        
        # Índices para tablas adicionales
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_name ON applications(app_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_roles_app ON roles(app_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_log_table ON audit_log(table_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp)')
        
        print("   ✅ Índices creados")
    
    def _create_triggers(self, cursor):
        """Crea triggers para actualización automática"""
        print("🔧 Creando triggers automáticos...")
        
        # Trigger para actualizar timestamp en procesos
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_procesos_timestamp 
                AFTER UPDATE ON procesos
                FOR EACH ROW
            BEGIN
                UPDATE procesos SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        # Trigger para actualizar timestamp en headcount
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_headcount_timestamp 
                AFTER UPDATE ON headcount
                FOR EACH ROW
            BEGIN
                UPDATE headcount SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        # Trigger para auditoría de cambios en procesos
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS audit_procesos_changes
                AFTER UPDATE ON procesos
                FOR EACH ROW
            BEGIN
                INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, user_id)
                VALUES ('procesos', NEW.id, 'UPDATE', 
                        json_object('status', OLD.status, 'app_quality', OLD.app_quality),
                        json_object('status', NEW.status, 'app_quality', NEW.app_quality),
                        NEW.ingreso_por);
            END
        ''')
        
        print("   ✅ Triggers creados")
    
    def _create_views(self, cursor):
        """Crea vistas para consultas optimizadas"""
        print("👁️ Creando vistas optimizadas...")
        
        # Vista de accesos actuales para conciliación
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS vw_current_assignments AS
            WITH latest_access AS (
                SELECT 
                    sid, 
                    app_name, 
                    role_name,
                    tipo,
                    record_date,
                    ROW_NUMBER() OVER (
                        PARTITION BY sid, app_name 
                        ORDER BY record_date DESC
                    ) as rn
                FROM access_history
            )
            SELECT 
                sid,
                app_name,
                role_name,
                CASE 
                    WHEN tipo = 'onboarding' THEN 1 
                    WHEN tipo = 'offboarding' THEN 0 
                    ELSE 0 
                END as has_access,
                record_date
            FROM latest_access 
            WHERE rn = 1
        ''')
        
        # Vista de accesos objetivo según puesto
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS vw_should_assignments AS
            SELECT 
                p.sid,
                am.app_name,
                am.role_name,
                p.subunit,
                p.cargo
            FROM person p
            JOIN authorized_matrix am ON p.subunit = am.subunit AND p.cargo = am.cargo
        ''')
        
        # Vista consolidada de empleados y procesos
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS vw_employee_summary AS
            SELECT 
                h.sid,
                h.nombre,
                h.apellido,
                h.email,
                h.departamento,
                h.cargo,
                h.estado,
                COUNT(p.id) as total_procesos,
                SUM(CASE WHEN p.status = 'Completado' THEN 1 ELSE 0 END) as procesos_completados,
                SUM(CASE WHEN p.status = 'Pendiente' THEN 1 ELSE 0 END) as procesos_pendientes
            FROM headcount h
            LEFT JOIN procesos p ON h.sid = p.sid
            GROUP BY h.sid, h.nombre, h.apellido, h.email, h.departamento, h.cargo, h.estado
        ''')
        
        print("   ✅ Vistas creadas")
    
    def _insert_sample_data(self, cursor):
        """Inserta datos de ejemplo en la base de datos"""
        print("📝 Insertando datos de ejemplo...")
        
        try:
            # Verificar si ya hay datos
            cursor.execute("SELECT COUNT(*) FROM headcount")
            if cursor.fetchone()[0] > 0:
                print("   ℹ️  La base de datos ya contiene datos, omitiendo inserción de ejemplos")
                return
            
            # Insertar aplicaciones de ejemplo
            self._insert_sample_applications(cursor)
            
            # Insertar empleados de ejemplo
            self._insert_sample_employees(cursor)
            
            # Insertar procesos de ejemplo
            self._insert_sample_processes(cursor)
            
            # Insertar datos de conciliación
            self._insert_sample_reconciliation_data(cursor)
            
            print("   ✅ Datos de ejemplo insertados correctamente")
            
        except sqlite3.Error as e:
            print(f"   ⚠️  Error al insertar datos de ejemplo: {e}")
    
    def _insert_sample_applications(self, cursor):
        """Inserta aplicaciones de ejemplo"""
        applications = [
            ('Sistema de Gestión de Empleados', 'Sistema principal de RRHH', 'RRHH', 'Admin'),
            ('Portal de Recursos Humanos', 'Portal web para empleados', 'RRHH', 'Admin'),
            ('Aplicación de Nómina', 'Sistema de nómina y pagos', 'Finanzas', 'Finanzas'),
            ('Sistema de Control de Asistencia', 'Control de entrada/salida', 'RRHH', 'Admin'),
            ('Portal de Beneficios', 'Gestión de beneficios corporativos', 'RRHH', 'Admin'),
            ('Aplicación de Capacitación', 'Sistema de entrenamiento', 'RRHH', 'Admin'),
            ('Sistema de Evaluación', 'Evaluación de desempeño', 'RRHH', 'Admin'),
            ('Portal de Comunicaciones', 'Comunicaciones internas', 'Comunicaciones', 'Comunicaciones'),
            ('Aplicación de Proyectos', 'Gestión de proyectos', 'Tecnología', 'Tecnología'),
            ('Sistema de Reportes', 'Reportes gerenciales', 'Tecnología', 'Tecnología'),
            ('Portal de Autogestión', 'Autogestión de empleados', 'RRHH', 'Admin'),
            ('Sistema de Permisos', 'Gestión de permisos y vacaciones', 'RRHH', 'Admin'),
            ('Sistema de Seguridad', 'Control de accesos y seguridad', 'Tecnología', 'Tecnología'),
            ('Portal de Documentación', 'Documentación corporativa', 'Tecnología', 'Tecnología'),
            ('Aplicación de Inventarios', 'Gestión de inventarios', 'Operaciones', 'Operaciones')
        ]
        
        for app in applications:
            cursor.execute('''
                INSERT OR IGNORE INTO applications (app_name, description, category, owner)
                VALUES (?, ?, ?, ?)
            ''', app)
    
    def _insert_sample_employees(self, cursor):
        """Inserta empleados de ejemplo"""
        employees = [
            ('EMP001', 'Juan', 'Pérez', 'juan.perez@empresa.com', '+57 300 123 4567', 'Tecnología', 'Desarrollador Senior', '2024-01-15', 5000000.00, 'Activo'),
            ('EMP002', 'María', 'García', 'maria.garcia@empresa.com', '+57 300 234 5678', 'Recursos Humanos', 'Analista Senior', '2024-02-01', 4500000.00, 'Activo'),
            ('EMP003', 'Carlos', 'López', 'carlos.lopez@empresa.com', '+57 300 345 6789', 'Finanzas', 'Contador', '2024-01-20', 3800000.00, 'Activo'),
            ('EMP004', 'Ana', 'Rodríguez', 'ana.rodriguez@empresa.com', '+57 300 456 7890', 'Marketing', 'Especialista Digital', '2024-02-15', 4200000.00, 'Activo'),
            ('EMP005', 'Luis', 'Martínez', 'luis.martinez@empresa.com', '+57 300 567 8901', 'Operaciones', 'Coordinador', '2024-01-10', 3500000.00, 'Activo'),
            ('EMP006', 'Sofia', 'Hernández', 'sofia.hernandez@empresa.com', '+57 300 678 9012', 'Tecnología', 'DevOps Engineer', '2024-03-01', 4800000.00, 'Activo'),
            ('EMP007', 'Roberto', 'Díaz', 'roberto.diaz@empresa.com', '+57 300 789 0123', 'Finanzas', 'Analista Financiero', '2024-02-20', 4000000.00, 'Activo'),
            ('EMP008', 'Carmen', 'Moreno', 'carmen.moreno@empresa.com', '+57 300 890 1234', 'RRHH', 'Reclutadora', '2024-01-25', 3500000.00, 'Activo')
        ]
        
        for emp in employees:
            cursor.execute('''
                INSERT INTO headcount (numero_caso, sid, nombre, apellido, email, telefono, departamento, cargo, fecha_contratacion, salario, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (f"HC-{emp[0]}-{datetime.now().strftime('%Y%m%d')}", *emp))
    
    def _insert_sample_processes(self, cursor):
        """Inserta procesos de ejemplo"""
        # Obtener aplicaciones disponibles
        cursor.execute("SELECT app_name FROM applications")
        apps = [row[0] for row in cursor.fetchall()]
        
        processes = [
            ('EMP001', 'Sub Unidad 1 - Desarrollo Frontend', 'Desarrollador Frontend', 'onboarding'),
            ('EMP002', 'Sub Unidad 6 - Gestión de Proyectos', 'Analista Senior', 'onboarding'),
            ('EMP003', 'Sub Unidad 4 - QA y Testing', 'Analista de Calidad', 'lateral_movement'),
            ('EMP004', 'Sub Unidad 5 - Diseño UX/UI', 'Diseñador UX', 'offboarding'),
            ('EMP005', 'Sub Unidad 3 - DevOps e Infraestructura', 'DevOps Engineer', 'onboarding'),
            ('EMP006', 'Sub Unidad 2 - Desarrollo Backend', 'Desarrollador Backend', 'onboarding'),
            ('EMP007', 'Sub Unidad 7 - Análisis Financiero', 'Analista Financiero', 'onboarding'),
            ('EMP008', 'Sub Unidad 8 - Reclutamiento', 'Reclutadora Senior', 'onboarding')
        ]
        
        for i, process in enumerate(processes):
            # Generar número de caso único
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            short_uuid = str(uuid.uuid4())[:8]
            numero_caso = f"CASE-{timestamp}-{short_uuid}"
            
            # Asignar aplicación aleatoria
            app_name = random.choice(apps)
            
            # Insertar proceso principal
            cursor.execute('''
                INSERT INTO procesos (numero_caso, tipo_proceso, sid, nueva_sub_unidad, nuevo_cargo, 
                                   request_date, ingreso_por, fecha, status, app_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (numero_caso, process[3], process[0], process[1], process[2], 
                  datetime.now().strftime('%Y-%m-%d'), 'Admin', datetime.now().strftime('%Y-%m-%d'), 
                  random.choice(['Pendiente', 'En Proceso', 'Completado']), app_name))
            
            proceso_id = cursor.lastrowid
            
            # Insertar detalles según el tipo de proceso
            if process[3] == 'onboarding':
                tipos_onboarding = ['Nuevo Empleado', 'Recontratación', 'Transferencia Interna', 'Promoción']
                cursor.execute('''
                    INSERT INTO onboarding_detalles (proceso_id, tipo_onboarding)
                    VALUES (?, ?)
                ''', (proceso_id, random.choice(tipos_onboarding)))
                
            elif process[3] == 'offboarding':
                tipos_offboarding = ['Salida Definitiva', 'Reducción de Personal', 'Fin de Proyecto', 'Cambio de Empresa']
                cursor.execute('''
                    INSERT INTO offboarding_detalles (proceso_id, tipo_offboarding)
                    VALUES (?, ?, ?)
                ''', (proceso_id, random.choice(tipos_offboarding)))
                
            elif process[3] == 'lateral_movement':
                tipos_lateral = ['Movimiento Horizontal', 'Reasignación de Proyecto', 'Cambio de Equipo', 'Rotación de Funciones']
                cursor.execute('''
                    INSERT INTO lateral_movement_detalles (proceso_id, empleo_anterior, tipo_lateral)
                    VALUES (?, ?, ?)
                ''', (proceso_id, 'Contador', random.choice(tipos_lateral)))
    
    def _insert_sample_reconciliation_data(self, cursor):
        """Inserta datos de ejemplo para conciliación"""
        # Insertar personas en tabla person
        persons = [
            ('EMP001', 'Tecnología', 'Desarrollo', 'Desarrollador Senior', 'juan.perez@empresa.com'),
            ('EMP002', 'Recursos Humanos', 'Gestión', 'Analista Senior', 'maria.garcia@empresa.com'),
            ('EMP003', 'Finanzas', 'Contabilidad', 'Contador', 'carlos.lopez@empresa.com'),
            ('EMP004', 'Marketing', 'Digital', 'Especialista Digital', 'ana.rodriguez@empresa.com'),
            ('EMP005', 'Operaciones', 'Coordinación', 'Coordinador', 'luis.martinez@empresa.com')
        ]
        
        for person in persons:
            cursor.execute('''
                INSERT OR REPLACE INTO person (sid, area, subunit, cargo, email, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (*person, datetime.now().isoformat()))
        
        # Insertar matriz de autorizaciones
        authorizations = [
            ('Desarrollo', 'Desarrollador Senior', 'Sistema de Gestión de Empleados', 'Admin'),
            ('Desarrollo', 'Desarrollador Senior', 'Portal de Recursos Humanos', 'Developer'),
            ('Desarrollo', 'Desarrollador Senior', 'Aplicación de Proyectos', 'Developer'),
            ('Desarrollo', 'Desarrollador Senior', 'Sistema de Seguridad', 'Developer'),
            ('Gestión', 'Analista Senior', 'Sistema de Gestión de Empleados', 'User'),
            ('Gestión', 'Analista Senior', 'Portal de Recursos Humanos', 'Editor'),
            ('Gestión', 'Analista Senior', 'Aplicación de Capacitación', 'Admin'),
            ('Contabilidad', 'Contador', 'Aplicación de Nómina', 'User'),
            ('Contabilidad', 'Contador', 'Sistema de Reportes', 'Viewer'),
            ('Digital', 'Especialista Digital', 'Portal de Comunicaciones', 'Editor'),
            ('Digital', 'Especialista Digital', 'Portal de Beneficios', 'User'),
            ('Coordinación', 'Coordinador', 'Sistema de Control de Asistencia', 'User'),
            ('Coordinación', 'Coordinador', 'Aplicación de Inventarios', 'User')
        ]
        
        for auth in authorizations:
            cursor.execute('''
                INSERT OR IGNORE INTO authorized_matrix (subunit, cargo, app_name, role_name)
                VALUES (?, ?, ?, ?)
            ''', auth)
        
        # Insertar historial de accesos
        access_history = [
            ('EMP001', 'Sistema de Gestión de Empleados', 'Admin', 'onboarding', '2024-01-15T09:00:00', 'Admin', 'Completado', 'Acceso inicial'),
            ('EMP001', 'Portal de Recursos Humanos', 'Developer', 'onboarding', '2024-01-15T09:00:00', 'Admin', 'Completado', 'Acceso inicial'),
            ('EMP002', 'Sistema de Gestión de Empleados', 'User', 'onboarding', '2024-02-01T10:00:00', 'Admin', 'Completado', 'Acceso inicial'),
            ('EMP002', 'Portal de Recursos Humanos', 'Editor', 'onboarding', '2024-02-01T10:00:00', 'Admin', 'Completado', 'Acceso inicial'),
            ('EMP003', 'Aplicación de Nómina', 'User', 'onboarding', '2024-01-20T08:00:00', 'Admin', 'Completado', 'Acceso inicial'),
            ('EMP004', 'Portal de Comunicaciones', 'Editor', 'onboarding', '2024-02-15T11:00:00', 'Admin', 'Completado', 'Acceso inicial'),
            ('EMP005', 'Sistema de Control de Asistencia', 'User', 'onboarding', '2024-01-10T07:00:00', 'Admin', 'Completado', 'Acceso inicial')
        ]
        
        for access in access_history:
            cursor.execute('''
                INSERT OR IGNORE INTO access_history (sid, app_name, role_name, tipo, record_date, ingresado_por, status, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', access)
    
    def _show_database_structure(self, cursor):
        """Muestra la estructura de la base de datos creada"""
        print("\n📊 Estructura de la base de datos:")
        print("=" * 60)
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 Total de tablas: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"\n🔹 Tabla: {table_name}")
            
            # Obtener estructura de la tabla
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for column in columns:
                name = column[1]
                type_name = column[2]
                not_null = "NOT NULL" if column[3] else ""
                default = f"DEFAULT {column[4]}" if column[4] else ""
                
                print(f"   • {name}: {type_name} {not_null} {default}".strip())
            
            # Mostrar conteo de registros
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📊 Registros: {count}")
            except:
                print(f"   📊 Registros: Error al contar")
        
        # Mostrar vistas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = cursor.fetchall()
        if views:
            print(f"\n👁️  Vistas creadas: {[v[0] for v in views]}")
        
        # Mostrar triggers
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
        triggers = cursor.fetchall()
        if triggers:
            print(f"🔧 Triggers creados: {[t[0] for t in triggers]}")
    
    def verify_connection(self):
        """Verifica que la base de datos se pueda conectar correctamente"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar que las tablas existen
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"\n🔍 Verificación de conexión:")
            print(f"   ✅ Conexión exitosa a: {self.db_path}")
            print(f"   📋 Tablas encontradas: {len(tables)}")
            
            # Mostrar resumen de datos
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"      • {table[0]}: {count} registros")
                except:
                    print(f"      • {table[0]}: Error al contar")
            
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error de conexión: {e}")
            return False

def main():
    """Función principal para ejecutar la creación de la base de datos"""
    print("🚀 Sistema de Creación de Base de Datos Completa")
    print("=" * 70)
    print("Este script creará una base de datos completa con:")
    print("• Tablas de gestión de empleados")
    print("• Tablas de conciliación de accesos")
    print("• Tablas adicionales para funcionalidades extendidas")
    print("• Índices, triggers y vistas optimizadas")
    print("• Datos de ejemplo para pruebas")
    print("=" * 70)
    
    # Crear instancia del gestor de base de datos
    db_manager = DatabaseManager()
    
    # Crear la base de datos
    db_manager.create_database()
    
    # Verificar la conexión
    print("\n" + "=" * 70)
    db_manager.verify_connection()
    
    print("\n✨ Base de datos completa lista para usar!")
    print("💡 Puedes ejecutar este script nuevamente para verificar el estado")
    print("📁 Ubicación: database/empleados.db")

if __name__ == "__main__":
    main()
