# GAMLO - Sistema Integrado de Gestión de Empleados

## 📋 Descripción General

Sistema de escritorio desarrollado en Python con Tkinter para la gestión integral de empleados, incluyendo procesos de onboarding, offboarding, movimientos laterales y conciliación de accesos. **Soporta tanto SQLite como SQL Server** con configuración flexible.

## 🚀 Características Principales

### 🎨 **Interfaz Moderna**
- **Navegación lateral**: Botones grandes con iconos descriptivos
- **Estilos personalizados**: Sistema de estilos consistente y moderno
- **Ventana ampliada**: Tamaño 1600x800 para mejor aprovechamiento del espacio
- **Logo GAMLO**: Posicionado en la esquina inferior izquierda

### 🔧 **Funcionalidades Core**
- **Gestión de Procesos**: Onboarding, offboarding y movimientos laterales
- **Edición y Búsqueda**: Herramientas avanzadas para modificar y consultar registros
- **Creación de Personas**: Formulario para agregar nuevos empleados
- **Filtrado Avanzado**: Sistema de filtrado en tiempo real con selección de columna
- **Conciliación de Accesos**: Sistema completo para gestionar permisos de usuarios

### 🗄️ **Soporte Dual de Base de Datos**
- **SQLite**: Por defecto, ideal para desarrollo y pruebas
- **SQL Server**: Para entornos empresariales y producción
- **Configuración flexible**: Cambio fácil entre bases de datos
- **Migración automática**: Herramientas para migrar datos entre sistemas

## 🆕 Sistema de Conciliación de Accesos

### **Características del Sistema**
- **Conciliación por SID**: Analiza accesos actuales vs. autorizados para un usuario específico
- **Conciliación Masiva**: Procesa todos los usuarios del sistema
- **Exportación a Excel**: Genera reportes con hojas de resumen y tickets
- **Registro de Tickets**: Crea tickets automáticos para accesos a otorgar/revocar
- **Historial Completo**: Seguimiento de todos los cambios de accesos

### **Funcionalidades Implementadas**
- ✅ **Conciliar Accesos**: Por SID específico
- ✅ **Exportar Excel**: Con formato profesional y múltiples hojas
- ✅ **Registrar Tickets**: Inserta en histórico lo calculado
- ✅ **Conciliar Todos**: Procesamiento masivo del sistema
- ✅ **Base de Datos Dual**: SQLite y SQL Server

## 🗂️ Estructura del Proyecto

```
Pruebas-Tranbajo/
├── app_empleados_refactorizada.py    # Aplicación principal
├── config.py                         # Configuración del sistema
├── cambiar_base_datos.py             # Herramienta de configuración
├── requirements.txt                  # Dependencias
├── README_UNIFICADO.md              # Este archivo
├── database/
│   ├── empleados.db                 # Base de datos SQLite
│   └── database_manager.py          # Gestor de base de datos
├── services/
│   ├── access_management_service.py # Servicio de gestión de accesos
│   ├── excel_importer.py           # Importador de Excel
│   ├── export_service.py           # Servicio de exportación
│   ├── history_service.py          # Servicio de historial
│   └── search_service.py           # Servicio de búsqueda
├── ui/
│   ├── components.py                # Componentes de interfaz
│   ├── manual_access_component.py  # Componente de registro manual
│   └── styles.py                   # Estilos personalizados
├── sql_server_setup_corregido.sql   # Script de SQL Server
├── sql_server_connection_config.py  # Configuración SQL Server
└── output/                          # Archivos Excel generados
```

## 🚀 Instalación y Configuración

### **1. Instalación de Dependencias**
```bash
pip install -r requirements.txt
```

### **2. Configuración de Base de Datos**

#### **Opción A: SQLite (Por Defecto)**
```bash
# No requiere configuración adicional
python app_empleados_refactorizada.py
```

#### **Opción B: SQL Server**
```bash
# 1. Configurar SQL Server
python cambiar_base_datos.py
# Seleccionar opción 2

# 2. Ejecutar script de base de datos
# Abrir SQL Server Management Studio
# Ejecutar: sql_server_setup_corregido.sql

# 3. Ejecutar aplicación
python app_empleados_refactorizada.py
```

### **3. Verificación de Configuración**
```bash
# Probar configuración actual
python test_sql_server_config.py
```

## 🔧 Configuración Avanzada

### **Configuración de SQL Server**

Editar `config.py`:
```python
# Cambiar a True para usar SQL Server
USE_SQL_SERVER = True

# Configuración de SQL Server
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

### **Requisitos para SQL Server**
- **SQL Server 2016+** (Express, Standard, o Enterprise)
- **ODBC Driver 17 for SQL Server**
- **SQL Server Management Studio** (recomendado)
- **Puerto 1433** abierto

## 📊 Estructura de Base de Datos

### **Tablas Principales**

#### **1. headcount** - Empleados
```sql
- scotia_id (PK) - ID único del empleado
- employee - Nombre de usuario
- full_name - Nombre completo
- email - Correo electrónico
- position - Cargo/Posición
- unit - Unidad/Departamento
- activo - Estado activo/inactivo
```

#### **2. applications** - Aplicaciones
```sql
- id (PK) - ID autoincremental
- logical_access_name - Nombre lógico del acceso
- unit - Unidad que usa la aplicación
- position_role - Rol de posición requerido
- access_status - Estado del acceso
```

#### **3. historico** - Historial de Procesos
```sql
- id (PK) - ID autoincremental
- scotia_id (FK) - Referencia a headcount
- process_access - Tipo de proceso
- app_access_name - Nombre de la aplicación
- status - Estado del proceso
```

#### **4. procesos** - Gestión de Procesos
```sql
- id (PK) - ID autoincremental
- sid (FK) - Referencia a headcount
- tipo_proceso - Tipo de proceso
- status - Estado del proceso
```

### **Vistas del Sistema**
- **vw_required_apps**: Aplicaciones requeridas por empleado
- **vw_current_access**: Accesos actuales de cada empleado
- **vw_to_grant**: Accesos que faltan y deben ser otorgados
- **vw_to_revoke**: Accesos excesivos que deben ser revocados
- **vw_system_stats**: Estadísticas generales del sistema

## 🎯 Uso del Sistema

### **1. Gestión de Empleados**
- **Crear empleado**: Formulario de creación con validaciones
- **Editar empleado**: Modificar datos existentes
- **Buscar empleado**: Filtrado avanzado por múltiples criterios

### **2. Procesos de Acceso**
- **Onboarding**: Otorgar accesos para nueva posición
- **Offboarding**: Revocar accesos al salir de posición
- **Lateral Movement**: Movimiento aditivo (mantiene accesos actuales + agrega nuevos)

### **3. Conciliación de Accesos**
- **Conciliar por SID**: Analizar accesos de un empleado específico
- **Conciliar todos**: Procesamiento masivo del sistema
- **Exportar Excel**: Generar reportes detallados
- **Registrar tickets**: Crear tickets automáticos

### **4. Búsqueda y Filtrado**
- **Filtrado en tiempo real**: Resultados se actualizan automáticamente
- **Selección de columna**: Filtrar por cualquier campo
- **Búsqueda inteligente**: Coincidencias parciales insensibles a mayúsculas

## 🔧 Solución de Problemas

### **Error de Conexión SQL Server**
```bash
# Verificar que SQL Server esté ejecutándose
# Verificar credenciales en config.py
# Verificar que el puerto 1433 esté abierto
# Verificar que ODBC Driver 17 esté instalado
```

### **Error de Driver ODBC**
```bash
# Instalar "ODBC Driver 17 for SQL Server"
# Verificar que esté en la lista de drivers ODBC
```

### **Error de Permisos**
```bash
# Verificar que el usuario tenga permisos en la base de datos
# Ejecutar como administrador
```

## 🧪 Datos de Ejemplo

El sistema incluye datos de ejemplo para pruebas:
- **Empleados**: 12 empleados activos con diferentes posiciones
- **Aplicaciones**: 45 aplicaciones en diferentes unidades
- **Historial**: 75 registros de procesos
- **Procesos**: 10 procesos de gestión

## 🔧 Tecnologías Utilizadas

- **Python 3.10+**
- **Tkinter/ttk**: Interfaz gráfica
- **SQLite3**: Base de datos por defecto
- **SQL Server**: Base de datos empresarial
- **pyodbc**: Conexión a SQL Server
- **Pandas**: Manipulación de datos
- **OpenPyXL**: Generación de archivos Excel
- **Threading**: Operaciones no bloqueantes

## 📋 Criterios de Aceptación Cumplidos

- ✅ **Conciliar Accesos**: Muestra qué apps otorgar/quitar por SID
- ✅ **Exportar Excel**: Crea archivo con dos hojas y filas correctas
- ✅ **Registrar Tickets**: Agrega filas en historial consistentes
- ✅ **Re-ejecutar**: La conciliación refleja el nuevo estado
- ✅ **Integración UI**: Usa StringVar existentes sin remaquetar
- ✅ **Base de Datos Dual**: SQLite y SQL Server funcionando
- ✅ **Lateral Movement**: Lógica aditiva implementada
- ✅ **Comparación de Registros**: Funciona correctamente con historial

## 🚀 Características Avanzadas

### **1. Lateral Movement Aditivo**
- **Mantiene accesos actuales**: No revoca accesos existentes
- **Agrega nuevos accesos**: Solo otorga accesos que no tiene
- **Coexistencia**: Permite aplicaciones con mismo nombre pero diferente subunit

### **2. Configuración Flexible**
- **Cambio fácil**: Entre SQLite y SQL Server
- **Herramientas de diagnóstico**: Verificación automática de configuración
- **Migración automática**: Datos se migran automáticamente

### **3. Robustez del Sistema**
- **Manejo de errores**: En cada operación
- **Verificaciones de integridad**: Antes de cada operación
- **Mensajes informativos**: Para debugging y monitoreo

## 📞 Soporte y Mantenimiento

### **Para problemas específicos:**
1. **Verificar logs** de la aplicación
2. **Revisar configuración** de base de datos
3. **Consultar documentación** técnica incluida
4. **Verificar permisos** de usuario y base de datos

### **Para actualizaciones:**
1. **Hacer backup** de la base de datos
2. **Probar cambios** en entorno de desarrollo
3. **Documentar cambios** realizados
4. **Capacitar usuarios** sobre nuevas funcionalidades

## ✅ Estado Final

**🎉 SISTEMA COMPLETAMENTE FUNCIONAL**

- ✅ Todas las funcionalidades implementadas
- ✅ Soporte dual de base de datos (SQLite + SQL Server)
- ✅ Lateral movement aditivo funcionando
- ✅ Conciliación de accesos precisa
- ✅ Interfaz moderna y responsive
- ✅ Herramientas de configuración incluidas
- ✅ Documentación completa
- ✅ Scripts de migración listos

**El sistema está listo para usar en producción con cualquiera de las dos bases de datos.**

---

## 📄 Licencia

Este proyecto es de uso interno para pruebas de trabajo.

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Mantener la estructura de código limpia y documentada
2. Seguir las convenciones de nomenclatura existentes
3. Probar cambios antes de enviar
4. Documentar nuevas funcionalidades
5. Actualizar este README cuando sea necesario



