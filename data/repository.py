import sqlite3
import os
from typing import List, Dict, Any, Tuple
import sys

# Agregar el directorio database al path para importar config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from config import get_db_path

class EmpleadoRepository:
    """Repositorio simplificado para manejar datos de empleados usando SQLite"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_db_path()
        self._crear_tablas_si_no_existen()
    
    def _crear_tablas_si_no_existen(self):
        """Crea las tablas básicas si no existen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla empleados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sid TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                cargo TEXT,
                sub_unidad TEXT,
                estado TEXT DEFAULT 'Activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla procesos (usar estructura existente)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procesos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_caso TEXT,
                tipo_proceso TEXT,
                sid TEXT,
                nueva_sub_unidad TEXT,
                nuevo_cargo TEXT,
                request_date DATE,
                ingreso_por TEXT,
                fecha DATE,
                status TEXT DEFAULT 'Pendiente',
                app_name TEXT,
                mail TEXT,
                closing_date_app DATE,
                app_quality TEXT,
                confirmation_by_user TEXT,
                comment TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos con configuración para evitar bloqueos"""
        return sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
    
    def crear_empleado(self, sid: str, nombre: str, cargo: str = None, sub_unidad: str = None) -> bool:
        """Crea un nuevo empleado"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO empleados (sid, nombre, cargo, sub_unidad)
                VALUES (?, ?, ?, ?)
            ''', (sid, nombre, cargo, sub_unidad))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # SID duplicado
        except Exception as e:
            print(f"Error creando empleado: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    def buscar_empleado(self, sid: str = None, nombre: str = None) -> List[Dict[str, Any]]:
        """Busca empleados por SID o nombre"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if sid:
                cursor.execute('SELECT * FROM empleados WHERE sid = ?', (sid,))
            elif nombre:
                cursor.execute('SELECT * FROM empleados WHERE nombre LIKE ?', (f'%{nombre}%',))
            else:
                cursor.execute('SELECT * FROM empleados ORDER BY nombre')
            
            empleados = []
            for row in cursor.fetchall():
                empleados.append({
                    'id': row[0],
                    'sid': row[1],
                    'nombre': row[2],
                    'cargo': row[3],
                    'sub_unidad': row[4],
                    'estado': row[5],
                    'fecha_creacion': row[6]
                })
            
            return empleados
        except Exception as e:
            print(f"Error buscando empleado: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def obtener_procesos(self, empleado_sid: str = None) -> List[Dict[str, Any]]:
        """Obtiene procesos de empleados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if empleado_sid:
            cursor.execute('SELECT * FROM procesos WHERE sid = ?', (empleado_sid,))
        else:
            cursor.execute('SELECT * FROM procesos ORDER BY fecha_creacion DESC')
        
        procesos = []
        for row in cursor.fetchall():
            procesos.append({
                'id': row[0],
                'numero_caso': row[1],
                'tipo_proceso': row[2],
                'sid': row[3],
                'nueva_sub_unidad': row[4],
                'nuevo_cargo': row[5],
                'request_date': row[6],
                'ingreso_por': row[7],
                'fecha': row[8],
                'status': row[9],
                'app_name': row[10],
                'mail': row[11],
                'closing_date_app': row[12],
                'app_quality': row[13],
                'confirmation_by_user': row[14],
                'comment': row[15],
                'fecha_creacion': row[16],
                'fecha_actualizacion': row[17]
            })
        
        conn.close()
        return procesos
    
    def actualizar_empleado(self, sid: str, datos: Dict[str, Any]) -> bool:
        """Actualiza un empleado existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Construir query dinámicamente
            campos = []
            valores = []
            for campo, valor in datos.items():
                if campo != 'sid' and valor is not None:
                    campos.append(f"{campo} = ?")
                    valores.append(valor)
            
            if not campos:
                return False
            
            query = f"UPDATE empleados SET {', '.join(campos)} WHERE sid = ?"
            valores.append(sid)
            
            cursor.execute(query, valores)
            conn.commit()
            conn.close()
            
            return cursor.rowcount > 0
        except Exception:
            return False
    
    # Métodos compatibilidad para la aplicación existente
    def guardar_proceso(self, datos: Dict[str, Any], tipo_proceso: str) -> Tuple[bool, str]:
        """Guarda un proceso (método de compatibilidad)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO procesos (numero_caso, tipo_proceso, sid, nueva_sub_unidad, nuevo_cargo, 
                                   request_date, ingreso_por, fecha, status, app_name, mail, 
                                   closing_date_app, app_quality, confirmation_by_user, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos.get('numero_caso', ''),
                tipo_proceso,
                datos.get('sid'),
                datos.get('nueva_sub_unidad', ''),
                datos.get('nuevo_cargo', ''),
                datos.get('request_date', ''),
                datos.get('ingreso_por', ''),
                datos.get('fecha', ''),
                datos.get('status', 'Pendiente'),
                datos.get('app_name', ''),
                datos.get('mail', ''),
                datos.get('closing_date_app', ''),
                datos.get('app_quality', ''),
                datos.get('confirmation_by_user', ''),
                datos.get('comment', '')
            ))
            
            conn.commit()
            conn.close()
            return True, "Proceso guardado exitosamente"
        except Exception as e:
            return False, f"Error guardando proceso: {str(e)}"
    
    def guardar_headcount(self, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """Guarda un empleado (método de compatibilidad)"""
        try:
            exito = self.crear_empleado(
                sid=datos.get('sid'),
                nombre=datos.get('nombre'),
                cargo=datos.get('cargo'),
                sub_unidad=datos.get('sub_unidad')
            )
            if exito:
                return True, "Empleado guardado exitosamente"
            else:
                return False, "Error guardando empleado"
        except Exception as e:
            return False, f"Error guardando empleado: {str(e)}"
    
    def obtener_todo_headcount(self) -> List[Dict[str, Any]]:
        """Obtiene todos los empleados (método de compatibilidad)"""
        return self.buscar_empleado()
    
    def buscar_procesos(self, filtros: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Busca procesos con filtros (método de compatibilidad)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Construir query base
            query = 'SELECT * FROM procesos'
            params = []
            where_clauses = []
            
            if filtros:
                # Filtro por SID
                if filtros.get('sid'):
                    where_clauses.append('sid = ?')
                    params.append(filtros['sid'])
                
                # Filtro por número de caso
                if filtros.get('numero_caso'):
                    where_clauses.append('numero_caso = ?')
                    params.append(filtros['numero_caso'])
                
                # Filtro por tipo de proceso
                if filtros.get('tipo_proceso'):
                    where_clauses.append('tipo_proceso = ?')
                    params.append(filtros['tipo_proceso'])
                
                # Filtro por estado
                if filtros.get('estado'):
                    where_clauses.append('status = ?')
                    params.append(filtros['estado'])
            
            # Agregar WHERE si hay filtros
            if where_clauses:
                query += ' WHERE ' + ' AND '.join(where_clauses)
            
            # Ordenar por fecha de creación descendente
            query += ' ORDER BY fecha_creacion DESC'
            
            cursor.execute(query, params)
            procesos = []
            
            for row in cursor.fetchall():
                procesos.append({
                    'id': row[0],
                    'numero_caso': row[1],
                    'tipo_proceso': row[2],
                    'sid': row[3],
                    'nueva_sub_unidad': row[4],
                    'nuevo_cargo': row[5],
                    'request_date': row[6],
                    'ingreso_por': row[7],
                    'fecha': row[8],
                    'status': row[9],
                    'app_name': row[10],
                    'mail': row[11],
                    'closing_date_app': row[12],
                    'app_quality': row[13],
                    'confirmation_by_user': row[14],
                    'comment': row[15],
                    'fecha_creacion': row[16],
                    'fecha_actualizacion': row[17]
                })
            
            conn.close()
            return procesos
            
        except Exception as e:
            print(f"Error en buscar_procesos: {e}")
            return []
    
    def buscar_headcount_por_sid(self, sid: str) -> List[Dict[str, Any]]:
        """Busca empleado por SID (método de compatibilidad)"""
        return self.buscar_empleado(sid=sid)
    
    def actualizar_proceso(self, numero_caso: str, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualiza un proceso por número de caso (método de compatibilidad)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Mapear campos de la UI a campos de la base de datos
            mapeo_campos = {
                'status': 'status',
                'mail': 'mail',
                'closing_date_app': 'closing_date_app',
                'app_quality': 'app_quality',
                'confirmation_by_user': 'confirmation_by_user',
                'comment': 'comment'
            }
            
            campos = []
            valores = []
            for campo_ui, valor in datos.items():
                if campo_ui in mapeo_campos and valor is not None:
                    campo_bd = mapeo_campos[campo_ui]
                    campos.append(f"{campo_bd} = ?")
                    valores.append(valor)
            
            if not campos:
                return False, "No hay campos para actualizar"
            
            # Actualizar fecha de actualización
            campos.append('fecha_actualizacion = ?')
            valores.append('CURRENT_TIMESTAMP')
            
            query = f"UPDATE procesos SET {', '.join(campos)} WHERE numero_caso = ?"
            valores.append(numero_caso)
            
            cursor.execute(query, valores)
            conn.commit()
            conn.close()
            
            if cursor.rowcount > 0:
                return True, "Proceso actualizado exitosamente"
            else:
                return False, "No se encontró el proceso para actualizar"
                
        except Exception as e:
            return False, f"Error actualizando proceso: {str(e)}"
    
    def obtener_estadisticas(self) -> Dict[str, int]:
        """Obtiene estadísticas básicas (método de compatibilidad)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Contar empleados
            cursor.execute('SELECT COUNT(*) FROM empleados')
            total_empleados = cursor.fetchone()[0]
            
            # Contar procesos
            cursor.execute('SELECT COUNT(*) FROM procesos')
            total_procesos = cursor.fetchone()[0]
            
            # Contar empleados activos
            cursor.execute('SELECT COUNT(*) FROM empleados WHERE estado = "Activo"')
            empleados_activos = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_empleados': total_empleados,
                'total_procesos': total_procesos,
                'empleados_activos': empleados_activos
            }
        except Exception:
            return {'total_empleados': 0, 'total_procesos': 0, 'empleados_activos': 0}
