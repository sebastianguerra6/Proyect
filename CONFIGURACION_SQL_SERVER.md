# Configuración para SQL Server

## 📋 Pasos para Configurar SQL Server

### 1. Instalar SQL Server
- Instalar SQL Server 2019 o superior
- Habilitar autenticación mixta (Windows + SQL Server)
- Crear usuario `sa` con contraseña segura

### 2. Instalar Driver ODBC
- Instalar "ODBC Driver 17 for SQL Server"
- Verificar que esté disponible en el sistema

### 3. Ejecutar Script de Base de Datos
```sql
-- Ejecutar el archivo sql_server_setup.sql en SQL Server Management Studio
-- Esto creará la base de datos GAMLO_Empleados con todas las tablas y vistas
```

### 4. Configurar la Aplicación
Editar el archivo `config.py`:

```python
# Cambiar a True para usar SQL Server
USE_SQL_SERVER = True

# Configurar conexión
SQL_SERVER_CONFIG = {
    'server': 'localhost',  # Tu servidor SQL Server
    'database': 'GAMLO_Empleados',
    'username': 'sa',  # Tu usuario
    'password': 'TuPassword123!',  # Tu contraseña
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'no',
    'timeout': 30
}
```

### 5. Instalar Dependencias Python
```bash
pip install pyodbc
```

### 6. Probar la Configuración
```bash
python test_sql_server_config.py
```

## 🔄 Cambiar entre SQLite y SQL Server

### Para usar SQLite:
```python
# En config.py
USE_SQL_SERVER = False
```

### Para usar SQL Server:
```python
# En config.py
USE_SQL_SERVER = True
```

## 🚀 Ejecutar la Aplicación
```bash
python app_empleados_refactorizada.py
```

## 📊 Verificar Funcionamiento

1. **Conexión**: La aplicación debe conectarse sin errores
2. **Datos**: Debe mostrar empleados y aplicaciones existentes
3. **Funcionalidad**: Todas las operaciones deben funcionar normalmente

## 🔧 Solución de Problemas

### Error de Conexión
- Verificar que SQL Server esté ejecutándose
- Verificar credenciales en `config.py`
- Verificar que el puerto 1433 esté abierto

### Error de Driver
- Instalar "ODBC Driver 17 for SQL Server"
- Verificar que el driver esté en la lista de drivers ODBC

### Error de Permisos
- Verificar que el usuario tenga permisos en la base de datos
- Ejecutar el script de permisos en SQL Server

## ✅ Verificación Final

La aplicación debe funcionar exactamente igual que con SQLite, pero usando SQL Server como base de datos.
