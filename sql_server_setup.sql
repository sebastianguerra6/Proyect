-- =====================================================
-- SCRIPT DE CONFIGURACIÓN PARA SQL SERVER
-- Sistema de Gestión de Empleados y Conciliación de Accesos
-- =====================================================

-- Crear base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'GAMLO_Empleados')
BEGIN
    CREATE DATABASE GAMLO_Empleados;
END
GO

USE GAMLO_Empleados;
GO

-- =====================================================
-- TABLA 1: HEADCOUNT (Empleados)
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[headcount]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[headcount] (
        [scotia_id] VARCHAR(20) NOT NULL PRIMARY KEY,
        [employee] VARCHAR(100) NOT NULL,
        [full_name] VARCHAR(150) NOT NULL,
        [email] VARCHAR(150) NOT NULL,
        [position] VARCHAR(100) NULL,
        [manager] VARCHAR(100) NULL,
        [senior_manager] VARCHAR(100) NULL,
        [unit] VARCHAR(100) NULL,
        [start_date] DATE NULL,
        [ceco] VARCHAR(100) NULL,
        [skip_level] VARCHAR(100) NULL,
        [cafe_alcides] VARCHAR(100) NULL,
        [parents] VARCHAR(100) NULL,
        [personal_email] VARCHAR(150) NULL,
        [size] VARCHAR(50) NULL,
        [birthday] DATE NULL,
        [validacion] VARCHAR(100) NULL,
        [activo] BIT NOT NULL DEFAULT 1,
        [inactivation_date] DATE NULL
    );
END
GO

-- =====================================================
-- TABLA 2: APPLICATIONS (Aplicaciones y Accesos)
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[applications]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[applications] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [jurisdiction] VARCHAR(100) NULL,
        [unit] VARCHAR(100) NULL,
        [subunit] VARCHAR(100) NULL,
        [logical_access_name] VARCHAR(150) NOT NULL,
        [alias] VARCHAR(150) NULL,
        [path_email_url] VARCHAR(255) NULL,
        [position_role] VARCHAR(100) NULL,
        [exception_tracking] VARCHAR(255) NULL,
        [fulfillment_action] VARCHAR(255) NULL,
        [system_owner] VARCHAR(100) NULL,
        [role_name] VARCHAR(100) NULL,
        [access_type] VARCHAR(50) NULL,
        [category] VARCHAR(100) NULL,
        [additional_data] VARCHAR(255) NULL,
        [ad_code] VARCHAR(100) NULL,
        [access_status] VARCHAR(50) NULL,
        [last_update_date] DATETIME2 NULL,
        [require_licensing] VARCHAR(255) NULL,
        [description] TEXT NULL,
        [authentication_method] VARCHAR(100) NULL
    );
END
GO

-- =====================================================
-- TABLA 3: HISTORICO (Historial de Procesos)
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[historico]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[historico] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [scotia_id] VARCHAR(20) NOT NULL,
        [case_id] VARCHAR(100) NULL,
        [responsible] VARCHAR(100) NULL,
        [record_date] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [request_date] DATE NULL,
        [process_access] VARCHAR(50) NULL,
        [sid] VARCHAR(100) NULL,
        [area] VARCHAR(100) NULL,
        [subunit] VARCHAR(100) NULL,
        [event_description] TEXT NULL,
        [ticket_email] VARCHAR(150) NULL,
        [app_access_name] VARCHAR(150) NULL,
        [computer_system_type] VARCHAR(100) NULL,
        [status] VARCHAR(50) NULL,
        [closing_date_app] DATE NULL,
        [closing_date_ticket] DATE NULL,
        [app_quality] VARCHAR(50) NULL,
        [confirmation_by_user] BIT NULL,
        [comment] TEXT NULL,
        [ticket_quality] VARCHAR(50) NULL,
        [general_status] VARCHAR(50) NULL,
        [average_time_open_ticket] TIME NULL,
        
        -- Foreign Key Constraints
        CONSTRAINT [FK_historico_headcount] FOREIGN KEY ([scotia_id]) 
            REFERENCES [dbo].[headcount]([scotia_id]) ON DELETE CASCADE,
        CONSTRAINT [FK_historico_applications] FOREIGN KEY ([app_access_name]) 
            REFERENCES [dbo].[applications]([logical_access_name]) ON DELETE SET NULL
    );
END
GO

-- =====================================================
-- TABLA 4: PROCESOS (Gestión de Procesos)
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[procesos]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[procesos] (
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [sid] VARCHAR(20) NOT NULL,
        [nueva_sub_unidad] VARCHAR(100) NULL,
        [nuevo_cargo] VARCHAR(100) NULL,
        [status] VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
        [request_date] DATE NULL,
        [ingreso_por] VARCHAR(100) NULL,
        [fecha_creacion] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [fecha_actualizacion] DATETIME2 NULL,
        [tipo_proceso] VARCHAR(50) NULL,
        [app_name] VARCHAR(150) NULL,
        [mail] VARCHAR(150) NULL,
        [closing_date_app] DATE NULL,
        [app_quality] VARCHAR(50) NULL,
        [confirmation_by_user] VARCHAR(50) NULL,
        [comment] TEXT NULL,
        
        -- Foreign Key Constraint
        CONSTRAINT [FK_procesos_headcount] FOREIGN KEY ([sid]) 
            REFERENCES [dbo].[headcount]([scotia_id]) ON DELETE CASCADE
    );
END
GO

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para headcount
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_headcount_scotia_id' AND object_id = OBJECT_ID('headcount'))
    CREATE INDEX IX_headcount_scotia_id ON [dbo].[headcount] ([scotia_id]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_headcount_position' AND object_id = OBJECT_ID('headcount'))
    CREATE INDEX IX_headcount_position ON [dbo].[headcount] ([position]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_headcount_unit' AND object_id = OBJECT_ID('headcount'))
    CREATE INDEX IX_headcount_unit ON [dbo].[headcount] ([unit]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_headcount_activo' AND object_id = OBJECT_ID('headcount'))
    CREATE INDEX IX_headcount_activo ON [dbo].[headcount] ([activo]);

-- Índices para applications
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_logical_access_name' AND object_id = OBJECT_ID('applications'))
    CREATE INDEX IX_applications_logical_access_name ON [dbo].[applications] ([logical_access_name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_position_role' AND object_id = OBJECT_ID('applications'))
    CREATE INDEX IX_applications_position_role ON [dbo].[applications] ([position_role]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_alias' AND object_id = OBJECT_ID('applications'))
    CREATE INDEX IX_applications_alias ON [dbo].[applications] ([alias]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_unit_position' AND object_id = OBJECT_ID('applications'))
    CREATE INDEX IX_applications_unit_position ON [dbo].[applications] ([unit], [position_role]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_access_status' AND object_id = OBJECT_ID('applications'))
    CREATE INDEX IX_applications_access_status ON [dbo].[applications] ([access_status]);

-- Índices para historico
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_scotia_id' AND object_id = OBJECT_ID('historico'))
    CREATE INDEX IX_historico_scotia_id ON [dbo].[historico] ([scotia_id]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_process_access' AND object_id = OBJECT_ID('historico'))
    CREATE INDEX IX_historico_process_access ON [dbo].[historico] ([process_access]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_app_access_name' AND object_id = OBJECT_ID('historico'))
    CREATE INDEX IX_historico_app_access_name ON [dbo].[historico] ([app_access_name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_record_date' AND object_id = OBJECT_ID('historico'))
    CREATE INDEX IX_historico_record_date ON [dbo].[historico] ([record_date]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_status' AND object_id = OBJECT_ID('historico'))
    CREATE INDEX IX_historico_status ON [dbo].[historico] ([status]);

-- Índices para procesos
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_procesos_sid' AND object_id = OBJECT_ID('procesos'))
    CREATE INDEX IX_procesos_sid ON [dbo].[procesos] ([sid]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_procesos_status' AND object_id = OBJECT_ID('procesos'))
    CREATE INDEX IX_procesos_status ON [dbo].[procesos] ([status]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_procesos_tipo' AND object_id = OBJECT_ID('procesos'))
    CREATE INDEX IX_procesos_tipo ON [dbo].[procesos] ([tipo_proceso]);

-- =====================================================
-- VISTAS PARA EL SISTEMA
-- =====================================================

-- Vista 1: Aplicaciones requeridas por (unit, position)
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_required_apps')
    DROP VIEW [dbo].[vw_required_apps];
GO

CREATE VIEW [dbo].[vw_required_apps] AS
SELECT 
    h.scotia_id,
    h.unit,
    h.position,
    a.logical_access_name,
    a.subunit,
    a.position_role,
    a.role_name,
    a.system_owner,
    a.access_type,
    a.category,
    a.description
FROM [dbo].[headcount] h
INNER JOIN (
    SELECT DISTINCT
        logical_access_name,
        unit,
        position_role,
        subunit,
        role_name,
        system_owner,
        access_type,
        category,
        description
    FROM [dbo].[applications]
    WHERE access_status = 'Activo'
) a ON 
    UPPER(LTRIM(RTRIM(h.unit))) = UPPER(LTRIM(RTRIM(a.unit))) AND
    UPPER(LTRIM(RTRIM(h.position))) = UPPER(LTRIM(RTRIM(a.position_role)))
WHERE h.activo = 1
GROUP BY h.scotia_id, a.logical_access_name, h.unit, h.position, a.subunit, a.position_role, 
         a.role_name, a.system_owner, a.access_type, a.category, a.description
ORDER BY h.scotia_id, a.logical_access_name;
GO

-- Vista 2: Accesos actuales (completados y pendientes)
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_current_access')
    DROP VIEW [dbo].[vw_current_access];
GO

CREATE VIEW [dbo].[vw_current_access] AS
SELECT 
    h.scotia_id,
    head.unit,
    head.position,
    h.app_access_name as logical_access_name,
    h.area as subunit,
    head.position as position_role,
    h.record_date,
    h.status
FROM [dbo].[historico] h
INNER JOIN [dbo].[headcount] head ON h.scotia_id = head.scotia_id
WHERE h.status IN ('Completado', 'Pendiente', 'En Proceso', 'Cancelado', 'Rechazado')
AND h.process_access IN ('onboarding', 'lateral_movement')
AND head.activo = 1
AND h.app_access_name IS NOT NULL
GROUP BY h.scotia_id, h.app_access_name, head.unit, head.position, h.area, h.record_date, h.status
ORDER BY h.scotia_id, h.app_access_name;
GO

-- Vista 3: Accesos por otorgar
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_to_grant')
    DROP VIEW [dbo].[vw_to_grant];
GO

CREATE VIEW [dbo].[vw_to_grant] AS
SELECT 
    req.scotia_id,
    req.unit,
    req.position,
    req.logical_access_name,
    req.subunit,
    req.position_role,
    'onboarding' as process_type
FROM [dbo].[vw_required_apps] req
LEFT JOIN [dbo].[vw_current_access] curr ON 
    req.scotia_id = curr.scotia_id AND
    UPPER(LTRIM(RTRIM(req.logical_access_name))) = UPPER(LTRIM(RTRIM(curr.logical_access_name))) AND
    UPPER(LTRIM(RTRIM(req.unit))) = UPPER(LTRIM(RTRIM(curr.unit))) AND
    UPPER(LTRIM(RTRIM(req.position))) = UPPER(LTRIM(RTRIM(curr.position)))
WHERE curr.scotia_id IS NULL
ORDER BY req.scotia_id, req.logical_access_name;
GO

-- Vista 4: Accesos por revocar
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_to_revoke')
    DROP VIEW [dbo].[vw_to_revoke];
GO

CREATE VIEW [dbo].[vw_to_revoke] AS
SELECT 
    curr.scotia_id,
    curr.unit,
    curr.position,
    curr.logical_access_name,
    curr.subunit,
    curr.position_role,
    curr.record_date,
    'offboarding' as process_type
FROM [dbo].[vw_current_access] curr
LEFT JOIN [dbo].[vw_required_apps] req ON 
    curr.scotia_id = req.scotia_id AND
    UPPER(LTRIM(RTRIM(curr.logical_access_name))) = UPPER(LTRIM(RTRIM(req.logical_access_name))) AND
    UPPER(LTRIM(RTRIM(curr.unit))) = UPPER(LTRIM(RTRIM(req.unit))) AND
    UPPER(LTRIM(RTRIM(curr.position))) = UPPER(LTRIM(RTRIM(req.position)))
WHERE req.scotia_id IS NULL
ORDER BY curr.scotia_id, curr.logical_access_name;
GO

-- Vista 5: Estadísticas del sistema
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_system_stats')
    DROP VIEW [dbo].[vw_system_stats];
GO

CREATE VIEW [dbo].[vw_system_stats] AS
SELECT 
    (SELECT COUNT(*) FROM [dbo].[headcount]) as total_empleados,
    (SELECT COUNT(*) FROM [dbo].[headcount] WHERE activo = 1) as empleados_activos,
    (SELECT COUNT(*) FROM [dbo].[applications]) as total_aplicaciones,
    (SELECT COUNT(*) FROM [dbo].[applications] WHERE access_status = 'Activo') as aplicaciones_activas,
    (SELECT COUNT(*) FROM [dbo].[historico]) as total_historico,
    (SELECT COUNT(*) FROM [dbo].[procesos]) as total_procesos,
    (SELECT COUNT(*) FROM [dbo].[historico] WHERE process_access = 'onboarding') as total_onboarding,
    (SELECT COUNT(*) FROM [dbo].[historico] WHERE process_access = 'offboarding') as total_offboarding,
    (SELECT COUNT(*) FROM [dbo].[historico] WHERE process_access = 'lateral_movement') as total_lateral_movement;
GO

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- =====================================================

-- Procedimiento para obtener estadísticas de la base de datos
IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_GetDatabaseStats')
    DROP PROCEDURE [dbo].[sp_GetDatabaseStats];
GO

CREATE PROCEDURE [dbo].[sp_GetDatabaseStats]
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        'headcount' as tabla,
        COUNT(*) as registros
    FROM [dbo].[headcount]
    
    UNION ALL
    
    SELECT 
        'empleados_activos' as tabla,
        COUNT(*) as registros
    FROM [dbo].[headcount] 
    WHERE activo = 1
    
    UNION ALL
    
    SELECT 
        'applications' as tabla,
        COUNT(*) as registros
    FROM [dbo].[applications]
    
    UNION ALL
    
    SELECT 
        'aplicaciones_activas' as tabla,
        COUNT(*) as registros
    FROM [dbo].[applications] 
    WHERE access_status = 'Activo'
    
    UNION ALL
    
    SELECT 
        'historico' as tabla,
        COUNT(*) as registros
    FROM [dbo].[historico]
    
    UNION ALL
    
    SELECT 
        'procesos' as tabla,
        COUNT(*) as registros
    FROM [dbo].[procesos];
END
GO

-- Procedimiento para obtener historial de un empleado
IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_GetEmployeeHistory')
    DROP PROCEDURE [dbo].[sp_GetEmployeeHistory];
GO

CREATE PROCEDURE [dbo].[sp_GetEmployeeHistory]
    @scotia_id VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        h.*, 
        a.logical_access_name AS app_logical_access_name,
        a.description AS app_description,
        a.unit AS app_unit,
        a.subunit AS app_subunit,
        a.position_role AS app_position_role
    FROM [dbo].[historico] h
    LEFT JOIN (
        SELECT 
            logical_access_name,
            description,
            unit,
            subunit,
            position_role,
            ROW_NUMBER() OVER (PARTITION BY logical_access_name ORDER BY id) as rn
        FROM [dbo].[applications]
    ) a ON h.app_access_name = a.logical_access_name AND a.rn = 1
    WHERE h.scotia_id = @scotia_id
    ORDER BY h.record_date DESC;
END
GO

-- Procedimiento para obtener aplicaciones por posición
IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_GetApplicationsByPosition')
    DROP PROCEDURE [dbo].[sp_GetApplicationsByPosition];
GO

CREATE PROCEDURE [dbo].[sp_GetApplicationsByPosition]
    @position VARCHAR(100),
    @unit VARCHAR(100),
    @subunit VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT DISTINCT
        logical_access_name,
        unit,
        subunit,
        position_role,
        role_name,
        system_owner,
        access_type,
        category,
        description
    FROM [dbo].[applications]
    WHERE access_status = 'Activo'
    AND UPPER(LTRIM(RTRIM(unit))) = UPPER(LTRIM(RTRIM(@unit)))
    AND UPPER(LTRIM(RTRIM(position_role))) = UPPER(LTRIM(RTRIM(@position)))
    AND (@subunit IS NULL OR UPPER(LTRIM(RTRIM(subunit))) = UPPER(LTRIM(RTRIM(@subunit))))
    ORDER BY logical_access_name;
END
GO

-- =====================================================
-- FUNCIONES
-- =====================================================

-- Función para normalizar texto (equivalente a TRIM en SQL Server)
IF EXISTS (SELECT * FROM sys.objects WHERE name = 'fn_NormalizeText' AND type = 'FN')
    DROP FUNCTION [dbo].[fn_NormalizeText];
GO

CREATE FUNCTION [dbo].[fn_NormalizeText](@text VARCHAR(MAX))
RETURNS VARCHAR(MAX)
AS
BEGIN
    RETURN LTRIM(RTRIM(@text));
END
GO

-- =====================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- =====================================================

-- Insertar datos de ejemplo en headcount
INSERT INTO [dbo].[headcount] (scotia_id, employee, full_name, email, position, manager, senior_manager, unit, start_date, ceco, skip_level, cafe_alcides, parents, personal_email, size, birthday, validacion, activo)
VALUES 
    ('EMP001', 'Juan Pérez', 'Juan Pérez', 'juan.perez@empresa.com', 'Desarrollador', 'María García', 'Carlos López', 'Tecnología', '2023-01-15', 'CECO001', 'Carlos López', 'María García', 'Juan Pérez', 'juan.personal@gmail.com', 'M', '1990-05-20', 'Oficina Central', 1),
    ('EMP002', 'María García', 'María García', 'maria.garcia@empresa.com', 'Analista Senior', 'Carlos López', 'Ana Rodríguez', 'Tecnología', '2022-08-10', 'CECO002', 'Ana Rodríguez', 'Carlos López', 'María García', 'maria.personal@gmail.com', 'F', '1988-12-03', 'Oficina Central', 1),
    ('EMP003', 'Carlos López', 'Carlos López', 'carlos.lopez@empresa.com', 'Gerente', 'Ana Rodríguez', 'Luis Martínez', 'Tecnología', '2021-03-22', 'CECO003', 'Luis Martínez', 'Ana Rodríguez', 'Carlos López', 'carlos.personal@gmail.com', 'M', '1985-09-15', 'Oficina Central', 1),
    ('EMP004', 'Ana Rodríguez', 'Ana Rodríguez', 'ana.rodriguez@empresa.com', 'Desarrollador Senior', 'Luis Martínez', 'Carmen Silva', 'Tecnología', '2020-11-05', 'CECO004', 'Carmen Silva', 'Luis Martínez', 'Ana Rodríguez', 'ana.personal@gmail.com', 'F', '1987-07-28', 'Oficina Central', 1),
    ('EMP005', 'Luis Martínez', 'Luis Martínez', 'luis.martinez@empresa.com', 'Analista', 'Carmen Silva', 'Pedro González', 'Recursos Humanos', '2023-06-12', 'CECO005', 'Pedro González', 'Carmen Silva', 'Luis Martínez', 'luis.personal@gmail.com', 'M', '1992-04-10', 'Oficina Central', 1),
    ('EMP006', 'Carmen Silva', 'Carmen Silva', 'carmen.silva@empresa.com', 'Gerente', 'Pedro González', 'Sofia Herrera', 'Recursos Humanos', '2019-09-18', 'CECO006', 'Sofia Herrera', 'Pedro González', 'Carmen Silva', 'carmen.personal@gmail.com', 'F', '1983-11-25', 'Oficina Central', 1);

-- Insertar datos de ejemplo en applications
INSERT INTO [dbo].[applications] (jurisdiction, unit, subunit, logical_access_name, alias, path_email_url, position_role, exception_tracking, fulfillment_action, system_owner, role_name, access_type, category, additional_data, ad_code, access_status, last_update_date, require_licensing, description, authentication_method)
VALUES 
    -- TECNOLOGÍA - DESARROLLADOR
    ('Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'SIS-GEST', 'https://sistema.empresa.com', 'Desarrollador', 'TRK001', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD001', 'Activo', GETDATE(), 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
    ('Global', 'Tecnología', 'Desarrollo', 'GitLab', 'GIT-REPO', 'https://gitlab.empresa.com', 'Desarrollador', 'TRK002', 'Crear usuario', 'Admin GitLab', 'Developer', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD002', 'Activo', GETDATE(), 'Licencia estándar', 'Repositorio de código fuente', 'LDAP'),
    ('Global', 'Tecnología', 'Desarrollo', 'Jira', 'JIRA-PROJ', 'https://jira.empresa.com', 'Desarrollador', 'TRK003', 'Asignar acceso', 'Admin Jira', 'Developer', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD003', 'Activo', GETDATE(), 'Licencia estándar', 'Gestión de proyectos y tickets', 'LDAP'),
    
    -- TECNOLOGÍA - ANALISTA SENIOR
    ('Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'SIS-GEST-ADM', 'https://sistema.empresa.com', 'Analista Senior', 'TRK004', 'Crear usuario', 'Admin Sistema', 'Administrador', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD004', 'Activo', GETDATE(), 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
    ('Global', 'Tecnología', 'Desarrollo', 'GitLab', 'GIT-REPO-ADM', 'https://gitlab.empresa.com', 'Analista Senior', 'TRK005', 'Crear usuario', 'Admin GitLab', 'Maintainer', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD005', 'Activo', GETDATE(), 'Licencia premium', 'Repositorio de código fuente', 'LDAP'),
    ('Global', 'Tecnología', 'Desarrollo', 'Jira', 'JIRA-PROJ-ADM', 'https://jira.empresa.com', 'Analista Senior', 'TRK006', 'Asignar acceso', 'Admin Jira', 'Project Lead', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD006', 'Activo', GETDATE(), 'Licencia premium', 'Gestión de proyectos y tickets', 'LDAP'),
    ('Global', 'Tecnología', 'Desarrollo', 'Docker Registry', 'DOCK-REG', 'https://registry.empresa.com', 'Analista Senior', 'TRK007', 'Crear usuario', 'Admin Docker', 'Maintainer', 'Aplicación', 'DevOps', 'Datos adicionales', 'AD007', 'Activo', GETDATE(), 'Licencia premium', 'Registro de contenedores Docker', 'LDAP'),
    
    -- RECURSOS HUMANOS - ANALISTA
    ('Global', 'Recursos Humanos', 'RRHH', 'Sistema de Gestión', 'SIS-GEST-RRHH', 'https://sistema.empresa.com', 'Analista', 'TRK015', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD015', 'Activo', GETDATE(), 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
    ('Global', 'Recursos Humanos', 'RRHH', 'Workday', 'WD-RRHH', 'https://workday.empresa.com', 'Analista', 'TRK016', 'Crear usuario', 'Admin Workday', 'Analyst', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD016', 'Activo', GETDATE(), 'Licencia estándar', 'Sistema de gestión de RRHH', 'LDAP'),
    ('Global', 'Recursos Humanos', 'RRHH', 'SuccessFactors', 'SF-RRHH', 'https://successfactors.empresa.com', 'Analista', 'TRK017', 'Crear usuario', 'Admin SuccessFactors', 'Analyst', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD017', 'Activo', GETDATE(), 'Licencia estándar', 'Gestión de talento y rendimiento', 'LDAP');

-- Insertar datos de ejemplo en historico
INSERT INTO [dbo].[historico] (scotia_id, case_id, responsible, record_date, request_date, process_access, sid, area, subunit, event_description, ticket_email, app_access_name, computer_system_type, status, closing_date_app, closing_date_ticket, app_quality, confirmation_by_user, comment, ticket_quality, general_status, average_time_open_ticket)
VALUES 
    ('EMP001', 'CASE-20240115-001', 'Admin Sistema', GETDATE(), '2024-01-14', 'onboarding', 'EMP001', 'Tecnología', 'Desarrollo', 'Usuario creado en sistema', 'admin@empresa.com', 'Sistema de Gestión', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', 1, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:30:00'),
    ('EMP002', 'CASE-20240115-002', 'Admin Portal', GETDATE(), '2024-01-14', 'onboarding', 'EMP002', 'Tecnología', 'Desarrollo', 'Usuario creado en portal', 'admin@empresa.com', 'GitLab', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', 1, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:45:00'),
    ('EMP003', 'CASE-20240115-003', 'Admin Sistema', GETDATE(), '2024-01-14', 'onboarding', 'EMP003', 'Tecnología', 'Desarrollo', 'Usuario creado en sistema', 'admin@empresa.com', 'Jira', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', 1, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:20:00');

-- =====================================================
-- VERIFICACIÓN FINAL
-- =====================================================

-- Mostrar estadísticas de las tablas creadas
SELECT 'headcount' as tabla, COUNT(*) as registros FROM [dbo].[headcount]
UNION ALL
SELECT 'applications' as tabla, COUNT(*) as registros FROM [dbo].[applications]
UNION ALL
SELECT 'historico' as tabla, COUNT(*) as registros FROM [dbo].[historico]
UNION ALL
SELECT 'procesos' as tabla, COUNT(*) as registros FROM [dbo].[procesos];

-- Mostrar las vistas creadas
SELECT 'vw_required_apps' as vista, COUNT(*) as registros FROM [dbo].[vw_required_apps]
UNION ALL
SELECT 'vw_current_access' as vista, COUNT(*) as registros FROM [dbo].[vw_current_access]
UNION ALL
SELECT 'vw_to_grant' as vista, COUNT(*) as registros FROM [dbo].[vw_to_grant]
UNION ALL
SELECT 'vw_to_revoke' as vista, COUNT(*) as registros FROM [dbo].[vw_to_revoke]
UNION ALL
SELECT 'vw_system_stats' as vista, COUNT(*) as registros FROM [dbo].[vw_system_stats];

PRINT '=====================================================';
PRINT 'CONFIGURACIÓN COMPLETADA EXITOSAMENTE';
PRINT 'Base de datos: GAMLO_Empleados';
PRINT 'Tablas creadas: headcount, applications, historico, procesos';
PRINT 'Vistas creadas: vw_required_apps, vw_current_access, vw_to_grant, vw_to_revoke, vw_system_stats';
PRINT 'Procedimientos creados: sp_GetDatabaseStats, sp_GetEmployeeHistory, sp_GetApplicationsByPosition';
PRINT 'Función creada: fn_NormalizeText';
PRINT 'Datos de ejemplo insertados correctamente';
PRINT '=====================================================';
