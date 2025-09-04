"""
Gestor de base de datos para el sistema de gestión de empleados y accesos
Incluye las tablas: headcount, applications, historico
"""
import os
import sqlite3
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import shutil

# Configuración centralizada
DB_PATH = os.path.join(os.path.dirname(__file__), "empleados.db")
DB_CONFIG = {
    'path': DB_PATH,
    'timeout': 30,
    'check_same_thread': False
}

def get_db_path():
    """Retorna la ruta de la base de datos"""
    return DB_PATH

def get_db_config():
    """Retorna la configuración de la base de datos"""
    return DB_CONFIG.copy()


class DatabaseManager:
    """Gestor principal de la base de datos con las 3 tablas requeridas"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()
        self.db_path = Path(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30
        )
    
    def init_database(self) -> bool:
        """Inicializa la base de datos con las 3 tablas requeridas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # ==============================
            # Tabla 1: Headcount
            # ==============================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS headcount (
                    scotia_id        VARCHAR(20) PRIMARY KEY,
                    employee         VARCHAR(100) NOT NULL,
                    full_name        VARCHAR(150) NOT NULL,
                    email            VARCHAR(150) NOT NULL,
                    position         VARCHAR(100),
                    manager          VARCHAR(100),
                    senior_manager   VARCHAR(100),
                    unit             VARCHAR(100),
                    start_date       DATE,
                    coca             VARCHAR(100),
                    skip_level       VARCHAR(100),
                    coleadores       VARCHAR(100),
                    parents          VARCHAR(100),
                    personal_email   VARCHAR(150),
                    size             VARCHAR(50),
                    birthday         DATE,
                    ubicacion        VARCHAR(100),
                    activo           BOOLEAN DEFAULT TRUE
                )
            ''')
            
            # ==============================
            # Tabla 2: Applications
            # ==============================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id SERIAL PRIMARY KEY,
                    jurisdiction         VARCHAR(100),
                    unit                 VARCHAR(100),
                    subunit              VARCHAR(100),
                    logical_access_name  VARCHAR(150) NOT NULL,
                    path_email_url       VARCHAR(255),
                    position_role        VARCHAR(100),
                    exception_tracking   VARCHAR(255),
                    fulfillment_action   VARCHAR(255),
                    system_owner         VARCHAR(100),
                    role_name            VARCHAR(100),
                    access_type          VARCHAR(50),
                    category             VARCHAR(100),
                    additional_data      VARCHAR(255),
                    ad_code              VARCHAR(100),
                    access_status        VARCHAR(50),
                    last_update_date     TIMESTAMP,
                    requirement_licensing VARCHAR(255),
                    description          TEXT,
                    authentication_method VARCHAR(100)
                )
            ''')
            
            # ==============================
            # Tabla 3: Historico
            # ==============================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico (
                    id SERIAL PRIMARY KEY,
                    scotia_id        VARCHAR(20) REFERENCES headcount(scotia_id),
                    case_id          VARCHAR(100),
                    responsible      VARCHAR(100),
                    record_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    process_access   VARCHAR(50),
                    sid              VARCHAR(100),
                    area             VARCHAR(100),
                    subunit          VARCHAR(100),
                    event_description TEXT,
                    ticket_email     VARCHAR(150),
                    app_access_name  VARCHAR(150) REFERENCES applications(logical_access_name),
                    computer_system_type VARCHAR(100),
                    status           VARCHAR(50),
                    closing_date_app DATE,
                    closing_date_ticket DATE,
                    app_quality      VARCHAR(50),
                    confirmation_by_user BOOLEAN,
                    comment          TEXT,
                    ticket_quality   VARCHAR(50),
                    general_status   VARCHAR(50),
                    average_time_open_ticket INTERVAL
                )
            ''')
            
            # Crear índices para mejor rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_scotia_id ON headcount (scotia_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_position ON headcount (position)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_headcount_unit ON headcount (unit)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_logical_access_name ON applications (logical_access_name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_position_role ON applications (position_role)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_historico_scotia_id ON historico (scotia_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_historico_process_access ON historico (process_access)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_historico_app_access_name ON historico (app_access_name)')
            
            conn.commit()
            conn.close()
            
            print("✅ Base de datos inicializada correctamente con las 3 tablas requeridas")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            return False
    
    def insert_sample_data(self) -> bool:
        """Inserta datos de ejemplo para las 3 tablas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insertar datos de ejemplo en headcount
            headcount_ejemplo = [
                ('EMP001', 'Juan Pérez', 'Juan Pérez', 'juan.perez@empresa.com', 'Desarrollador', 'María García', 'Carlos López', 'Tecnología', '2023-01-15', 'COCA001', 'Carlos López', 'María García', 'Juan Pérez', 'juan.personal@gmail.com', 'M', '1990-05-20', 'Oficina Central', True),
                ('EMP002', 'María García', 'María García', 'maria.garcia@empresa.com', 'Analista Senior', 'Carlos López', 'Ana Rodríguez', 'Tecnología', '2022-08-10', 'COCA002', 'Ana Rodríguez', 'Carlos López', 'María García', 'maria.personal@gmail.com', 'F', '1988-12-03', 'Oficina Central', True),
                ('EMP003', 'Carlos López', 'Carlos López', 'carlos.lopez@empresa.com', 'Gerente', 'Ana Rodríguez', 'Luis Martínez', 'Tecnología', '2021-03-22', 'COCA003', 'Luis Martínez', 'Ana Rodríguez', 'Carlos López', 'carlos.personal@gmail.com', 'M', '1985-09-15', 'Oficina Central', True),
                ('EMP004', 'Ana Rodríguez', 'Ana Rodríguez', 'ana.rodriguez@empresa.com', 'Desarrollador Senior', 'Luis Martínez', 'Carmen Silva', 'Tecnología', '2020-11-05', 'COCA004', 'Carmen Silva', 'Luis Martínez', 'Ana Rodríguez', 'ana.personal@gmail.com', 'F', '1987-07-28', 'Oficina Central', True),
                ('EMP005', 'Luis Martínez', 'Luis Martínez', 'luis.martinez@empresa.com', 'Analista', 'Carmen Silva', 'Pedro González', 'Recursos Humanos', '2023-06-12', 'COCA005', 'Pedro González', 'Carmen Silva', 'Luis Martínez', 'luis.personal@gmail.com', 'M', '1992-04-10', 'Oficina Central', True),
                ('EMP006', 'Carmen Silva', 'Carmen Silva', 'carmen.silva@empresa.com', 'Gerente', 'Pedro González', 'Sofia Herrera', 'Recursos Humanos', '2019-09-18', 'COCA006', 'Sofia Herrera', 'Pedro González', 'Carmen Silva', 'carmen.personal@gmail.com', 'F', '1983-11-25', 'Oficina Central', True)
            ]
            
            for row in headcount_ejemplo:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO headcount 
                        (scotia_id, employee, full_name, email, position, manager, senior_manager, unit, 
                         start_date, coca, skip_level, coleadores, parents, personal_email, size, birthday, ubicacion, activo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', row)
                except sqlite3.IntegrityError:
                    pass  # Ya existe
            
            # Insertar datos de ejemplo en applications - Aplicaciones completas para pruebas
            applications_ejemplo = [
                # ===== TECNOLOGÍA - DESARROLLADOR =====
                (1, 'Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Desarrollador', 'TRK001', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD001', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
                (2, 'Global', 'Tecnología', 'Desarrollo', 'GitLab', 'https://gitlab.empresa.com', 'Desarrollador', 'TRK002', 'Crear usuario', 'Admin GitLab', 'Developer', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD002', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Repositorio de código fuente', 'LDAP'),
                (3, 'Global', 'Tecnología', 'Desarrollo', 'Jira', 'https://jira.empresa.com', 'Desarrollador', 'TRK003', 'Asignar acceso', 'Admin Jira', 'Developer', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD003', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Gestión de proyectos y tickets', 'LDAP'),
                
                # ===== TECNOLOGÍA - DESARROLLADOR SENIOR =====
                (4, 'Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Desarrollador Senior', 'TRK004', 'Crear usuario', 'Admin Sistema', 'Administrador', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD004', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
                (5, 'Global', 'Tecnología', 'Desarrollo', 'GitLab', 'https://gitlab.empresa.com', 'Desarrollador Senior', 'TRK005', 'Crear usuario', 'Admin GitLab', 'Maintainer', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD005', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Repositorio de código fuente', 'LDAP'),
                (6, 'Global', 'Tecnología', 'Desarrollo', 'Jira', 'https://jira.empresa.com', 'Desarrollador Senior', 'TRK006', 'Asignar acceso', 'Admin Jira', 'Project Lead', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD006', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Gestión de proyectos y tickets', 'LDAP'),
                (7, 'Global', 'Tecnología', 'Desarrollo', 'Docker Registry', 'https://registry.empresa.com', 'Desarrollador Senior', 'TRK007', 'Crear usuario', 'Admin Docker', 'Maintainer', 'Aplicación', 'DevOps', 'Datos adicionales', 'AD007', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Registro de contenedores Docker', 'LDAP'),
                
                # ===== TECNOLOGÍA - ANALISTA =====
                (8, 'Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Analista', 'TRK008', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD008', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
                (9, 'Global', 'Tecnología', 'Desarrollo', 'Jira', 'https://jira.empresa.com', 'Analista', 'TRK009', 'Asignar acceso', 'Admin Jira', 'Analyst', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD009', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Gestión de proyectos y tickets', 'LDAP'),
                (10, 'Global', 'Tecnología', 'Desarrollo', 'Power BI', 'https://powerbi.empresa.com', 'Analista', 'TRK010', 'Crear usuario', 'Admin PowerBI', 'Analyst', 'Aplicación', 'Analytics', 'Datos adicionales', 'AD010', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Herramienta de análisis de datos', 'LDAP'),
                
                # ===== TECNOLOGÍA - GERENTE =====
                (11, 'Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Gerente', 'TRK011', 'Crear usuario', 'Admin Sistema', 'Administrador', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD011', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
                (12, 'Global', 'Tecnología', 'Desarrollo', 'GitLab', 'https://gitlab.empresa.com', 'Gerente', 'TRK012', 'Crear usuario', 'Admin GitLab', 'Owner', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD012', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Repositorio de código fuente', 'LDAP'),
                (13, 'Global', 'Tecnología', 'Desarrollo', 'Jira', 'https://jira.empresa.com', 'Gerente', 'TRK013', 'Asignar acceso', 'Admin Jira', 'Administrator', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD013', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Gestión de proyectos y tickets', 'LDAP'),
                (14, 'Global', 'Tecnología', 'Desarrollo', 'Power BI', 'https://powerbi.empresa.com', 'Gerente', 'TRK014', 'Crear usuario', 'Admin PowerBI', 'Administrator', 'Aplicación', 'Analytics', 'Datos adicionales', 'AD014', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Herramienta de análisis de datos', 'LDAP'),
                
                # ===== RECURSOS HUMANOS - ANALISTA =====
                (15, 'Global', 'Recursos Humanos', 'RRHH', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Analista', 'TRK015', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD015', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
                (16, 'Global', 'Recursos Humanos', 'RRHH', 'Workday', 'https://workday.empresa.com', 'Analista', 'TRK016', 'Crear usuario', 'Admin Workday', 'Analyst', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD016', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Sistema de gestión de RRHH', 'LDAP'),
                (17, 'Global', 'Recursos Humanos', 'RRHH', 'SuccessFactors', 'https://successfactors.empresa.com', 'Analista', 'TRK017', 'Crear usuario', 'Admin SuccessFactors', 'Analyst', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD017', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Gestión de talento y rendimiento', 'LDAP'),
                
                # ===== RECURSOS HUMANOS - GERENTE =====
                (18, 'Global', 'Recursos Humanos', 'RRHH', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Gerente', 'TRK018', 'Crear usuario', 'Admin Sistema', 'Administrador', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD018', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
                (19, 'Global', 'Recursos Humanos', 'RRHH', 'Workday', 'https://workday.empresa.com', 'Gerente', 'TRK019', 'Crear usuario', 'Admin Workday', 'Administrator', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD019', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Sistema de gestión de RRHH', 'LDAP'),
                (20, 'Global', 'Recursos Humanos', 'RRHH', 'SuccessFactors', 'https://successfactors.empresa.com', 'Gerente', 'TRK020', 'Crear usuario', 'Admin SuccessFactors', 'Administrator', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD020', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Gestión de talento y rendimiento', 'LDAP'),
                
                # ===== FINANZAS - ANALISTA =====
                (21, 'Global', 'Finanzas', 'Contabilidad', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Analista', 'TRK021', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD021', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
                (22, 'Global', 'Finanzas', 'Contabilidad', 'SAP', 'https://sap.empresa.com', 'Analista', 'TRK022', 'Crear usuario', 'Admin SAP', 'Analyst', 'Aplicación', 'ERP', 'Datos adicionales', 'AD022', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Sistema ERP de gestión empresarial', 'LDAP'),
                (23, 'Global', 'Finanzas', 'Contabilidad', 'Oracle Financials', 'https://oracle.empresa.com', 'Analista', 'TRK023', 'Crear usuario', 'Admin Oracle', 'Analyst', 'Aplicación', 'ERP', 'Datos adicionales', 'AD023', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Módulo financiero de Oracle', 'LDAP'),
                (24, 'Global', 'Finanzas', 'Contabilidad', 'Power BI', 'https://powerbi.empresa.com', 'Analista', 'TRK024', 'Crear usuario', 'Admin PowerBI', 'Analyst', 'Aplicación', 'Analytics', 'Datos adicionales', 'AD024', 'Activo', '2024-01-15 10:30:00', 'Licencia estándar', 'Herramienta de análisis de datos', 'LDAP'),
                
                # ===== FINANZAS - GERENTE =====
                (25, 'Global', 'Finanzas', 'Contabilidad', 'Sistema de Gestión', 'https://sistema.empresa.com', 'Gerente', 'TRK025', 'Crear usuario', 'Admin Sistema', 'Administrador', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD025', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
                (26, 'Global', 'Finanzas', 'Contabilidad', 'SAP', 'https://sap.empresa.com', 'Gerente', 'TRK026', 'Crear usuario', 'Admin SAP', 'Administrator', 'Aplicación', 'ERP', 'Datos adicionales', 'AD026', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Sistema ERP de gestión empresarial', 'LDAP'),
                (27, 'Global', 'Finanzas', 'Contabilidad', 'Oracle Financials', 'https://oracle.empresa.com', 'Gerente', 'TRK027', 'Crear usuario', 'Admin Oracle', 'Administrator', 'Aplicación', 'ERP', 'Datos adicionales', 'AD027', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Módulo financiero de Oracle', 'LDAP'),
                (28, 'Global', 'Finanzas', 'Contabilidad', 'Power BI', 'https://powerbi.empresa.com', 'Gerente', 'TRK028', 'Crear usuario', 'Admin PowerBI', 'Administrator', 'Aplicación', 'Analytics', 'Datos adicionales', 'AD028', 'Activo', '2024-01-15 10:30:00', 'Licencia premium', 'Herramienta de análisis de datos', 'LDAP')
            ]
            
            for row in applications_ejemplo:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO applications 
                        (id, jurisdiction, unit, subunit, logical_access_name, path_email_url, position_role, 
                         exception_tracking, fulfillment_action, system_owner, role_name, access_type, category, 
                         additional_data, ad_code, access_status, last_update_date, requirement_licensing, description, authentication_method)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', row)
                except sqlite3.IntegrityError:
                    pass  # Ya existe
            
            # Insertar datos de ejemplo en historico
            historico_ejemplo = [
                (1, 'EMP001', 'CASE-20240115-001', 'Admin Sistema', '2024-01-15 09:00:00', 'onboarding', 'EMP001', 'Tecnología', 'Desarrollo', 'Usuario creado en sistema', 'admin@empresa.com', 'Sistema de Gestión', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', True, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:30:00'),
                (2, 'EMP002', 'CASE-20240115-002', 'Admin Portal', '2024-01-15 10:00:00', 'onboarding', 'EMP002', 'Tecnología', 'Desarrollo', 'Usuario creado en portal', 'admin@empresa.com', 'Portal de Recursos', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', True, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:45:00'),
                (3, 'EMP003', 'CASE-20240115-003', 'Admin Sistema', '2024-01-15 11:00:00', 'onboarding', 'EMP003', 'Tecnología', 'Desarrollo', 'Usuario creado en sistema', 'admin@empresa.com', 'Sistema de Gestión', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', True, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:20:00'),
                (4, 'EMP004', 'CASE-20240115-004', 'Admin Portal', '2024-01-15 12:00:00', 'onboarding', 'EMP004', 'Tecnología', 'Desarrollo', 'Usuario creado en portal', 'admin@empresa.com', 'Portal de Recursos', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', True, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:35:00'),
                (5, 'EMP005', 'CASE-20240115-005', 'Admin Sistema', '2024-01-15 13:00:00', 'onboarding', 'EMP005', 'Recursos Humanos', 'RRHH', 'Usuario creado en sistema', 'admin@empresa.com', 'Sistema de Gestión', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', True, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:25:00'),
                (6, 'EMP006', 'CASE-20240115-006', 'Admin Portal', '2024-01-15 14:00:00', 'onboarding', 'EMP006', 'Recursos Humanos', 'RRHH', 'Usuario creado en portal', 'admin@empresa.com', 'Portal de Recursos', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', True, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:40:00')
            ]
            
            for row in historico_ejemplo:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO historico 
                        (id, scotia_id, case_id, responsible, record_date, process_access, sid, area, subunit, 
                         event_description, ticket_email, app_access_name, computer_system_type, status, 
                         closing_date_app, closing_date_ticket, app_quality, confirmation_by_user, comment, 
                         ticket_quality, general_status, average_time_open_ticket)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', row)
                except sqlite3.IntegrityError:
                    pass  # Ya existe
            
            conn.commit()
            conn.close()
            
            print("✅ Datos de ejemplo insertados correctamente en las 3 tablas")
            return True
            
        except Exception as e:
            print(f"❌ Error insertando datos de ejemplo: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            stats = {}
            
            # Contar registros en headcount
            cursor.execute('SELECT COUNT(*) FROM headcount')
            stats['headcount'] = cursor.fetchone()[0]
            
            # Contar registros en applications
            cursor.execute('SELECT COUNT(*) FROM applications')
            stats['applications'] = cursor.fetchone()[0]
            
            # Contar registros en historico
            cursor.execute('SELECT COUNT(*) FROM historico')
            stats['historico'] = cursor.fetchone()[0]
            
            # Contar empleados activos
            cursor.execute('SELECT COUNT(*) FROM headcount WHERE activo = 1')
            stats['empleados_activos'] = cursor.fetchone()[0]
            
            # Contar aplicaciones activas
            cursor.execute('SELECT COUNT(*) FROM applications WHERE access_status = "Activo"')
            stats['aplicaciones_activas'] = cursor.fetchone()[0]
            
            conn.close()
            return stats
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def backup_database(self, backup_path: str = None) -> bool:
        """Crea una copia de seguridad de la base de datos"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backup_empleados_{timestamp}.db"
            
            backup_path = os.path.join(os.path.dirname(self.db_path), backup_path)
            shutil.copy2(str(self.db_path), backup_path)
            
            print(f"✅ Copia de seguridad creada: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando copia de seguridad: {e}")
            return False
    
    def cleanup_old_backups(self, keep_days: int = 7) -> int:
        """Elimina copias de seguridad antiguas"""
        try:
            backup_dir = os.path.dirname(self.db_path)
            current_time = datetime.now()
            backups_removed = 0
            
            for filename in os.listdir(backup_dir):
                if filename.startswith("backup_empleados_") and filename.endswith(".db"):
                    file_path = os.path.join(backup_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if (current_time - file_time).days > keep_days:
                        os.remove(file_path)
                        backups_removed += 1
            
            if backups_removed > 0:
                print(f"✅ {backups_removed} copias de seguridad antiguas eliminadas")
            
            return backups_removed
            
        except Exception as e:
            print(f"❌ Error limpiando copias de seguridad: {e}")
            return 0


# Funciones helper para uso directo
def init_database() -> bool:
    """Función helper para inicializar la base de datos"""
    manager = DatabaseManager()
    return manager.init_database()

def insert_sample_data() -> bool:
    """Función helper para insertar datos de ejemplo"""
    manager = DatabaseManager()
    return manager.insert_sample_data()

def get_database_stats() -> Dict[str, int]:
    """Función helper para obtener estadísticas"""
    manager = DatabaseManager()
    return manager.get_database_stats()

def backup_database(backup_path: str = None) -> bool:
    """Función helper para crear copia de seguridad"""
    manager = DatabaseManager()
    return manager.backup_database(backup_path)

def cleanup_old_backups(keep_days: int = 7) -> int:
    """Función helper para limpiar copias antiguas"""
    manager = DatabaseManager()
    return manager.cleanup_old_backups(keep_days)


# Instancia global para usar en toda la aplicación
db_manager = DatabaseManager()


if __name__ == "__main__":
    """Script principal para inicializar la base de datos"""
    print("🚀 Inicializando base de datos con las 3 tablas requeridas...")
    
    if init_database():
        if insert_sample_data():
            stats = get_database_stats()
            print(f"\n📊 Estadísticas de la base de datos:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            print("\n✅ Base de datos completamente configurada!")
        else:
            print("❌ Error insertando datos de ejemplo")
    else:
        print("❌ Error inicializando base de datos")