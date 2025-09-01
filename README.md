# Sistema de Gestión de Empleados - Refactorizado

## Descripción
Aplicación de escritorio desarrollada en Python con Tkinter para la gestión de empleados, incluyendo procesos de onboarding, offboarding y movimientos laterales, **ahora con sistema de conciliación de accesos avanzado**.

## Características Principales

### 🎨 Interfaz Mejorada
- **Menú de navegación más grande**: Botones laterales con mayor tamaño y mejor espaciado
- **Imágenes en botones**: Emojis y iconos para mejor identificación visual
- **Estilos personalizados**: Sistema de estilos consistente y moderno
- **Ventana ampliada**: Tamaño 1600x800 para mejor aprovechamiento del espacio

### 🔧 Funcionalidades
- **Gestión de Procesos**: Formularios para onboarding, offboarding y movimientos laterales
- **Edición y Búsqueda**: Herramientas para modificar y consultar registros existentes
- **Creación de Personas**: Formulario para agregar nuevos empleados al sistema
- **Base de Datos**: Almacenamiento persistente con SQLite
- **Filtrado Avanzado**: Sistema de filtrado en tiempo real con selección de columna
- **🆕 Conciliación de Accesos**: Sistema completo para gestionar permisos de usuarios

### 📱 Navegación
- **Botones Laterales**: Menú de navegación intuitivo con iconos descriptivos
- **Pestañas Dinámicas**: Sistema de pestañas que se crean según la selección del usuario
- **Estados Visuales**: Indicadores visuales para botones activos e inactivos

## 🆕 Sistema de Conciliación de Accesos

### Características del Sistema
- **Conciliación por SID**: Analiza accesos actuales vs. autorizados para un usuario específico
- **Conciliación Masiva**: Procesa todos los usuarios del sistema
- **Exportación a Excel**: Genera reportes con hojas de resumen y tickets
- **Registro de Tickets**: Crea tickets automáticos para accesos a otorgar/revocar
- **Historial Completo**: Seguimiento de todos los cambios de accesos

### Funcionalidades Implementadas
- ✅ **Conciliar Accesos**: Por SID específico
- ✅ **Exportar Excel**: Con formato profesional y múltiples hojas
- ✅ **Registrar Tickets**: Inserta en histórico lo calculado
- ✅ **Conciliar Todos**: Procesamiento masivo del sistema
- ✅ **Base de Datos SQLite**: Esquema completo con tablas y vistas

### Estructura de Base de Datos
```sql
-- Personas
CREATE TABLE IF NOT EXISTS person (
  sid TEXT PRIMARY KEY,
  area TEXT,
  subunit TEXT,
  cargo TEXT,
  email TEXT,
  updated_at TEXT
);

-- Matriz de autorizaciones por puesto
CREATE TABLE IF NOT EXISTS authorized_matrix (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subunit TEXT NOT NULL,
  cargo TEXT NOT NULL,
  app_name TEXT NOT NULL,
  role_name TEXT,
  UNIQUE(subunit, cargo, app_name, IFNULL(role_name,'')) ON CONFLICT IGNORE
);

-- Historial de accesos
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
);
```

## Estructura del Proyecto

```
Pruebas-Tranbajo/
├── app/
│   └── main.py                    # 🆕 Aplicación principal de conciliación
├── app_empleados_refactorizada.py # Aplicación original de empleados
├── ui/
│   ├── components.py              # Componentes de interfaz originales
│   ├── styles.py                  # Estilos personalizados
│   └── bindings.py                # 🆕 Bindings para conciliación
├── db/
│   ├── __init__.py                # 🆕 Módulo de base de datos
│   ├── schema.py                  # 🆕 Esquema y vistas SQL
│   ├── connection.py              # 🆕 Conexión y manejo de BD
│   └── queries.py                 # 🆕 Consultas SQL centralizadas
├── services/
│   ├── __init__.py                # 🆕 Módulo de servicios
│   ├── reconcile_service.py       # 🆕 Servicio de conciliación
│   ├── export_service.py          # 🆕 Servicio de exportación Excel
│   └── history_service.py         # 🆕 Servicio de historial
├── models/
│   └── empleado.py                # Modelo de datos
├── data/
│   └── repository.py              # Acceso a datos
├── database/
│   ├── empleados.db               # Base de datos SQLite
│   ├── init_database.py           # Inicialización de BD
│   └── update_database.py         # Actualizaciones de BD
├── output/                         # 🆕 Directorio de archivos Excel
├── requirements.txt                # 🆕 Dependencias del proyecto
└── README.md                      # Documentación
```

## 🚀 Cómo Ejecutar

### 1. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 2. Aplicación Original de Empleados
```bash
python app_empleados_refactorizada.py
```

### 3. 🆕 Sistema de Conciliación de Accesos
```bash
python app/main.py
```

## 🔍 Sistema de Filtrado Avanzado

### Características del Filtrado
- **Input de Texto**: Campo para ingresar el texto a buscar
- **Selección de Columna**: Menú desplegable con 12 columnas disponibles
- **Filtrado en Tiempo Real**: Resultados se actualizan automáticamente al escribir
- **Búsqueda Inteligente**: Coincidencias parciales insensibles a mayúsculas/minúsculas
- **Controles Manuales**: Botones para aplicar y limpiar filtros

### Ubicaciones del Sistema de Filtrado
- **Edición y Búsqueda**: Filtrado por 12 columnas de procesos
- **Creación de Persona**: Filtrado por 7 columnas de empleados

## 🆕 Uso del Sistema de Conciliación

### 1. Conciliar Accesos por SID
1. Ingrese el SID del usuario
2. Haga clic en "🔍 Conciliar Accesos"
3. Revise los resultados en la tabla

### 2. Exportar a Excel
1. Después de una conciliación, haga clic en "📊 Exportar Excel"
2. Se genera archivo con hojas de resumen y tickets

### 3. Registrar Tickets
1. Revise los resultados de conciliación
2. Haga clic en "📝 Registrar Tickets"
3. Los tickets se crean en el historial

### 4. Conciliación Masiva
1. Haga clic en "🌐 Conciliar Todos"
2. Se procesan todos los usuarios del sistema
3. Los resultados están disponibles para exportación

## Estilos Personalizados

La aplicación utiliza un sistema de estilos personalizado que incluye:
- **Botones de Navegación**: Estilo `Nav.TButton` con efectos hover
- **Botones de Acción**: Estilos `Success`, `Info`, `Warning`, `Danger`
- **Labels**: Estilos `Title`, `Section`, `Subsection`
- **Frames**: Estilos `Main.TFrame`, `Nav.TLabelframe`

## 🧪 Datos de Ejemplo

El sistema incluye datos de ejemplo para pruebas:
- **3 personas** con diferentes cargos y subunidades
- **7 autorizaciones** en la matriz de permisos
- **4 registros** en el historial de accesos

## 🔧 Tecnologías Utilizadas

- **Python 3.10+**
- **Tkinter/ttk**: Interfaz gráfica
- **SQLite3**: Base de datos
- **Pandas**: Manipulación de datos
- **OpenPyXL**: Generación de archivos Excel
- **Threading**: Operaciones no bloqueantes

## 📋 Criterios de Aceptación Cumplidos

- ✅ **Conciliar Accesos**: Muestra qué apps otorgar/quitar por SID
- ✅ **Exportar Excel**: Crea archivo con dos hojas y filas correctas
- ✅ **Registrar Tickets**: Agrega filas en access_history consistentes
- ✅ **Re-ejecutar**: La conciliación refleja el nuevo estado
- ✅ **Integración UI**: Usa StringVar existentes sin remaquetar
- ✅ **Base de Datos**: Esquema SQLite idempotente con migraciones

## Contribuciones

Para contribuir al proyecto:
1. Mantener la estructura de código limpia y documentada
2. Seguir las convenciones de nomenclatura existentes
3. Probar cambios antes de enviar
4. Documentar nuevas funcionalidades

## Licencia

Este proyecto es de uso interno para pruebas de trabajo.
