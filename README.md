# Sistema de Gestión de Empleados - Versión Refactorizada

Una aplicación de escritorio desarrollada en Python con Tkinter para gestionar procesos de empleados, siguiendo buenas prácticas de Programación Orientada a Objetos (POO) y arquitectura en capas.

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado siguiendo el patrón de **Arquitectura en Capas** con separación clara de responsabilidades:

```
Pruebas-Tranbajo/
├── models/                    # Capa de Modelos (Entidades de negocio)
│   ├── __init__.py
│   ├── empleado.py           # Clase Empleado
│   └── procesos.py           # Clases Onboarding, Offboarding, LateralMovement
├── data/                     # Capa de Datos (Acceso a datos)
│   ├── __init__.py
│   └── repository.py         # EmpleadoRepository
├── services/                 # Capa de Servicios (Lógica de negocio)
│   ├── __init__.py
│   └── empleado_service.py   # EmpleadoService
├── ui/                       # Capa de Presentación (Interfaz de usuario)
│   ├── __init__.py
│   └── components.py         # Componentes de UI reutilizables
├── app_empleados.py          # Versión original (monolítica)
├── app_empleados_refactorizada.py  # Versión refactorizada
└── README.md
```

## 📋 Características

### Campos Generales
- **ID**: Identificador único del empleado
- **Área**: Área o departamento del empleado
- **Empleo**: Cargo o puesto del empleado
- **Quien hace el ingreso**: Persona responsable del registro
- **Fecha**: Fecha del registro (se establece automáticamente)

### Tipos de Proceso

#### 1. Onboarding
Campos específicos para nuevos empleados:
- Fecha de Ingreso
- Departamento Destino
- Supervisor
- Salario
- Tipo de Contrato (Indefinido, Temporal, Prácticas, Otro)
- Observaciones

#### 2. Offboarding
Campos específicos para empleados que salen:
- Fecha de Salida
- Motivo de Salida (Renuncia, Despido, Fin de contrato, Jubilación, Otro)
- Tipo de Salida (Voluntaria, Involuntaria, Mutuo acuerdo)
- Entrevista de Salida (Sí, No, Pendiente)
- Equipos Devueltos (Completo, Pendiente, No aplica)
- Observaciones

#### 3. Lateral Movement
Campos específicos para movimientos internos:
- Fecha de Movimiento
- Departamento Origen
- Departamento Destino
- Cargo Anterior
- Cargo Nuevo
- Motivo del Movimiento (Promoción, Reorganización, Desarrollo profesional, Necesidad del negocio, Otro)
- Observaciones

## 🚀 Instalación y Uso

### Requisitos
- Python 3.6 o superior
- Tkinter (incluido con Python)

### Ejecución

#### Versión Refactorizada (Recomendada)
```bash
python app_empleados_refactorizada.py
```

#### Versión Original
```bash
python app_empleados.py
```

### Instrucciones de Uso

1. **Llenar información general**: Complete los campos ID, Área, Empleo, y opcionalmente "Quien hace el ingreso"

2. **Seleccionar tipo de proceso**: 
   - Vaya a la pestaña "Seleccionar Proceso"
   - Elija entre Onboarding, Offboarding o Lateral Movement

3. **Completar información específica**: 
   - Se abrirá automáticamente una nueva pestaña con campos específicos según el tipo seleccionado
   - Complete los campos requeridos

4. **Guardar datos**: 
   - Haga clic en "Guardar" para almacenar la información
   - Los datos se guardan en archivos JSON separados por tipo de proceso

5. **Funciones adicionales**:
   - **Limpiar**: Borra todos los campos y empieza un nuevo registro
   - **Estadísticas**: Muestra el número de registros por tipo de proceso

## 🏛️ Arquitectura Detallada

### Capa de Modelos (`models/`)
- **Empleado**: Representa la entidad básica del empleado
- **ProcesoBase**: Clase base para todos los tipos de proceso
- **Onboarding/Offboarding/LateralMovement**: Clases específicas para cada tipo de proceso

### Capa de Datos (`data/`)
- **EmpleadoRepository**: Maneja el almacenamiento y recuperación de datos
- Persistencia en archivos JSON separados por tipo de proceso
- Manejo de errores y validación de datos

### Capa de Servicios (`services/`)
- **EmpleadoService**: Contiene toda la lógica de negocio
- Validación de datos
- Creación de objetos de dominio
- Coordinación entre capas

### Capa de Presentación (`ui/`)
- **Componentes reutilizables**: CamposGeneralesFrame, OnboardingFrame, etc.
- Separación de responsabilidades de UI
- Fácil mantenimiento y extensión

## 💾 Almacenamiento de Datos

Los datos se guardan en archivos JSON separados en el directorio `data/`:
- `data/datos_empleados_onboarding.json` - Para procesos de onboarding
- `data/datos_empleados_offboarding.json` - Para procesos de offboarding  
- `data/datos_empleados_lateral.json` - Para movimientos laterales

Cada archivo contiene un array de objetos con toda la información registrada.

## ✨ Ventajas de la Arquitectura Refactorizada

### 🔧 Mantenibilidad
- **Código modular**: Cada componente tiene una responsabilidad específica
- **Fácil extensión**: Agregar nuevos tipos de proceso es sencillo
- **Reutilización**: Los componentes pueden ser reutilizados

### 🧪 Testabilidad
- **Separación de capas**: Cada capa puede ser testeada independientemente
- **Inyección de dependencias**: Los servicios reciben sus dependencias como parámetros
- **Lógica aislada**: La lógica de negocio está separada de la UI

### 📈 Escalabilidad
- **Arquitectura en capas**: Fácil agregar nuevas funcionalidades
- **Patrones de diseño**: Uso de Repository y Service patterns
- **Tipado estático**: Uso de type hints para mejor documentación

### 🛡️ Robustez
- **Manejo de errores**: Validación en múltiples capas
- **Persistencia segura**: Manejo robusto de archivos JSON
- **Validación de datos**: Verificación de integridad en cada capa

## 🔄 Comparación de Versiones

| Aspecto | Versión Original | Versión Refactorizada |
|---------|------------------|----------------------|
| **Estructura** | Monolítica | Arquitectura en capas |
| **Mantenibilidad** | Baja | Alta |
| **Testabilidad** | Difícil | Fácil |
| **Extensibilidad** | Limitada | Alta |
| **Reutilización** | Baja | Alta |
| **Separación de responsabilidades** | No | Sí |

## 🚀 Funcionalidades Adicionales

- **Estadísticas**: Vista del número de registros por tipo
- **Validación robusta**: Validación en múltiples capas
- **Manejo de errores**: Mensajes informativos y manejo de excepciones
- **Componentes reutilizables**: UI modular y extensible

## 📝 Próximas Mejoras

- [ ] Agregar base de datos SQLite
- [ ] Implementar sistema de búsqueda y filtros
- [ ] Agregar exportación a Excel/PDF
- [ ] Implementar sistema de usuarios y permisos
- [ ] Agregar logs de auditoría
- [ ] Crear tests unitarios y de integración
