# Guía de Importación de Excel a Bases de Datos

Este documento explica cómo usar las clases `ExcelToSQLiteImporter` y `ExcelToSQLServerImporter` para importar datos desde archivos Excel a las bases de datos.

## 📋 Requisitos

### Dependencias Python
```bash
pip install pandas openpyxl pyodbc
```

### Para SQL Server
- **ODBC Driver 17 for SQL Server** instalado
- Acceso a una instancia de SQL Server
- Permisos para crear tablas e insertar datos

## 🗂️ Estructura de Archivos Excel

Los archivos Excel deben tener las siguientes hojas y columnas:

### 1. Empleados (hoja: `headcount`)
| Columna | Tipo | Descripción |
|---------|------|-------------|
| scotia_id | Texto | ID único del empleado |
| employee | Texto | Nombre del empleado |
| full_name | Texto | Nombre completo |
| email | Texto | Email corporativo |
| position | Texto | Posición/cargo |
| manager | Texto | Manager directo |
| senior_manager | Texto | Manager senior |
| unit | Texto | Unidad/área |
| start_date | Fecha | Fecha de inicio |
| coca | Texto | COCA |
| skip_level | Texto | Skip level |
| coleadores | Texto | Coleadores |
| parents | Texto | Parents |
| personal_email | Texto | Email personal |
| size | Texto | Tamaño |
| birthday | Fecha | Cumpleaños |
| ubicacion | Texto | Ubicación |
| activo | Booleano | Estado activo |

### 2. Aplicaciones (hoja: `applications`)
| Columna | Tipo | Descripción |
|---------|------|-------------|
| jurisdiction | Texto | Jurisdicción |
| unit | Texto | Unidad |
| subunit | Texto | Sub unidad |
| logical_access_name | Texto | Nombre lógico de acceso |
| alias | Texto | Alias |
| path_email_url | Texto | Path/Email/URL |
| position_role | Texto | Rol de posición |
| exception_tracking | Texto | Seguimiento de excepciones |
| fulfillment_action | Texto | Acción de cumplimiento |
| system_owner | Texto | Propietario del sistema |
| role_name | Texto | Nombre del rol |
| access_type | Texto | Tipo de acceso |
| category | Texto | Categoría |
| additional_data | Texto | Datos adicionales |
| ad_code | Texto | Código AD |
| access_status | Texto | Estado de acceso |
| last_update_date | Fecha | Fecha de última actualización |
| requirement_licensing | Texto | Requisito de licencia |
| description | Texto | Descripción |
| authentication_method | Texto | Método de autenticación |

### 3. Histórico (hoja: `historico`)
| Columna | Tipo | Descripción |
|---------|------|-------------|
| scotia_id | Texto | ID del empleado |
| case_id | Texto | ID del caso |
| responsible | Texto | Responsable |
| record_date | Fecha/Hora | Fecha de registro |
| request_date | Fecha | Fecha de solicitud |
| process_access | Texto | Proceso de acceso |
| sid | Texto | SID |
| area | Texto | Área |
| subunit | Texto | Sub unidad |
| event_description | Texto | Descripción del evento |
| ticket_email | Texto | Email del ticket |
| app_access_name | Texto | Nombre de la aplicación |
| computer_system_type | Texto | Tipo de sistema |
| status | Texto | Estado |
| closing_date_app | Fecha | Fecha de cierre app |
| closing_date_ticket | Fecha | Fecha de cierre ticket |
| app_quality | Texto | Calidad de app |
| confirmation_by_user | Booleano | Confirmación por usuario |
| comment | Texto | Comentario |
| ticket_quality | Texto | Calidad del ticket |
| general_status | Texto | Estado general |
| average_time_open_ticket | Texto | Tiempo promedio de apertura |

## 🚀 Uso Básico

### Importación a SQLite

```python
from services.excel_importer import ExcelToSQLiteImporter

# Crear importador
importer = ExcelToSQLiteImporter("database/empleados.db")

# Importar empleados
success, message, count = importer.import_from_excel(
    excel_path="data/empleados.xlsx",
    sheet_name="headcount",
    table_name="headcount",
    skip_rows=1  # Saltar encabezados
)

print(f"Resultado: {success}")
print(f"Mensaje: {message}")
print(f"Registros importados: {count}")

# Cerrar conexión
importer.close()
```

### Importación a SQL Server

```python
from services.excel_importer import ExcelToSQLServerImporter

# Crear importador
importer = ExcelToSQLServerImporter(
    server="localhost\\SQLEXPRESS",
    database="EmpleadosDB",
    username="sa",
    password="tu_password",
    trusted_connection=False
)

# Crear tablas si no existen
success, message = importer.create_tables()
print(f"Tablas creadas: {success} - {message}")

# Importar datos
success, message, count = importer.import_from_excel(
    excel_path="data/empleados.xlsx",
    sheet_name="headcount",
    table_name="headcount",
    skip_rows=1
)

print(f"Importación: {success} - {message} - {count} registros")

# Cerrar conexión
importer.close()
```

## 🔧 Funciones de Conveniencia

### SQLite
```python
from services.excel_importer import import_excel_to_sqlite

success, message, count = import_excel_to_sqlite(
    excel_path="data/empleados.xlsx",
    sheet_name="headcount",
    table_name="headcount",
    db_path="database/empleados.db",
    skip_rows=1
)
```

### SQL Server
```python
from services.excel_importer import import_excel_to_sqlserver

success, message, count = import_excel_to_sqlserver(
    excel_path="data/empleados.xlsx",
    sheet_name="headcount",
    table_name="headcount",
    server="localhost\\SQLEXPRESS",
    database="EmpleadosDB",
    username="sa",
    password="tu_password",
    trusted_connection=False,
    skip_rows=1
)
```

## ⚙️ Configuración de SQL Server

### Conexión con Usuario/Contraseña
```python
importer = ExcelToSQLServerImporter(
    server="tu_servidor",
    database="tu_base_datos",
    username="tu_usuario",
    password="tu_contraseña",
    trusted_connection=False
)
```

### Conexión con Windows Authentication
```python
importer = ExcelToSQLServerImporter(
    server="tu_servidor",
    database="tu_base_datos",
    trusted_connection=True
)
```

## 📝 Notas Importantes

1. **Formato de Fechas**: Las fechas en Excel deben estar en formato estándar (YYYY-MM-DD)
2. **Valores Nulos**: Las celdas vacías se convierten en strings vacíos
3. **Duplicados**: 
   - SQLite: Usa `INSERT OR REPLACE` para headcount
   - SQL Server: Usa `MERGE` para headcount, `INSERT` para otras tablas
4. **Encoding**: Los archivos Excel deben estar en UTF-8
5. **Hojas**: Los nombres de las hojas deben coincidir exactamente

## 🐛 Solución de Problemas

### Error de Conexión SQL Server
- Verificar que el servidor esté ejecutándose
- Comprobar credenciales
- Instalar ODBC Driver 17 for SQL Server

### Error de Archivo Excel
- Verificar que el archivo existe
- Comprobar que la hoja existe
- Verificar formato de columnas

### Error de Datos
- Revisar tipos de datos en Excel
- Verificar que las columnas requeridas no estén vacías
- Comprobar formato de fechas

## 📊 Ejemplo Completo

```python
#!/usr/bin/env python3
import sys
sys.path.append('services')
from excel_importer import import_excel_to_sqlite, import_excel_to_sqlserver

def import_all_data():
    """Importa todos los datos desde Excel"""
    
    # Importar a SQLite
    print("Importando a SQLite...")
    
    # Empleados
    success, message, count = import_excel_to_sqlite(
        "data/empleados.xlsx", "headcount", "headcount", skip_rows=1
    )
    print(f"Empleados SQLite: {count} registros")
    
    # Aplicaciones
    success, message, count = import_excel_to_sqlite(
        "data/aplicaciones.xlsx", "applications", "applications", skip_rows=1
    )
    print(f"Aplicaciones SQLite: {count} registros")
    
    # Histórico
    success, message, count = import_excel_to_sqlite(
        "data/historico.xlsx", "historico", "historico", skip_rows=1
    )
    print(f"Histórico SQLite: {count} registros")
    
    # Importar a SQL Server
    print("\nImportando a SQL Server...")
    
    try:
        # Empleados
        success, message, count = import_excel_to_sqlserver(
            "data/empleados.xlsx", "headcount", "headcount",
            server="localhost\\SQLEXPRESS",
            database="EmpleadosDB",
            trusted_connection=True,
            skip_rows=1
        )
        print(f"Empleados SQL Server: {count} registros")
        
    except Exception as e:
        print(f"Error SQL Server: {e}")

if __name__ == "__main__":
    import_all_data()
```
