# Configuración de SQL Server para GAMLO - Sistema de Gestión de Empleados

Este documento explica cómo configurar el sistema para usar SQL Server en lugar de SQLite.

## 📋 Requisitos Previos

### Software Necesario
1. **SQL Server 2019 o superior** (Express, Standard, o Enterprise)
2. **SQL Server Management Studio (SSMS)** para administración
3. **Python 3.8+** con las siguientes librerías:
   ```bash
   pip install pyodbc
   pip install pandas  # Opcional, para migración de datos
   ```

### Drivers ODBC
- **ODBC Driver 17 for SQL Server** (recomendado)
- **ODBC Driver 13 for SQL Server** (alternativo)

## 🚀 Instalación Paso a Paso

### 1. Preparar SQL Server

1. **Instalar SQL Server** con las siguientes características:
   - Database Engine Services
   - SQL Server Management Tools
   - SQL Server Books Online

2. **Configurar autenticación**:
   - Habilitar autenticación mixta (Windows + SQL Server)
   - Crear usuario `sa` con contraseña segura
   - O configurar autenticación de Windows

3. **Habilitar TCP/IP**:
   - Abrir SQL Server Configuration Manager
   - Habilitar TCP/IP en SQL Server Network Configuration
   - Configurar puerto 1433 (por defecto)

### 2. Ejecutar Script de Configuración

1. **Abrir SQL Server Management Studio**
2. **Conectar al servidor** con credenciales de administrador
3. **Ejecutar el script** `sql_server_setup.sql`:
   ```sql
   -- El script creará:
   -- - Base de datos GAMLO_Empleados
   -- - 4 tablas principales
   -- - 5 vistas para consultas
   -- - 3 procedimientos almacenados
   -- - 1 función de utilidad
   -- - Índices para optimización
   -- - Datos de ejemplo
   ```

### 3. Configurar Conexión desde Python

1. **Editar configuración** en `sql_server_connection_config.py`:
   ```python
   SQL_SERVER_CONFIG = {
       'server': 'localhost',  # Tu servidor SQL Server
       'database': 'GAMLO_Empleados',
       'username': 'sa',  # Tu usuario
       'password': 'TuPassword123!',  # Tu contraseña
       'driver': '{ODBC Driver 17 for SQL Server}',
       'trusted_connection': 'no',  # 'yes' para Windows Auth
       'timeout': 30
   }
   ```

2. **Probar conexión**:
   ```bash
   python sql_server_connection_config.py
   ```

### 4. Migrar Datos Existentes (Opcional)

Si tienes datos en SQLite y quieres migrarlos:

```bash
python sql_server_connection_config.py --migrate
```

Esto migrará automáticamente:
- Tabla `headcount`
- Tabla `applications` 
- Tabla `historico`
- Tabla `procesos`

## 📊 Estructura de la Base de Datos

### Tablas Principales

#### 1. `headcount` - Empleados
```sql
- scotia_id (PK) - ID único del empleado
- employee - Nombre de usuario
- full_name - Nombre completo
- email - Correo electrónico
- position - Cargo/Posición
- unit - Unidad/Departamento
- activo - Estado activo/inactivo
- [otros campos...]
```

#### 2. `applications` - Aplicaciones
```sql
- id (PK) - ID autoincremental
- logical_access_name - Nombre lógico del acceso
- unit - Unidad que usa la aplicación
- position_role - Rol de posición requerido
- access_status - Estado del acceso
- [otros campos...]
```

#### 3. `historico` - Historial de Procesos
```sql
- id (PK) - ID autoincremental
- scotia_id (FK) - Referencia a headcount
- process_access - Tipo de proceso
- app_access_name (FK) - Referencia a applications
- status - Estado del proceso
- [otros campos...]
```

#### 4. `procesos` - Gestión de Procesos
```sql
- id (PK) - ID autoincremental
- sid (FK) - Referencia a headcount
- tipo_proceso - Tipo de proceso
- status - Estado del proceso
- [otros campos...]
```

### Vistas del Sistema

#### 1. `vw_required_apps` - Aplicaciones Requeridas
Muestra qué aplicaciones debe tener cada empleado según su posición.

#### 2. `vw_current_access` - Accesos Actuales
Muestra los accesos que tiene actualmente cada empleado.

#### 3. `vw_to_grant` - Accesos por Otorgar
Identifica accesos que faltan y deben ser otorgados.

#### 4. `vw_to_revoke` - Accesos por Revocar
Identifica accesos excesivos que deben ser revocados.

#### 5. `vw_system_stats` - Estadísticas del Sistema
Proporciona estadísticas generales del sistema.

### Procedimientos Almacenados

#### 1. `sp_GetDatabaseStats`
```sql
EXEC sp_GetDatabaseStats
```
Retorna estadísticas de todas las tablas.

#### 2. `sp_GetEmployeeHistory`
```sql
EXEC sp_GetEmployeeHistory @scotia_id = 'EMP001'
```
Obtiene el historial completo de un empleado.

#### 3. `sp_GetApplicationsByPosition`
```sql
EXEC sp_GetApplicationsByPosition 
    @position = 'Desarrollador', 
    @unit = 'Tecnología',
    @subunit = 'Desarrollo'
```
Obtiene aplicaciones requeridas para una posición específica.

## 🔧 Configuración Avanzada

### Configuración de Seguridad

1. **Crear usuario específico** para la aplicación:
   ```sql
   CREATE LOGIN gamlo_app WITH PASSWORD = 'PasswordSeguro123!';
   USE GAMLO_Empleados;
   CREATE USER gamlo_app FOR LOGIN gamlo_app;
   GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO gamlo_app;
   ```

2. **Configurar firewall** para permitir conexiones:
   - Puerto 1433 (TCP)
   - Puerto 1434 (UDP) para SQL Browser

### Optimización de Rendimiento

1. **Configurar índices adicionales** según necesidades:
   ```sql
   CREATE INDEX IX_historico_scotia_id_date 
   ON historico (scotia_id, record_date);
   ```

2. **Configurar estadísticas automáticas**:
   ```sql
   ALTER DATABASE GAMLO_Empleados 
   SET AUTO_CREATE_STATISTICS ON;
   ```

### Backup y Mantenimiento

1. **Configurar backup automático**:
   ```sql
   -- Crear job de backup diario
   EXEC dbo.sp_add_job @job_name = 'GAMLO_Backup_Daily';
   ```

2. **Configurar mantenimiento de índices**:
   ```sql
   -- Reorganizar índices semanalmente
   ALTER INDEX ALL ON headcount REORGANIZE;
   ```

## 🐛 Solución de Problemas

### Error de Conexión
```
Error: [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Login failed
```
**Solución**: Verificar credenciales y configuración de autenticación.

### Error de Driver
```
Error: [Microsoft][ODBC Driver Manager] Data source name not found
```
**Solución**: Instalar ODBC Driver 17 for SQL Server.

### Error de Permisos
```
Error: The SELECT permission was denied on the object
```
**Solución**: Otorgar permisos necesarios al usuario de la aplicación.

### Error de Timeout
```
Error: [Microsoft][ODBC Driver 17 for SQL Server]Timeout expired
```
**Solución**: Aumentar el valor de timeout en la configuración.

## 📈 Monitoreo y Mantenimiento

### Consultas Útiles para Monitoreo

1. **Verificar conexiones activas**:
   ```sql
   SELECT 
       session_id,
       login_name,
       host_name,
       program_name,
       login_time
   FROM sys.dm_exec_sessions
   WHERE database_id = DB_ID('GAMLO_Empleados');
   ```

2. **Verificar uso de espacio**:
   ```sql
   SELECT 
       name,
       size * 8 / 1024 as size_mb,
       max_size * 8 / 1024 as max_size_mb
   FROM sys.database_files;
   ```

3. **Verificar estadísticas de tablas**:
   ```sql
   EXEC sp_GetDatabaseStats;
   ```

## 🔄 Migración desde SQLite

Si ya tienes datos en SQLite:

1. **Hacer backup** de la base de datos SQLite
2. **Ejecutar script de migración**:
   ```bash
   python sql_server_connection_config.py --migrate
   ```
3. **Verificar datos migrados** en SQL Server Management Studio
4. **Actualizar configuración** de la aplicación

## 📞 Soporte

Para problemas específicos:

1. **Verificar logs** de SQL Server
2. **Revisar configuración** de red y firewall
3. **Consultar documentación** de Microsoft SQL Server
4. **Verificar permisos** de usuario y base de datos

## ✅ Verificación Final

Para verificar que todo funciona correctamente:

1. **Ejecutar script de prueba**:
   ```bash
   python sql_server_connection_config.py
   ```

2. **Verificar vistas** en SSMS:
   ```sql
   SELECT * FROM vw_system_stats;
   ```

3. **Probar procedimientos**:
   ```sql
   EXEC sp_GetDatabaseStats;
   ```

4. **Ejecutar aplicación** y verificar funcionalidad completa.

---

**¡Configuración completada!** El sistema ahora está listo para usar SQL Server como base de datos.
