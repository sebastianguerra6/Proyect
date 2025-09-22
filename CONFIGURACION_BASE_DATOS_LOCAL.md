# Configuración de Base de Datos Local (SQLite)

## ✅ **Estado Actual**

La aplicación está configurada para usar **SQLite** como base de datos local para pruebas.

### 📋 **Configuración Actual:**

```python
# En config.py
USE_SQL_SERVER = False  # ← Usando SQLite (base de datos local)
```

### 🗄️ **Base de Datos Local:**
- **Tipo**: SQLite
- **Archivo**: `database/empleados.db`
- **Tamaño**: ~151 KB
- **Tablas**: 27 tablas creadas
- **Empleados**: 13 empleados activos

## 🚀 **Cómo Usar la Aplicación**

### **1. Ejecutar la Aplicación Principal:**
```bash
python app_empleados_refactorizada.py
```

### **2. Ejecutar Pruebas E2E:**
```bash
python tests/test_access_eddu_flow.py
```

### **3. Cambiar a SQL Server (si es necesario):**
```bash
python cambiar_base_datos.py
# Seleccionar opción 2 para SQL Server
```

## 📊 **Verificación de Funcionamiento**

### **✅ Servicio de Acceso:**
- ✅ Se conecta correctamente a SQLite
- ✅ Encuentra 13 empleados en la base de datos
- ✅ Todas las funcionalidades disponibles

### **✅ Base de Datos:**
- ✅ Archivo `database/empleados.db` existe
- ✅ Esquema completo creado
- ✅ Datos de prueba disponibles
- ✅ Sin errores de conexión

### **✅ Aplicación Principal:**
- ✅ Se ejecuta sin errores
- ✅ Interfaz gráfica funciona
- ✅ Todas las funcionalidades disponibles

## 🔧 **Funcionalidades Disponibles**

### **Gestión de Empleados:**
- ✅ Crear empleados
- ✅ Editar empleados
- ✅ Buscar empleados
- ✅ Filtrado avanzado

### **Procesos de Acceso:**
- ✅ Onboarding
- ✅ Offboarding
- ✅ Lateral movement
- ✅ Conciliación de accesos

### **Reportes y Exportación:**
- ✅ Exportar a Excel
- ✅ Generar reportes
- ✅ Estadísticas del sistema

## 📁 **Estructura de la Base de Datos Local**

```
database/
└── empleados.db
    ├── headcount (13 empleados)
    ├── applications (45 aplicaciones)
    ├── historico (75 registros)
    ├── procesos (10 procesos)
    └── [vistas y índices]
```

## 🧪 **Datos de Prueba Disponibles**

### **Empleados de Prueba:**
- **S7547774**: Empleado de prueba para E2E
- **12 empleados adicionales**: Con diferentes posiciones y unidades

### **Aplicaciones de Prueba:**
- **45 aplicaciones**: En diferentes unidades (RRHH, TECNOLOGÍA, EDDU)
- **Políticas de acceso**: Para diferentes posiciones

### **Historial de Prueba:**
- **75 registros**: Procesos de onboarding/offboarding
- **Datos realistas**: Para pruebas completas

## ⚠️ **Notas Importantes**

### **Para Pruebas:**
- ✅ La base de datos local es perfecta para pruebas
- ✅ No requiere configuración de servidor
- ✅ Datos se mantienen entre sesiones
- ✅ Fácil de respaldar y restaurar

### **Para Producción:**
- 🔄 Cambiar a SQL Server cuando sea necesario
- 🔄 Usar `python cambiar_base_datos.py`
- 🔄 Configurar credenciales de SQL Server

## 🚀 **Próximos Pasos**

1. **Usar la aplicación** con la base de datos local
2. **Ejecutar pruebas** para verificar funcionalidad
3. **Desarrollar nuevas características** con datos locales
4. **Migrar a SQL Server** cuando esté listo para producción

## ✅ **Estado Final**

**🎉 APLICACIÓN CONFIGURADA PARA BASE DE DATOS LOCAL**

- ✅ SQLite configurado como base de datos por defecto
- ✅ Aplicación funcionando correctamente
- ✅ Todas las funcionalidades disponibles
- ✅ Datos de prueba listos
- ✅ Pruebas E2E funcionando

**La aplicación está lista para usar con la base de datos local para tus pruebas.**



