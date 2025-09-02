# 🚀 Sistema Integrado de Gestión de Empleados y Aplicaciones

## Descripción
Sistema completo e integrado que combina la gestión de empleados, procesos de onboarding/offboarding, conciliación de accesos y **gestión de aplicaciones del sistema** en una sola interfaz unificada.

## ✨ Características Principales

### 🔧 Módulos Integrados
1. **📋 Gestión de Procesos** - Creación y gestión de procesos de empleados
2. **🔍 Edición y Búsqueda** - Búsqueda y edición de empleados existentes
3. **👤 Crear Persona** - Creación de nuevos empleados en el sistema
4. **🔐 Conciliación de Accesos** - Verificación de accesos y permisos
5. **📱 Gestión de Aplicaciones** - **NUEVO**: Gestión completa de aplicaciones del sistema

### 🎨 Interfaz Unificada
- **Navegación lateral** con botones intuitivos
- **Diseño responsive** que se adapta a diferentes tamaños de pantalla
- **Estilos consistentes** en toda la aplicación
- **Transiciones suaves** entre módulos

## 📋 Requisitos Previos

### 1. Base de Datos
Antes de usar la interfaz, debe ejecutar:
```bash
cd database
python database_completa.py
```

### 2. Python
- Python 3.7 o superior
- Tkinter (incluido con Python estándar)
- SQLite3 (incluido con Python estándar)

### 3. Estructura de Archivos
```
proyecto/
├── database/
│   ├── empleados.db          # Base de datos (creada por database_completa.py)
│   └── database_completa.py  # Script de creación de BD
├── app_empleados_refactorizada.py  # Interfaz principal integrada
├── models/                   # Modelos de datos
├── data/                     # Repositorios de datos
├── services/                 # Servicios de negocio
├── ui/                       # Componentes de interfaz
└── README_Interfaz_Integrada.md  # Este archivo
```

## 🚀 Instalación y Uso

### Paso 1: Crear la Base de Datos
```bash
cd database
python database_completa.py
```

### Paso 2: Ejecutar la Interfaz Integrada
```bash
python app_empleados_refactorizada.py
```

## 📖 Guía de Uso

### 🧭 Navegación
La interfaz tiene una **barra de navegación lateral** con 5 módulos principales:

1. **📋 Gestión de Procesos** - Formularios para crear procesos de empleados
2. **🔍 Edición y Búsqueda** - Buscar y editar empleados existentes
3. **👤 Crear Persona** - Crear nuevos empleados en el sistema
4. **🔐 Conciliación de Accesos** - Verificar y reconciliar accesos
5. **📱 Gestión de Aplicaciones** - **NUEVO**: Gestionar aplicaciones del sistema

### 📱 Gestión de Aplicaciones (NUEVO)

#### 🆕 Agregar Nueva Aplicación
1. Haga clic en **"📱 Gestión de Aplicaciones"** en la navegación lateral
2. Haga clic en **"➕ Nueva Aplicación"**
3. Complete el formulario:
   - **Nombre**: Nombre único de la aplicación
   - **Descripción**: Descripción detallada
   - **Categoría**: Seleccione o escriba una categoría
   - **Propietario**: Seleccione o escriba el propietario
4. Haga clic en **"Guardar"**

#### ✏️ Editar Aplicación
1. Seleccione la aplicación en la tabla
2. Haga clic en **"✏️ Editar"** o **doble clic** en la fila
3. Modifique los campos deseados
4. Haga clic en **"Guardar"**

#### 🗑️ Eliminar Aplicación
1. Seleccione la aplicación en la tabla
2. Haga clic en **"🗑️ Eliminar"**
3. Confirme la eliminación

#### 🔍 Buscar Aplicaciones
- Use el campo de búsqueda para filtrar por:
  - Nombre de la aplicación
  - Descripción
  - Categoría
  - Propietario
- La búsqueda es en tiempo real

#### 📊 Exportar Datos
1. Aplique filtros si desea exportar solo ciertas aplicaciones
2. Haga clic en **"📊 Exportar"**
3. Seleccione ubicación y nombre del archivo CSV

### 🔧 Gestión de Procesos
- **Onboarding**: Nuevos empleados
- **Offboarding**: Salida de empleados
- **Lateral Movement**: Movimientos internos
- Formularios con validación automática
- Generación automática de números de caso

### 🔍 Edición y Búsqueda
- Búsqueda por múltiples criterios
- Edición en línea de datos
- Historial de cambios
- Filtros avanzados

### 👤 Creación de Personas
- Formulario completo de empleado
- Validación de campos obligatorios
- Generación automática de SID
- Integración con procesos

### 🔐 Conciliación de Accesos
- Verificación de accesos actuales vs. esperados
- Generación de tickets de conciliación
- Exportación a Excel
- Registro en historial

## ⌨️ Atajos de Teclado

### Navegación General
- **Tab**: Navegar entre campos
- **Enter**: Ejecutar acción principal
- **Escape**: Cancelar operación

### Gestión de Aplicaciones
- **Doble clic**: Editar aplicación
- **Delete**: Eliminar aplicación seleccionada
- **Ctrl+F**: Enfocar búsqueda

### Gestión de Procesos
- **Ctrl+S**: Guardar proceso
- **Ctrl+L**: Limpiar formulario
- **F1**: Mostrar ayuda

## 🎨 Personalización

### Colores por Estado (Aplicaciones)
- **🟢 Activo**: Fondo verde claro (#d4edda)
- **🔴 Inactivo**: Fondo rojo claro (#f8d7da)
- **🟡 Mantenimiento**: Fondo amarillo claro (#fff3cd)

### Estilos Responsive
- **Pantalla pequeña** (< 1200px): Layout compacto
- **Pantalla mediana** (1200-1400px): Layout balanceado
- **Pantalla grande** (> 1400px): Layout espacioso

## 🔒 Seguridad y Validación

### Gestión de Aplicaciones
- **Verificación de dependencias** antes de eliminar
- **Validación de campos obligatorios**
- **Prevención de duplicados** por nombre
- **Confirmación de acciones destructivas**

### Gestión de Empleados
- **Validación de campos obligatorios**
- **Verificación de integridad referencial**
- **Generación automática de identificadores únicos**
- **Auditoría de cambios**

## 🐛 Solución de Problemas

### Error: "Base de datos no encontrada"
**Solución**: Ejecute primero `database_completa.py` para crear la base de datos.

### Error: "No se puede eliminar la aplicación"
**Causa**: La aplicación tiene roles o procesos asociados.
**Solución**: Elimine las dependencias primero o cambie el estado a "Inactivo".

### La interfaz no responde
**Solución**: Verifique que la base de datos no esté siendo usada por otro proceso.

### Error de importación de módulos
**Solución**: Verifique que todos los archivos estén en las carpetas correctas.

## 🔧 Estructura del Código

### Clases Principales
- **`AppEmpleadosRefactorizada`**: Clase principal de la aplicación
- **`AplicacionesFrame`**: Gestión de aplicaciones
- **`ApplicationManager`**: Operaciones de base de datos para aplicaciones
- **`ApplicationDialog`**: Diálogo para agregar/editar aplicaciones
- **`ConciliacionFrame`**: Conciliación de accesos

### Arquitectura
- **Separación de responsabilidades** entre UI, lógica de negocio y datos
- **Componentes modulares** para cada funcionalidad
- **Sistema de navegación** unificado
- **Gestión de estado** centralizada

## 📈 Funcionalidades Futuras

### Gestión de Aplicaciones
- [ ] Exportación a Excel (.xlsx)
- [ ] Importación desde CSV/Excel
- [ ] Historial de cambios
- [ ] Backup automático

### Sistema General
- [ ] Gráficos estadísticos
- [ ] Sistema de permisos por usuario
- [ ] Integración con APIs externas
- [ ] Notificaciones en tiempo real
- [ ] Modo oscuro/claro

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Cree una rama para su feature
3. Implemente los cambios
4. Envíe un pull request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Vea el archivo LICENSE para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Abra un issue en el repositorio
- Consulte la documentación de la base de datos
- Revise los logs de error en la consola

---

## 🎯 Resumen de la Integración

La **Gestión de Aplicaciones** se ha integrado completamente en la interfaz principal, proporcionando:

✅ **Navegación unificada** con botón dedicado  
✅ **Interfaz consistente** con el resto del sistema  
✅ **Funcionalidades completas** de CRUD para aplicaciones  
✅ **Integración con la base de datos** existente  
✅ **Estilos responsive** que se adaptan al diseño general  
✅ **Validaciones y seguridad** integradas  

**¡El sistema ahora es una solución completa y unificada para la gestión empresarial!**

---

**Desarrollado con ❤️ para la gestión eficiente de empleados y aplicaciones empresariales**
