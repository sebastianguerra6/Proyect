# Sistema de Gestión de Empleados - Refactorizado

## Descripción
Sistema de gestión de empleados desarrollado en Python con Tkinter, siguiendo principios de Programación Orientada a Objetos (POO) y arquitectura en capas.

## Características Principales

### 🏢 Gestión de Procesos
- **Onboarding**: Gestión de nuevos empleados, recontrataciones, transferencias internas y promociones
- **Offboarding**: Manejo de salidas definitivas, reducción de personal, fin de proyectos y cambios de empresa
- **Lateral Movement**: Control de movimientos horizontales, reasignaciones de proyecto, cambios de equipo y rotación de funciones

### 🔍 Edición y Búsqueda
- **Búsqueda por SID**: Localización rápida de registros anteriores por identificador de empleado
- **Edición de Campos**: Modificación de información de empleados existentes
- **Visualización de Resultados**: Tabla interactiva con todos los registros encontrados
- **Selección y Carga**: Carga automática de datos en formularios de edición

### 👥 Creación de Personas en Headcount
- **Formulario Completo**: Campos para información personal, laboral y de contacto
- **Validación de Datos**: Verificación de campos obligatorios
- **Almacenamiento JSON**: Persistencia de datos en archivo headcount.json
- **Gestión de Estados**: Control de estado laboral (Activo, Inactivo, Vacaciones, Licencia)

## Arquitectura del Sistema

### 📁 Estructura de Archivos
```
Pruebas-Tranbajo/
├── app_empleados_refactorizada.py    # Aplicación principal
├── data/                             # Capa de datos
│   ├── __init__.py
│   ├── repository.py                 # Repositorio de datos
│   ├── headcount.json               # Datos de personas
│   ├── datos_empleados_onboarding.json
│   ├── datos_empleados_offboarding.json
│   └── datos_empleados_lateral.json
├── models/                           # Modelos de datos
│   ├── __init__.py
│   ├── empleado.py                  # Modelo de empleado y persona
│   └── procesos.py                  # Modelos de procesos
├── services/                         # Capa de servicios
│   ├── __init__.py
│   └── empleado_service.py          # Lógica de negocio
└── ui/                              # Interfaz de usuario
    ├── __init__.py
    └── components.py                # Componentes de UI
```

### 🏗️ Patrones de Diseño
- **Arquitectura en Capas**: Separación clara entre UI, servicios y datos
- **Repository Pattern**: Abstracción del acceso a datos
- **Service Layer**: Lógica de negocio centralizada
- **Component-based UI**: Interfaz modular y reutilizable

## Funcionalidades por Pestaña

### 1. Gestión de Procesos
- **Campos Generales**: SID, Área, Subárea, Ingreso por, Fecha
- **Tipos de Proceso**: Selección dinámica entre Onboarding, Offboarding y Lateral Movement
- **Formularios Específicos**: Campos adaptados según el tipo de proceso seleccionado
- **Validación**: Verificación de campos obligatorios antes del guardado

### 2. Edición y Búsqueda
- **Búsqueda por SID**: Campo de entrada para buscar empleados específicos
- **Resultados en Tabla**: Visualización organizada de registros encontrados
- **Formulario de Edición**: Campos editables para modificar información
- **Integración con Servicios**: Búsqueda real en base de datos JSON

### 3. Crear Persona
- **Información Personal**: Nombre, apellido, email, teléfono
- **Información Laboral**: Departamento, cargo, fecha de contratación, salario
- **Estado del Empleado**: Control de estado laboral
- **Validación Completa**: Verificación de campos obligatorios y formato

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Tkinter**: Interfaz gráfica de usuario
- **JSON**: Almacenamiento de datos
- **POO**: Programación Orientada a Objetos
- **Arquitectura en Capas**: Separación de responsabilidades

## Instalación y Uso

### Requisitos
- Python 3.6 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución
```bash
python app_empleados_refactorizada.py
```

### Estructura de Datos
Los datos se almacenan en archivos JSON en el directorio `data/`:
- `headcount.json`: Personas del headcount
- `datos_empleados_onboarding.json`: Procesos de onboarding
- `datos_empleados_offboarding.json`: Procesos de offboarding
- `datos_empleados_lateral.json`: Movimientos laterales

## Características Técnicas

### 🔒 Validación de Datos
- Verificación de campos obligatorios
- Validación de formatos
- Manejo de errores con mensajes informativos

### 💾 Persistencia de Datos
- Almacenamiento en archivos JSON
- Estructura de datos consistente
- Manejo de errores de archivo

### 🎨 Interfaz de Usuario
- Diseño responsive y moderno
- Pestañas organizadas por funcionalidad
- Formularios intuitivos y fáciles de usar
- Mensajes de confirmación y error

### 🔍 Funcionalidades de Búsqueda
- Búsqueda por SID en todos los tipos de proceso
- Resultados presentados en tabla organizada
- Selección de registros para edición
- Carga automática de datos en formularios

## Mejoras Implementadas

### ✅ Funcionalidades Agregadas
- [x] Pestaña de Edición y Búsqueda por SID
- [x] Pestaña de Creación de Personas en Headcount
- [x] Sistema de búsqueda integrado
- [x] Formularios de edición funcionales
- [x] Validación de datos mejorada
- [x] Interfaz de usuario expandida

### 🔄 Funcionalidades Existentes Mejoradas
- [x] Arquitectura en pestañas principales
- [x] Sistema de estadísticas actualizado
- [x] Manejo de errores mejorado
- [x] Integración de servicios completa

## Próximas Mejoras Sugeridas

### 🚀 Funcionalidades Futuras
- [ ] Sistema de autenticación y roles
- [ ] Exportación de datos a Excel/CSV
- [ ] Reportes y dashboards
- [ ] Integración con bases de datos relacionales
- [ ] Sistema de notificaciones
- [ ] Historial de cambios y auditoría
- [ ] Backup automático de datos
- [ ] Interfaz web responsive

### 🧪 Testing y Calidad
- [ ] Crear tests unitarios y de integración
- [ ] Implementar CI/CD
- [ ] Análisis de código estático
- [ ] Cobertura de tests

## Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios siguiendo las convenciones del proyecto
4. Crear pull request con descripción detallada

## Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## Contacto

Para preguntas o sugerencias, contactar al equipo de desarrollo.

---

**Versión**: 2.0.0  
**Última Actualización**: Enero 2024  
**Estado**: En desarrollo activo
