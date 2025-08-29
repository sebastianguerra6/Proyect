import sqlite3
import os
from typing import List, Dict, Any, Tuple

class EmpleadoRepository:
    """Repositorio simplificado para manejar datos de empleados usando SQLite"""
    
    def __init__(self, db_path: str = "database/empleados.db"):
        self.db_path = db_path
        self._crear_tablas_si_no_existen()
    
    def _crear_tablas_si_no_existen(self):
        """Crea las tablas si no existen"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Crear tabla headcount
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS headcount (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_caso TEXT UNIQUE,
                    sid TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    departamento TEXT NOT NULL,
                    cargo TEXT NOT NULL,
                    fecha_contratacion DATE NOT NULL,
                    salario DECIMAL(10,2),
                    estado TEXT DEFAULT 'Activo',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Crear tabla procesos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procesos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_caso TEXT UNIQUE NOT NULL,
                    tipo_proceso TEXT NOT NULL,
                    sid TEXT NOT NULL,
                    nueva_sub_unidad TEXT NOT NULL,
                    nuevo_cargo TEXT NOT NULL,
                    request_date DATE NOT NULL,
                    ingreso_por TEXT NOT NULL,
                    fecha DATE NOT NULL,
                    status TEXT DEFAULT 'Pendiente',
                    mail TEXT,
                    closing_date_app DATE,
                    app_quality TEXT,
                    confirmation_by_user TEXT,
                    comment TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Error creando tablas: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def guardar_proceso(self, empleado_data: Dict[str, Any], tipo_proceso: str) -> Tuple[bool, str]:
        """Guarda un proceso en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Lista de nombres de aplicaciones para asignar aleatoriamente
            nombres_apps = [
                "Sistema de Gestión de Empleados",
                "Portal de Recursos Humanos",
                "Aplicación de Nómina",
                "Sistema de Control de Asistencia",
                "Portal de Beneficios",
                "Aplicación de Capacitación",
                "Sistema de Evaluación de Desempeño",
                "Portal de Comunicaciones Internas",
                "Aplicación de Gestión de Proyectos",
                "Sistema de Reportes Gerenciales",
                "Portal de Autogestión",
                "Aplicación de Gestión de Permisos",
                "Sistema de Seguridad y Accesos",
                "Portal de Documentación",
                "Aplicación de Gestión de Inventarios"
            ]
            
            # Seleccionar nombre de aplicación aleatorio
            import random
            app_name = random.choice(nombres_apps)
            
            cursor.execute('''
                INSERT INTO procesos (
                    numero_caso, tipo_proceso, sid, nueva_sub_unidad, nuevo_cargo,
                    request_date, ingreso_por, fecha, status, app_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                empleado_data.get('numero_caso'),
                tipo_proceso,
                empleado_data.get('sid'),
                empleado_data.get('nueva_sub_unidad'),
                empleado_data.get('nuevo_cargo'),
                empleado_data.get('request_date'),
                empleado_data.get('ingreso_por'),
                empleado_data.get('fecha'),
                empleado_data.get('status', 'Pendiente'),
                app_name
            ))
            
            conn.commit()
            conn.close()
            return True, f"Proceso guardado exitosamente con APP: {app_name}"
            
        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False, f"Error guardando proceso: {e}"
    
    def guardar_headcount(self, empleado_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Guarda una persona en el headcount"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO headcount (
                    numero_caso, sid, nombre, apellido, email, telefono, departamento,
                    cargo, fecha_contratacion, salario, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                empleado_data.get('numero_caso'),
                empleado_data.get('sid'),
                empleado_data.get('nombre'),
                empleado_data.get('apellido'),
                empleado_data.get('email'),
                empleado_data.get('telefono'),
                empleado_data.get('departamento'),
                empleado_data.get('cargo'),
                empleado_data.get('fecha_contratacion'),
                empleado_data.get('salario'),
                empleado_data.get('estado', 'Activo')
            ))
            
            conn.commit()
            conn.close()
            return True, "Persona agregada al headcount exitosamente"
            
        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False, f"Error guardando en headcount: {e}"
    
    def buscar_procesos(self, filtros: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Busca procesos según los filtros especificados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM procesos"
            params = []
            where_clauses = []
            
            if filtros:
                if filtros.get('numero_caso'):
                    where_clauses.append("numero_caso LIKE ?")
                    params.append(f"%{filtros['numero_caso']}%")
                
                if filtros.get('sid'):
                    where_clauses.append("sid LIKE ?")
                    params.append(f"%{filtros['sid']}%")
                
                if filtros.get('ingreso_por'):
                    where_clauses.append("ingreso_por LIKE ?")
                    params.append(f"%{filtros['ingreso_por']}%")
                
                if filtros.get('subunidad'):
                    where_clauses.append("nueva_sub_unidad LIKE ?")
                    params.append(f"%{filtros['subunidad']}%")
                
                if filtros.get('status'):
                    where_clauses.append("status LIKE ?")
                    params.append(f"%{filtros['status']}%")
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            query += " ORDER BY fecha_creacion DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            columnas = [desc[0] for desc in cursor.description]
            resultados = []
            
            for row in rows:
                resultado = dict(zip(columnas, row))
                resultados.append(resultado)
            
            conn.close()
            return resultados
            
        except sqlite3.Error as e:
            print(f"Error buscando procesos: {e}")
            return []
    
    def actualizar_proceso(self, numero_caso: str, datos_actualizados: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualiza un proceso existente"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            campos_actualizables = [
                'status', 'mail', 'closing_date_app', 'app_quality', 
                'confirmation_by_user', 'comment'
            ]
            
            set_clauses = []
            params = []
            
            for campo in campos_actualizables:
                if campo in datos_actualizados:
                    set_clauses.append(f"{campo} = ?")
                    params.append(datos_actualizados[campo])
            
            if not set_clauses:
                return False, "No hay campos para actualizar"
            
            params.append(numero_caso)
            
            query = f"UPDATE procesos SET {', '.join(set_clauses)} WHERE numero_caso = ?"
            
            cursor.execute(query, params)
            
            if cursor.rowcount == 0:
                return False, "No se encontró el proceso especificado"
            
            conn.commit()
            conn.close()
            return True, "Proceso actualizado exitosamente"
            
        except sqlite3.Error as e:
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False, f"Error actualizando proceso: {e}"
    
    def obtener_estadisticas(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            estadisticas = {}
            
            # Contar procesos por tipo
            cursor.execute("SELECT tipo_proceso, COUNT(*) FROM procesos GROUP BY tipo_proceso")
            for tipo, count in cursor.fetchall():
                estadisticas[tipo] = count
            
            # Contar headcount
            cursor.execute("SELECT COUNT(*) FROM headcount")
            estadisticas['headcount'] = cursor.fetchone()[0]
            
            conn.close()
            return estadisticas
            
        except sqlite3.Error as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {'onboarding': 0, 'offboarding': 0, 'lateral_movement': 0, 'headcount': 0}
    
    def buscar_headcount_por_sid(self, sid: str) -> List[Dict[str, Any]]:
        """Busca personas en el headcount por SID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT sid, nombre, apellido, email, telefono, departamento, cargo, estado
                FROM headcount 
                WHERE sid LIKE ?
                ORDER BY fecha_creacion DESC
            ''', (f"%{sid}%",))
            
            rows = cursor.fetchall()
            
            columnas = ['sid', 'nombre', 'apellido', 'email', 'telefono', 'departamento', 'cargo', 'estado']
            resultados = []
            
            for row in rows:
                resultado = dict(zip(columnas, row))
                resultados.append(resultado)
            
            conn.close()
            return resultados
            
        except sqlite3.Error as e:
            print(f"Error buscando headcount por SID: {e}")
            return []
    
    def obtener_todo_headcount(self) -> List[Dict[str, Any]]:
        """Obtiene todos los registros del headcount"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT sid, nombre, apellido, email, telefono, departamento, cargo, estado
                FROM headcount 
                ORDER BY fecha_creacion DESC
            ''')
            
            rows = cursor.fetchall()
            
            columnas = ['sid', 'nombre', 'apellido', 'email', 'telefono', 'departamento', 'cargo', 'estado']
            resultados = []
            
            for row in rows:
                resultado = dict(zip(columnas, row))
                resultados.append(resultado)
            
            conn.close()
            return resultados
            
        except sqlite3.Error as e:
            print(f"Error obteniendo todo el headcount: {e}")
            return []
