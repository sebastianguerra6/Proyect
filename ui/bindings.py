"""
Bindings para conectar la UI existente con los servicios de conciliación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
import threading
from datetime import datetime

from services.reconcile_service import reconciliation_service
from services.export_service import export_service
from services.history_service import history_service
from db.schema import init_database


class ReconciliationBindings:
    """Clase que conecta la UI existente con los servicios de conciliación"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.current_reconciliation_data = None
        self.is_processing = False
        
        # Inicializar base de datos
        try:
            init_database()
        except Exception as e:
            print(f"Advertencia: Error inicializando BD: {e}")
    
    def bind_reconciliation_buttons(self, 
                                  sid_var: tk.StringVar,
                                  subunit_var: tk.StringVar,
                                  cargo_var: tk.StringVar,
                                  ingresado_por_var: tk.StringVar,
                                  status_var: tk.StringVar,
                                  comment_var: tk.StringVar,
                                  tree_widget: ttk.Treeview) -> Dict[str, Any]:
        """
        Crea y conecta los botones de conciliación con la UI existente
        
        Args:
            sid_var: Variable StringVar para el SID
            subunit_var: Variable StringVar para la subunidad
            cargo_var: Variable StringVar para el cargo
            ingresado_por_var: Variable StringVar para quien ingresa
            status_var: Variable StringVar para el status
            comment_var: Variable StringVar para comentarios
            tree_widget: Widget Treeview para mostrar resultados
            
        Returns:
            Dict con los botones creados para que puedas posicionarlos
        """
        self.sid_var = sid_var
        self.subunit_var = subunit_var
        self.cargo_var = cargo_var
        self.ingresado_por_var = ingresado_por_var
        self.status_var = status_var
        self.comment_var = comment_var
        self.tree = tree_widget
        
        # Crear botones de conciliación
        buttons = {}
        
        # Botón "Conciliar Accesos" (por SID)
        buttons['conciliar'] = ttk.Button(
            self.parent,
            text="🔍 Conciliar Accesos",
            command=self._conciliar_accesos_por_sid,
            style="Info.TButton"
        )
        
        # Botón "Exportar Excel"
        buttons['exportar'] = ttk.Button(
            self.parent,
            text="📊 Exportar Excel",
            command=self._exportar_excel,
            style="Success.TButton"
        )
        
        # Botón "Registrar Tickets"
        buttons['registrar'] = ttk.Button(
            self.parent,
            text="📝 Registrar Tickets",
            command=self._registrar_tickets,
            style="Warning.TButton"
        )
        
        # Botón "Conciliar Todos" (opcional)
        buttons['conciliar_todos'] = ttk.Button(
            self.parent,
            text="🌐 Conciliar Todos",
            command=self._conciliar_todos,
            style="Info.TButton"
        )
        
        # Botón "Limpiar Resultados"
        buttons['limpiar'] = ttk.Button(
            self.parent,
            text="🧹 Limpiar Resultados",
            command=self._limpiar_resultados,
            style="Danger.TButton"
        )
        
        return buttons
    
    def _conciliar_accesos_por_sid(self):
        """Concilia los accesos de una persona específica por SID"""
        if self.is_processing:
            messagebox.showwarning("Advertencia", "Ya hay una operación en proceso")
            return
        
        sid = self.sid_var.get().strip()
        if not sid:
            messagebox.showwarning("Advertencia", "Por favor ingrese un SID")
            return
        
        # Deshabilitar botones durante el procesamiento
        self._set_processing_state(True)
        
        # Ejecutar en hilo separado para no bloquear la UI
        thread = threading.Thread(target=self._execute_reconciliation, args=(sid,))
        thread.daemon = True
        thread.start()
    
    def _execute_reconciliation(self, sid: str):
        """Ejecuta la conciliación en un hilo separado"""
        try:
            # Realizar conciliación
            result = reconciliation_service.reconcile_person(sid)
            
            # Actualizar UI en el hilo principal
            self.parent.after(0, lambda: self._show_reconciliation_results(result))
            
        except Exception as e:
            error_msg = f"Error en conciliación: {str(e)}"
            self.parent.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            self.parent.after(0, lambda: self._set_processing_state(False))
    
    def _show_reconciliation_results(self, result: Dict[str, Any]):
        """Muestra los resultados de la conciliación en el Treeview"""
        try:
            # Limpiar resultados anteriores
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if "error" in result:
                messagebox.showerror("Error", result["error"])
                return
            
            # Guardar datos para uso posterior
            self.current_reconciliation_data = result
            
            # Mostrar resumen
            current_count = len(result.get("current", []))
            target_count = len(result.get("target", []))
            to_grant_count = len(result.get("to_grant", []))
            to_revoke_count = len(result.get("to_revoke", []))
            
            summary_msg = f"Conciliación completada para SID: {result.get('person_info', {}).get('sid', 'N/A')}\n"
            summary_msg += f"Accesos actuales: {current_count}\n"
            summary_msg += f"Accesos objetivo: {target_count}\n"
            summary_msg += f"A otorgar: {to_grant_count}\n"
            summary_msg += f"A revocar: {to_revoke_count}"
            
            messagebox.showinfo("Conciliación Completada", summary_msg)
            
            # Mostrar resultados en el Treeview
            self._populate_tree_with_reconciliation(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando resultados: {str(e)}")
    
    def _populate_tree_with_reconciliation(self, result: Dict[str, Any]):
        """Puebla el Treeview con los resultados de conciliación"""
        try:
            # Configurar columnas del Treeview si no están configuradas
            if not self.tree['columns']:
                self.tree['columns'] = ('Tipo', 'App', 'Rol', 'Acción', 'Motivo', 'Estado')
                self.tree.column('#0', width=0, stretch=tk.NO)
                self.tree.column('Tipo', width=100, anchor=tk.W)
                self.tree.column('App', width=150, anchor=tk.W)
                self.tree.column('Rol', width=100, anchor=tk.W)
                self.tree.column('Acción', width=80, anchor=tk.CENTER)
                self.tree.column('Motivo', width=200, anchor=tk.W)
                self.tree.column('Estado', width=100, anchor=tk.CENTER)
                
                self.tree.heading('#0', text='', anchor=tk.W)
                self.tree.heading('Tipo', text='Tipo', anchor=tk.W)
                self.tree.heading('App', text='Aplicación', anchor=tk.W)
                self.tree.heading('Rol', text='Rol', anchor=tk.W)
                self.tree.heading('Acción', text='Acción', anchor=tk.CENTER)
                self.tree.heading('Motivo', text='Motivo', anchor=tk.W)
                self.tree.heading('Estado', text='Estado', anchor=tk.CENTER)
            
            # Agregar accesos actuales
            for access in result.get("current", []):
                self.tree.insert("", "end", values=(
                    "Actual",
                    access.get("app_name", ""),
                    access.get("role_name", ""),
                    "MANTENER",
                    "Acceso activo",
                    "Activo"
                ), tags=("current",))
            
            # Agregar accesos objetivo
            for access in result.get("target", []):
                self.tree.insert("", "end", values=(
                    "Objetivo",
                    access.get("app_name", ""),
                    access.get("role_name", ""),
                    "OBJETIVO",
                    "Según matriz de autorizaciones",
                    "Objetivo"
                ), tags=("target",))
            
            # Agregar accesos a otorgar
            for access in result.get("to_grant", []):
                self.tree.insert("", "end", values=(
                    "A Otorgar",
                    access.get("app_name", ""),
                    access.get("role_name", ""),
                    "GRANT",
                    access.get("motivo", ""),
                    "Pendiente"
                ), tags=("to_grant",))
            
            # Agregar accesos a revocar
            for access in result.get("to_revoke", []):
                self.tree.insert("", "end", values=(
                    "A Revocar",
                    access.get("app_name", ""),
                    access.get("role_name", ""),
                    "REVOKE",
                    access.get("motivo", ""),
                    "Pendiente"
                ), tags=("to_revoke",))
            
            # Aplicar colores a las filas - Cambiados a tonos de rojo
            self.tree.tag_configure("current", background="#ffebee")
            self.tree.tag_configure("target", background="#ffcdd2")
            self.tree.tag_configure("to_grant", background="#ffcdd2")
            self.tree.tag_configure("to_revoke", background="#ffebee")
            
        except Exception as e:
            print(f"Error poblando Treeview: {e}")
    
    def _exportar_excel(self):
        """Exporta los resultados de conciliación a Excel"""
        if not self.current_reconciliation_data:
            messagebox.showwarning("Advertencia", "No hay datos de conciliación para exportar")
            return
        
        try:
            # Obtener valores de las variables
            ingresado_por = self.ingresado_por_var.get().strip() or "Sistema"
            status = self.status_var.get().strip() or "Pendiente"
            comment = self.comment_var.get().strip()
            
            # Exportar a Excel
            filepath = export_service.export_single_person_tickets(
                self.current_reconciliation_data,
                ingresado_por,
                status,
                comment
            )
            
            messagebox.showinfo(
                "Exportación Exitosa", 
                f"Archivo Excel generado:\n{filepath}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando a Excel: {str(e)}")
    
    def _registrar_tickets(self):
        """Registra los tickets de conciliación en el historial"""
        if not self.current_reconciliation_data:
            messagebox.showwarning("Advertencia", "No hay datos de conciliación para registrar")
            return
        
        try:
            # Obtener valores de las variables
            ingresado_por = self.ingresado_por_var.get().strip() or "Sistema"
            status = self.status_var.get().strip() or "Pendiente"
            comment = self.comment_var.get().strip()
            
            # Registrar tickets
            result = history_service.register_reconciliation_tickets(
                self.current_reconciliation_data,
                ingresado_por,
                status,
                comment
            )
            
            if result["success"]:
                messagebox.showinfo(
                    "Tickets Registrados",
                    f"Se registraron {result['tickets_created']} tickets exitosamente.\n"
                    f"Se omitieron {result['tickets_skipped']} tickets duplicados."
                )
                
                # Actualizar estado en el Treeview
                self._update_tree_status_after_registration()
                
                # Limpiar datos actuales
                self.current_reconciliation_data = None
            else:
                messagebox.showerror("Error", f"Error registrando tickets: {result['error']}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error registrando tickets: {str(e)}")
    
    def _update_tree_status_after_registration(self):
        """Actualiza el estado de las filas en el Treeview después del registro"""
        try:
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                if values and len(values) >= 6:
                    accion = values[3]
                    if accion in ["GRANT", "REVOKE"]:
                        # Actualizar estado a "Registrado"
                        new_values = list(values)
                        new_values[5] = "Registrado"
                        self.tree.item(item, values=tuple(new_values))
                        
                        # Cambiar color a rojo
                        self.tree.item(item, tags=("registered",))
            
            # Configurar color para tickets registrados
            self.tree.tag_configure("registered", background="#ffcdd2")
            
        except Exception as e:
            print(f"Error actualizando estado del Treeview: {e}")
    
    def _conciliar_todos(self):
        """Concilia los accesos de todas las personas en el sistema"""
        if self.is_processing:
            messagebox.showwarning("Advertencia", "Ya hay una operación en proceso")
            return
        
        # Confirmar operación
        if not messagebox.askyesno(
            "Confirmar Conciliación Masiva",
            "¿Está seguro de que desea conciliar todos los accesos del sistema?\n"
            "Esta operación puede tomar varios minutos."
        ):
            return
        
        # Deshabilitar botones durante el procesamiento
        self._set_processing_state(True)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._execute_reconciliation_all)
        thread.daemon = True
        thread.start()
    
    def _execute_reconciliation_all(self):
        """Ejecuta la conciliación masiva en un hilo separado"""
        try:
            # Realizar conciliación masiva
            results = reconciliation_service.reconcile_all()
            
            # Actualizar UI en el hilo principal
            self.parent.after(0, lambda: self._show_bulk_reconciliation_results(results))
            
        except Exception as e:
            error_msg = f"Error en conciliación masiva: {str(e)}"
            self.parent.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            self.parent.after(0, lambda: self._set_processing_state(False))
    
    def _show_bulk_reconciliation_results(self, results: list):
        """Muestra los resultados de la conciliación masiva"""
        try:
            # Contar totales
            total_persons = len(results)
            total_to_grant = 0
            total_to_revoke = 0
            errors = 0
            
            for result in results:
                if "error" not in result:
                    total_to_grant += len(result.get("to_grant", []))
                    total_to_revoke += len(result.get("to_revoke", []))
                else:
                    errors += 1
            
            # Mostrar resumen
            summary_msg = f"Conciliación masiva completada:\n"
            summary_msg += f"Total de personas procesadas: {total_persons}\n"
            summary_msg += f"Total de accesos a otorgar: {total_to_grant}\n"
            summary_msg += f"Total de accesos a revocar: {total_to_revoke}\n"
            summary_msg += f"Errores encontrados: {errors}"
            
            messagebox.showinfo("Conciliación Masiva Completada", summary_msg)
            
            # Guardar resultados para exportación
            self.current_reconciliation_data = results
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando resultados masivos: {str(e)}")
    
    def _limpiar_resultados(self):
        """Limpia los resultados mostrados en el Treeview"""
        try:
            # Limpiar Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Limpiar datos de conciliación
            self.current_reconciliation_data = None
            
            messagebox.showinfo("Información", "Resultados limpiados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error limpiando resultados: {str(e)}")
    
    def _set_processing_state(self, is_processing: bool):
        """Establece el estado de procesamiento y habilita/deshabilita botones"""
        self.is_processing = is_processing
        
        # Aquí podrías deshabilitar/habilitar botones si los tienes como atributos
        # Por ahora solo actualizamos el estado interno
    
    def get_reconciliation_summary(self, sid: str = None) -> Dict[str, Any]:
        """Obtiene un resumen de la conciliación"""
        try:
            return reconciliation_service.get_reconciliation_summary(sid)
        except Exception as e:
            return {"error": f"Error obteniendo resumen: {str(e)}"}
    
    def get_access_history(self, sid: str = None, limit: int = 100) -> list:
        """Obtiene el historial de accesos"""
        try:
            if sid:
                return history_service.get_recent_tickets(sid, limit)
            else:
                return history_service.get_recent_tickets(limit=limit)
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []

