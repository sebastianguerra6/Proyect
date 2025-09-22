-- =====================================================
-- SCRIPT DE CONFIGURACIÓN CORREGIDO PARA SQL SERVER
-- Sistema de Gestión de Empleados y Conciliación de Accesos
-- =====================================================

-- Crear base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'GAMLO_Empleados')
BEGIN
    CREATE DATABASE GAMLO_Empleados;
    PRINT 'Base de datos GAMLO_Empleados creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Base de datos GAMLO_Empleados ya existe';
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
    PRINT 'Tabla headcount creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla headcount ya existe';
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
        [description] NVARCHAR(MAX) NULL,
        [authentication_method] VARCHAR(100) NULL
    );
    PRINT 'Tabla applications creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla applications ya existe';
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
        [event_description] NVARCHAR(MAX) NULL,
        [ticket_email] VARCHAR(150) NULL,
        [app_access_name] VARCHAR(150) NULL,
        [computer_system_type] VARCHAR(100) NULL,
        [status] VARCHAR(50) NULL,
        [closing_date_app] DATE NULL,
        [closing_date_ticket] DATE NULL,
        [app_quality] VARCHAR(50) NULL,
        [confirmation_by_user] BIT NULL,
        [comment] NVARCHAR(MAX) NULL,
        [ticket_quality] VARCHAR(50) NULL,
        [general_status] VARCHAR(50) NULL,
        [average_time_open_ticket] VARCHAR(20) NULL
    );
    PRINT 'Tabla historico creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla historico ya existe';
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
        [comment] NVARCHAR(MAX) NULL
    );
    PRINT 'Tabla procesos creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla procesos ya existe';
END
GO

-- =====================================================
-- CREAR FOREIGN KEYS DESPUÉS DE CREAR TODAS LAS TABLAS
-- =====================================================

-- Foreign Key para historico -> headcount
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_historico_headcount')
BEGIN
    ALTER TABLE [dbo].[historico]
    ADD CONSTRAINT [FK_historico_headcount] 
    FOREIGN KEY ([scotia_id]) REFERENCES [dbo].[headcount]([scotia_id]) ON DELETE CASCADE;
    PRINT 'Foreign Key FK_historico_headcount creada exitosamente';
END
GO

-- Foreign Key para historico -> applications
-- COMENTADO: No se puede crear porque logical_access_name no es UNIQUE
-- IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_historico_applications')
-- BEGIN
--     ALTER TABLE [dbo].[historico]
--     ADD CONSTRAINT [FK_historico_applications] 
--     FOREIGN KEY ([app_access_name]) REFERENCES [dbo].[applications]([logical_access_name]) ON DELETE SET NULL;
--     PRINT 'Foreign Key FK_historico_applications creada exitosamente';
-- END
PRINT 'Foreign Key FK_historico_applications omitida: logical_access_name no es UNIQUE en applications';
GO

-- Foreign Key para procesos -> headcount
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_procesos_headcount')
BEGIN
    ALTER TABLE [dbo].[procesos]
    ADD CONSTRAINT [FK_procesos_headcount] 
    FOREIGN KEY ([sid]) REFERENCES [dbo].[headcount]([scotia_id]) ON DELETE CASCADE;
    PRINT 'Foreign Key FK_procesos_headcount creada exitosamente';
END
GO

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para headcount
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_headcount_unit_position' AND object_id = OBJECT_ID(N'[dbo].[headcount]'))
BEGIN
    CREATE INDEX IX_headcount_unit_position ON [dbo].[headcount] ([unit], [position]);
    PRINT 'Índice IX_headcount_unit_position creado exitosamente';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_headcount_activo' AND object_id = OBJECT_ID(N'[dbo].[headcount]'))
BEGIN
    CREATE INDEX IX_headcount_activo ON [dbo].[headcount] ([activo]);
    PRINT 'Índice IX_headcount_activo creado exitosamente';
END
GO

-- Índices para applications
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_unit_position' AND object_id = OBJECT_ID(N'[dbo].[applications]'))
BEGIN
    CREATE INDEX IX_applications_unit_position ON [dbo].[applications] ([unit], [position_role]);
    PRINT 'Índice IX_applications_unit_position creado exitosamente';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_applications_access_status' AND object_id = OBJECT_ID(N'[dbo].[applications]'))
BEGIN
    CREATE INDEX IX_applications_access_status ON [dbo].[applications] ([access_status]);
    PRINT 'Índice IX_applications_access_status creado exitosamente';
END
GO

-- Índices para historico
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_scotia_status' AND object_id = OBJECT_ID(N'[dbo].[historico]'))
BEGIN
    CREATE INDEX IX_historico_scotia_status ON [dbo].[historico] ([scotia_id], [status]);
    PRINT 'Índice IX_historico_scotia_status creado exitosamente';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_process_status' AND object_id = OBJECT_ID(N'[dbo].[historico]'))
BEGIN
    CREATE INDEX IX_historico_process_status ON [dbo].[historico] ([process_access], [status]);
    PRINT 'Índice IX_historico_process_status creado exitosamente';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_record_date' AND object_id = OBJECT_ID(N'[dbo].[historico]'))
BEGIN
    CREATE INDEX IX_historico_record_date ON [dbo].[historico] ([record_date]);
    PRINT 'Índice IX_historico_record_date creado exitosamente';
END
GO

-- =====================================================
-- VISTAS DEL SISTEMA
-- =====================================================

-- Vista para aplicaciones requeridas
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_required_apps')
BEGIN
    EXEC('CREATE VIEW [dbo].[vw_required_apps] AS
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
        WHERE access_status = ''Activo''
    ) a ON 
        UPPER(LTRIM(RTRIM(h.unit))) = UPPER(LTRIM(RTRIM(a.unit))) AND
        UPPER(LTRIM(RTRIM(h.position))) = UPPER(LTRIM(RTRIM(a.position_role)))
    WHERE h.activo = 1
    GROUP BY h.scotia_id, a.logical_access_name, h.unit, h.position, a.subunit, a.position_role, 
             a.role_name, a.system_owner, a.access_type, a.category, a.description');
    PRINT 'Vista vw_required_apps creada exitosamente';
END
GO

-- Vista para accesos actuales
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_current_access')
BEGIN
    EXEC('CREATE VIEW [dbo].[vw_current_access] AS
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
    WHERE h.status IN (''Completado'', ''Pendiente'', ''En Proceso'', ''Cancelado'', ''Rechazado'')
    AND h.process_access IN (''onboarding'', ''lateral_movement'')
    AND head.activo = 1
    AND h.app_access_name IS NOT NULL
    GROUP BY h.scotia_id, h.app_access_name, head.unit, head.position, h.area, h.record_date, h.status');
    PRINT 'Vista vw_current_access creada exitosamente';
END
GO

-- Vista para accesos por otorgar
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_to_grant')
BEGIN
    EXEC('CREATE VIEW [dbo].[vw_to_grant] AS
    SELECT 
        req.scotia_id,
        req.unit,
        req.position,
        req.logical_access_name,
        req.subunit,
        req.position_role,
        ''onboarding'' as process_type
    FROM [dbo].[vw_required_apps] req
    LEFT JOIN [dbo].[vw_current_access] curr ON 
        req.scotia_id = curr.scotia_id AND
        UPPER(LTRIM(RTRIM(req.logical_access_name))) = UPPER(LTRIM(RTRIM(curr.logical_access_name))) AND
        UPPER(LTRIM(RTRIM(req.unit))) = UPPER(LTRIM(RTRIM(curr.unit))) AND
        UPPER(LTRIM(RTRIM(req.position))) = UPPER(LTRIM(RTRIM(curr.position)))
    WHERE curr.scotia_id IS NULL');
    PRINT 'Vista vw_to_grant creada exitosamente';
END
GO

-- Vista para accesos por revocar
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_to_revoke')
BEGIN
    EXEC('CREATE VIEW [dbo].[vw_to_revoke] AS
    SELECT 
        curr.scotia_id,
        curr.unit,
        curr.position,
        curr.logical_access_name,
        curr.subunit,
        curr.position_role,
        curr.record_date,
        ''offboarding'' as process_type
    FROM [dbo].[vw_current_access] curr
    LEFT JOIN [dbo].[vw_required_apps] req ON 
        curr.scotia_id = req.scotia_id AND
        UPPER(LTRIM(RTRIM(curr.logical_access_name))) = UPPER(LTRIM(RTRIM(req.logical_access_name))) AND
        UPPER(LTRIM(RTRIM(curr.unit))) = UPPER(LTRIM(RTRIM(req.unit))) AND
        UPPER(LTRIM(RTRIM(curr.position))) = UPPER(LTRIM(RTRIM(req.position)))
    WHERE req.scotia_id IS NULL');
    PRINT 'Vista vw_to_revoke creada exitosamente';
END
GO

-- Vista para estadísticas del sistema
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_system_stats')
BEGIN
    EXEC('CREATE VIEW [dbo].[vw_system_stats] AS
    SELECT 
        (SELECT COUNT(*) FROM [dbo].[headcount] WHERE activo = 1) as empleados_activos,
        (SELECT COUNT(*) FROM [dbo].[applications] WHERE access_status = ''Activo'') as aplicaciones_activas,
        (SELECT COUNT(*) FROM [dbo].[historico]) as total_historico,
        (SELECT COUNT(*) FROM [dbo].[procesos]) as total_procesos,
        (SELECT COUNT(*) FROM [dbo].[headcount]) as total_empleados,
        (SELECT COUNT(*) FROM [dbo].[applications]) as total_aplicaciones');
    PRINT 'Vista vw_system_stats creada exitosamente';
END
GO

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- =====================================================

-- Procedimiento para obtener estadísticas de la base de datos
IF NOT EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_GetDatabaseStats')
BEGIN
    EXEC('CREATE PROCEDURE [dbo].[sp_GetDatabaseStats]
    AS
    BEGIN
        SELECT 
            ''headcount'' as tabla, COUNT(*) as registros FROM [dbo].[headcount]
        UNION ALL
        SELECT ''applications'' as tabla, COUNT(*) as registros FROM [dbo].[applications]
        UNION ALL
        SELECT ''historico'' as tabla, COUNT(*) as registros FROM [dbo].[historico]
        UNION ALL
        SELECT ''procesos'' as tabla, COUNT(*) as registros FROM [dbo].[procesos];
    END');
    PRINT 'Procedimiento sp_GetDatabaseStats creado exitosamente';
END
GO

-- Procedimiento para obtener historial de empleado
IF NOT EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_GetEmployeeHistory')
BEGIN
    EXEC('CREATE PROCEDURE [dbo].[sp_GetEmployeeHistory]
        @scotia_id VARCHAR(20)
    AS
    BEGIN
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
    END');
    PRINT 'Procedimiento sp_GetEmployeeHistory creado exitosamente';
END
GO

-- Procedimiento para obtener aplicaciones por posición
IF NOT EXISTS (SELECT * FROM sys.procedures WHERE name = 'sp_GetApplicationsByPosition')
BEGIN
    EXEC('CREATE PROCEDURE [dbo].[sp_GetApplicationsByPosition]
        @position VARCHAR(100) = NULL,
        @unit VARCHAR(100) = NULL,
        @subunit VARCHAR(100) = NULL
    AS
    BEGIN
        SELECT *
        FROM [dbo].[applications]
        WHERE access_status = ''Activo''
        AND (@position IS NULL OR position_role = @position)
        AND (@unit IS NULL OR unit = @unit)
        AND (@subunit IS NULL OR subunit = @subunit)
        ORDER BY unit, position_role, logical_access_name;
    END');
    PRINT 'Procedimiento sp_GetApplicationsByPosition creado exitosamente';
END
GO

-- =====================================================
-- FUNCIÓN ESCALAR
-- =====================================================

-- Función para normalizar texto
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_NormalizeText]') AND type in (N'FN'))
BEGIN
    EXEC('CREATE FUNCTION [dbo].[fn_NormalizeText](@text VARCHAR(MAX))
    RETURNS VARCHAR(MAX)
    AS
    BEGIN
        DECLARE @result VARCHAR(MAX);
        SET @result = UPPER(LTRIM(RTRIM(ISNULL(@text, '''''))));
        RETURN @result;
    END');
    PRINT 'Función fn_NormalizeText creada exitosamente';
END
GO

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

-- Insertar datos de ejemplo en headcount
IF NOT EXISTS (SELECT * FROM headcount WHERE scotia_id = 'EMP001')
BEGIN
    INSERT INTO [dbo].[headcount] (scotia_id, employee, full_name, email, position, manager, senior_manager, unit, start_date, ceco, skip_level, cafe_alcides, parents, personal_email, size, birthday, validacion, activo, inactivation_date)
    VALUES 
        ('EMP001', 'Juan Pérez', 'Juan Carlos Pérez García', 'juan.perez@empresa.com', 'Analista', 'María González', 'Carlos López', 'Tecnología', '2023-01-15', 'CECO001', 'Nivel 1', 'Café 1', 'Padres', 'juan.personal@gmail.com', 'M', '1985-05-20', 'Validado', 1, NULL),
        ('EMP002', 'María González', 'María Elena González López', 'maria.gonzalez@empresa.com', 'Analista Senior', 'Carlos López', 'Ana Martínez', 'Tecnología', '2022-03-10', 'CECO002', 'Nivel 2', 'Café 2', 'Padres', 'maria.personal@gmail.com', 'L', '1980-08-15', 'Validado', 1, NULL),
        ('EMP003', 'Carlos López', 'Carlos Alberto López Martínez', 'carlos.lopez@empresa.com', 'Gerente', 'Ana Martínez', 'Director', 'Tecnología', '2021-06-01', 'CECO003', 'Nivel 3', 'Café 3', 'Padres', 'carlos.personal@gmail.com', 'XL', '1975-12-03', 'Validado', 1, NULL);
    PRINT 'Datos de ejemplo insertados en headcount';
END
GO

-- Insertar datos de ejemplo en applications
IF NOT EXISTS (SELECT * FROM applications WHERE logical_access_name = 'Sistema de Gestión')
BEGIN
    INSERT INTO [dbo].[applications] (jurisdiction, unit, subunit, logical_access_name, alias, path_email_url, position_role, exception_tracking, fulfillment_action, system_owner, role_name, access_type, category, additional_data, ad_code, access_status, last_update_date, require_licensing, description, authentication_method)
    VALUES 
        -- TECNOLOGÍA - ANALISTA
        ('Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'SIS-GEST', 'https://sistema.empresa.com', 'Analista', 'TRK001', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD001', 'Activo', GETDATE(), 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'GitLab', 'GIT-REPO', 'https://gitlab.empresa.com', 'Analista', 'TRK002', 'Crear usuario', 'Admin GitLab', 'Developer', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD002', 'Activo', GETDATE(), 'Licencia estándar', 'Repositorio de código fuente', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'Jira', 'JIRA-PROJ', 'https://jira.empresa.com', 'Analista', 'TRK003', 'Asignar acceso', 'Admin Jira', 'Developer', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD003', 'Activo', GETDATE(), 'Licencia estándar', 'Gestión de proyectos y tickets', 'LDAP'),
        
        -- TECNOLOGÍA - ANALISTA SENIOR
        ('Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'SIS-GEST-ADM', 'https://sistema.empresa.com', 'Analista Senior', 'TRK004', 'Crear usuario', 'Admin Sistema', 'Administrador', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD004', 'Activo', GETDATE(), 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'GitLab', 'GIT-REPO-ADM', 'https://gitlab.empresa.com', 'Analista Senior', 'TRK005', 'Crear usuario', 'Admin GitLab', 'Maintainer', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD005', 'Activo', GETDATE(), 'Licencia premium', 'Repositorio de código fuente', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'Jira', 'JIRA-PROJ-ADM', 'https://jira.empresa.com', 'Analista Senior', 'TRK006', 'Asignar acceso', 'Admin Jira', 'Project Lead', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD006', 'Activo', GETDATE(), 'Licencia premium', 'Gestión de proyectos y tickets', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'Docker Registry', 'DOCK-REG', 'https://registry.empresa.com', 'Analista Senior', 'TRK007', 'Crear usuario', 'Admin Docker', 'Maintainer', 'Aplicación', 'DevOps', 'Datos adicionales', 'AD007', 'Activo', GETDATE(), 'Licencia premium', 'Registro de contenedores Docker', 'LDAP'),
        
        -- TECNOLOGÍA - GERENTE
        ('Global', 'Tecnología', 'Desarrollo', 'Sistema de Gestión', 'SIS-GEST-MGR', 'https://sistema.empresa.com', 'Gerente', 'TRK008', 'Crear usuario', 'Admin Sistema', 'Manager', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD008', 'Activo', GETDATE(), 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'GitLab', 'GIT-REPO-MGR', 'https://gitlab.empresa.com', 'Gerente', 'TRK009', 'Crear usuario', 'Admin GitLab', 'Owner', 'Aplicación', 'Desarrollo', 'Datos adicionales', 'AD009', 'Activo', GETDATE(), 'Licencia premium', 'Repositorio de código fuente', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'Jira', 'JIRA-PROJ-MGR', 'https://jira.empresa.com', 'Gerente', 'TRK010', 'Asignar acceso', 'Admin Jira', 'Administrator', 'Aplicación', 'Gestión', 'Datos adicionales', 'AD010', 'Activo', GETDATE(), 'Licencia premium', 'Gestión de proyectos y tickets', 'LDAP'),
        ('Global', 'Tecnología', 'Desarrollo', 'Power BI', 'POWER-BI', 'https://powerbi.empresa.com', 'Gerente', 'TRK011', 'Crear usuario', 'Admin PowerBI', 'Admin', 'Aplicación', 'Analytics', 'Datos adicionales', 'AD011', 'Activo', GETDATE(), 'Licencia premium', 'Herramienta de análisis de datos', 'LDAP'),
        
        -- RECURSOS HUMANOS - ANALISTA
        ('Global', 'Recursos Humanos', 'RRHH', 'Sistema de Gestión', 'SIS-GEST-RRHH', 'https://sistema.empresa.com', 'Analista', 'TRK015', 'Crear usuario', 'Admin Sistema', 'Usuario', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD015', 'Activo', GETDATE(), 'Licencia estándar', 'Sistema principal de gestión empresarial', 'LDAP'),
        ('Global', 'Recursos Humanos', 'RRHH', 'Workday', 'WD-RRHH', 'https://workday.empresa.com', 'Analista', 'TRK016', 'Crear usuario', 'Admin Workday', 'Analyst', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD016', 'Activo', GETDATE(), 'Licencia estándar', 'Sistema de gestión de RRHH', 'LDAP'),
        ('Global', 'Recursos Humanos', 'RRHH', 'SuccessFactors', 'SF-RRHH', 'https://successfactors.empresa.com', 'Analista', 'TRK017', 'Crear usuario', 'Admin SuccessFactors', 'Analyst', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD017', 'Activo', GETDATE(), 'Licencia estándar', 'Gestión de talento y rendimiento', 'LDAP'),
        
        -- RECURSOS HUMANOS - GERENTE
        ('Global', 'Recursos Humanos', 'RRHH', 'Sistema de Gestión', 'SIS-GEST-RRHH-MGR', 'https://sistema.empresa.com', 'Gerente', 'TRK018', 'Crear usuario', 'Admin Sistema', 'Manager', 'Aplicación', 'Sistemas', 'Datos adicionales', 'AD018', 'Activo', GETDATE(), 'Licencia premium', 'Sistema principal de gestión empresarial', 'LDAP'),
        ('Global', 'Recursos Humanos', 'RRHH', 'Workday', 'WD-RRHH-MGR', 'https://workday.empresa.com', 'Gerente', 'TRK019', 'Crear usuario', 'Admin Workday', 'Manager', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD019', 'Activo', GETDATE(), 'Licencia premium', 'Sistema de gestión de RRHH', 'LDAP'),
        ('Global', 'Recursos Humanos', 'RRHH', 'SuccessFactors', 'SF-RRHH-MGR', 'https://successfactors.empresa.com', 'Gerente', 'TRK020', 'Crear usuario', 'Admin SuccessFactors', 'Manager', 'Aplicación', 'RRHH', 'Datos adicionales', 'AD020', 'Activo', GETDATE(), 'Licencia premium', 'Gestión de talento y rendimiento', 'LDAP');
    PRINT 'Datos de ejemplo insertados en applications';
END
GO

-- Insertar datos de ejemplo en historico
IF NOT EXISTS (SELECT * FROM historico WHERE scotia_id = 'EMP001')
BEGIN
    INSERT INTO [dbo].[historico] (scotia_id, case_id, responsible, record_date, request_date, process_access, sid, area, subunit, event_description, ticket_email, app_access_name, computer_system_type, status, closing_date_app, closing_date_ticket, app_quality, confirmation_by_user, comment, ticket_quality, general_status, average_time_open_ticket)
    VALUES 
        ('EMP001', 'CASE-20240115-001', 'Admin Sistema', GETDATE(), '2024-01-14', 'onboarding', 'EMP001', 'Tecnología', 'Desarrollo', 'Usuario creado en sistema', 'admin@empresa.com', 'Sistema de Gestión', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', 1, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:30:00'),
        ('EMP002', 'CASE-20240115-002', 'Admin Portal', GETDATE(), '2024-01-14', 'onboarding', 'EMP002', 'Tecnología', 'Desarrollo', 'Usuario creado en portal', 'admin@empresa.com', 'GitLab', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', 1, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:45:00'),
        ('EMP003', 'CASE-20240115-003', 'Admin Sistema', GETDATE(), '2024-01-14', 'onboarding', 'EMP003', 'Tecnología', 'Desarrollo', 'Usuario creado en sistema', 'admin@empresa.com', 'Jira', 'Desktop', 'Completado', '2024-01-15', '2024-01-15', 'Excelente', 1, 'Usuario creado exitosamente', 'Excelente', 'Completado', '00:20:00');
    PRINT 'Datos de ejemplo insertados en historico';
END
GO

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
