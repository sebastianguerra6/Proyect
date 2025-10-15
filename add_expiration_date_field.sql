-- Script para agregar el campo expiration_date a la tabla historico
-- Este campo es necesario para los accesos flex staff temporales

USE GAMLO_Empleados;
GO

-- Verificar si el campo ya existe
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[historico]') AND name = 'expiration_date')
BEGIN
    -- Agregar el campo expiration_date
    ALTER TABLE [dbo].[historico]
    ADD [expiration_date] DATETIME2 NULL;
    
    PRINT 'Campo expiration_date agregado exitosamente a la tabla historico';
END
ELSE
BEGIN
    PRINT 'Campo expiration_date ya existe en la tabla historico';
END
GO

-- Crear índice para optimizar consultas por fecha de expiración
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_historico_expiration_date' AND object_id = OBJECT_ID(N'[dbo].[historico]'))
BEGIN
    CREATE INDEX IX_historico_expiration_date ON [dbo].[historico] ([expiration_date]);
    PRINT 'Índice IX_historico_expiration_date creado exitosamente';
END
ELSE
BEGIN
    PRINT 'Índice IX_historico_expiration_date ya existe';
END
GO

-- Verificar la estructura actualizada de la tabla
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'historico' 
AND TABLE_SCHEMA = 'dbo'
ORDER BY ORDINAL_POSITION;

PRINT 'Script completado exitosamente';
