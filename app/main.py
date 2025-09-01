"""
Aplicación principal del sistema de conciliación de accesos
Integra con la UI existente de Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.bindings import ReconciliationBindings
from db.schema import init_database


class ReconciliationApp:
    """Aplicación principal que integra el sistema de conciliación con tu UI existente"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Conciliación de Accesos")
        self.root.geometry("1400x800")
        
        # Inicializar base de datos
        try:
            init_database()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
            messagebox.showerror("Error", f"Error inicializando base de datos: {e}")
        
        # Crear variables de control
        self._crear_variables()
        
        # Crear interfaz
        self._crear_interfaz()
        
        # Inicializar bindings de conciliación
        self._inicializar_conciliacion()
    
    def _crear_variables(self):
        """Crea las variables de control para la interfaz"""
        self.variables = {
            'sid': tk.StringVar(),
            'subunit': tk.StringVar(),
            'cargo': tk.StringVar(),
            'ingresado_por': tk.StringVar(),
            'status': tk.StringVar(value="Pendiente"),
            'comment': tk.StringVar()
        }
    
    def _crear_interfaz(self):
        """Crea la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="🔍 Sistema de Conciliación de Accesos", 
                          font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de entrada de datos
        self._crear_seccion_entrada(main_frame)
        
        # Sección de botones de conciliación
        self._crear_seccion_botones(main_frame)
        
        # Sección de resultados
        self._crear_seccion_resultados(main_frame)
        
        # Sección de historial
        self._crear_seccion_historial(main_frame)
    
    def _crear_seccion_entrada(self, parent):
        """Crea la sección de entrada de datos"""
        entrada_frame = ttk.LabelFrame(parent, text="Datos de Conciliación", padding="15")
        entrada_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        entrada_frame.columnconfigure(1, weight=1)
        entrada_frame.columnconfigure(3, weight=1)
        
        # SID
        ttk.Label(entrada_frame, text="SID:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        ttk.Entry(entrada_frame, textvariable=self.variables['sid'], width=20).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Sub Unidad
        ttk.Label(entrada_frame, text="Sub Unidad:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(0, 10))
        ttk.Entry(entrada_frame, textvariable=self.variables['subunit'], width=20).grid(
            row=0, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Cargo
        ttk.Label(entrada_frame, text="Cargo:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        ttk.Entry(entrada_frame, textvariable=self.variables['cargo'], width=20).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Ingresado Por
        ttk.Label(entrada_frame, text="Ingresado Por:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(0, 10))
        ttk.Entry(entrada_frame, textvariable=self.variables['ingresado_por'], width=20).grid(
            row=1, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Status
        ttk.Label(entrada_frame, text="Status:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        status_combo = ttk.Combobox(entrada_frame, textvariable=self.variables['status'], 
                                   values=["Pendiente", "En Proceso", "Completado", "Rechazado"], 
                                   width=17, state="readonly")
        status_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Comentarios
        ttk.Label(entrada_frame, text="Comentarios:").grid(row=2, column=2, sticky=tk.W, pady=5, padx=(0, 10))
        ttk.Entry(entrada_frame, textvariable=self.variables['comment'], width=20).grid(
            row=2, column=3, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
    
    def _crear_seccion_botones(self, parent):
        """Crea la sección de botones de conciliación"""
        botones_frame = ttk.LabelFrame(parent, text="Acciones de Conciliación", padding="15")
        botones_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        
        # Los botones se crearán en _inicializar_conciliacion
        self.botones_frame = botones_frame
    
    def _crear_seccion_resultados(self, parent):
        """Crea la sección de resultados de conciliación"""
        resultados_frame = ttk.LabelFrame(parent, text="Resultados de Conciliación", padding="15")
        resultados_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 20))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Crear Treeview para resultados
        self.tree = ttk.Treeview(resultados_frame, columns=('Tipo', 'App', 'Rol', 'Acción', 'Motivo', 'Estado'), 
                                show='tree headings', height=10)
        
        # Configurar columnas
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Tipo', width=100, anchor=tk.W)
        self.tree.column('App', width=150, anchor=tk.W)
        self.tree.column('Rol', width=100, anchor=tk.W)
        self.tree.column('Acción', width=80, anchor=tk.CENTER)
        self.tree.column('Motivo', width=200, anchor=tk.W)
        self.tree.column('Estado', width=100, anchor=tk.CENTER)
        
        # Configurar encabezados
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('Tipo', text='Tipo', anchor=tk.W)
        self.tree.heading('App', text='Aplicación', anchor=tk.W)
        self.tree.heading('Rol', text='Rol', anchor=tk.W)
        self.tree.heading('Acción', text='Acción', anchor=tk.CENTER)
        self.tree.heading('Motivo', text='Motivo', anchor=tk.W)
        self.tree.heading('Estado', text='Estado', anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar widgets
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
    
    def _crear_seccion_historial(self, parent):
        """Crea la sección de historial de accesos"""
        historial_frame = ttk.LabelFrame(parent, text="Historial de Accesos", padding="15")
        historial_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 20))
        historial_frame.columnconfigure(0, weight=1)
        historial_frame.rowconfigure(0, weight=1)
        
        # Frame para controles del historial
        controles_frame = ttk.Frame(historial_frame)
        controles_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(controles_frame, text="🔄 Actualizar Historial", 
                  command=self._actualizar_historial).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controles_frame, text="📊 Exportar Historial", 
                  command=self._exportar_historial).pack(side=tk.LEFT)
        
        # Treeview para historial
        self.historial_tree = ttk.Treeview(historial_frame, 
                                          columns=('SID', 'App', 'Rol', 'Tipo', 'Fecha', 'Status', 'Comentario'),
                                          show='tree headings', height=8)
        
        # Configurar columnas del historial
        self.historial_tree.column('#0', width=0, stretch=tk.NO)
        self.historial_tree.column('SID', width=100, anchor=tk.W)
        self.historial_tree.column('App', width=150, anchor=tk.W)
        self.historial_tree.column('Rol', width=100, anchor=tk.W)
        self.historial_tree.column('Tipo', width=100, anchor=tk.CENTER)
        self.historial_tree.column('Fecha', width=150, anchor=tk.W)
        self.historial_tree.column('Status', width=100, anchor=tk.CENTER)
        self.historial_tree.column('Comentario', width=200, anchor=tk.W)
        
        # Configurar encabezados del historial
        self.historial_tree.heading('#0', text='', anchor=tk.W)
        self.historial_tree.heading('SID', text='SID', anchor=tk.W)
        self.historial_tree.heading('App', text='Aplicación', anchor=tk.W)
        self.historial_tree.heading('Rol', text='Rol', anchor=tk.W)
        self.historial_tree.heading('Tipo', text='Tipo', anchor=tk.CENTER)
        self.historial_tree.heading('Fecha', text='Fecha', anchor=tk.W)
        self.historial_tree.heading('Status', text='Status', anchor=tk.CENTER)
        self.historial_tree.heading('Comentario', text='Comentario', anchor=tk.W)
        
        # Scrollbar para historial
        historial_scrollbar = ttk.Scrollbar(historial_frame, orient="vertical", command=self.historial_tree.yview)
        self.historial_tree.configure(yscrollcommand=historial_scrollbar.set)
        
        # Posicionar widgets del historial
        self.historial_tree.grid(row=1, column=0, sticky="nsew")
        historial_scrollbar.grid(row=1, column=1, sticky="ns")
    
    def _inicializar_conciliacion(self):
        """Inicializa el sistema de conciliación y conecta los botones"""
        try:
            # Crear instancia de bindings
            self.reconciliation_bindings = ReconciliationBindings(self.root)
            
            # Crear botones de conciliación
            botones = self.reconciliation_bindings.bind_reconciliation_buttons(
                sid_var=self.variables['sid'],
                subunit_var=self.variables['subunit'],
                cargo_var=self.variables['cargo'],
                ingresado_por_var=self.variables['ingresado_por'],
                status_var=self.variables['status'],
                comment_var=self.variables['comment'],
                tree_widget=self.tree
            )
            
            # Posicionar botones en el frame
            botones['conciliar'].grid(row=0, column=0, padx=(0, 10), pady=5)
            botones['exportar'].grid(row=0, column=1, padx=(0, 10), pady=5)
            botones['registrar'].grid(row=0, column=2, padx=(0, 10), pady=5)
            botones['conciliar_todos'].grid(row=0, column=3, padx=(0, 10), pady=5)
            botones['limpiar'].grid(row=0, column=4, padx=(0, 10), pady=5)
            
            # Cargar historial inicial
            self._actualizar_historial()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error inicializando conciliación: {e}")
            print(f"Error inicializando conciliación: {e}")
    
    def _actualizar_historial(self):
        """Actualiza el historial de accesos"""
        try:
            # Limpiar historial anterior
            for item in self.historial_tree.get_children():
                self.historial_tree.delete(item)
            
            # Obtener historial reciente
            historial = self.reconciliation_bindings.get_access_history(limit=50)
            
            # Poblar historial
            for item in historial:
                self.historial_tree.insert("", "end", values=(
                    item.get('sid', ''),
                    item.get('app_name', ''),
                    item.get('role_name', ''),
                    item.get('tipo', ''),
                    item.get('record_date', '')[:19] if item.get('record_date') else '',  # Truncar timestamp
                    item.get('status', ''),
                    item.get('comment', '')
                ))
            
        except Exception as e:
            print(f"Error actualizando historial: {e}")
    
    def _exportar_historial(self):
        """Exporta el historial de accesos a Excel"""
        try:
            historial = self.reconciliation_bindings.get_access_history(limit=1000)  # Más registros para exportación
            
            if not historial:
                messagebox.showwarning("Advertencia", "No hay datos de historial para exportar")
                return
            
            # Importar aquí para evitar dependencias circulares
            from services.export_service import export_service
            
            filepath = export_service.export_access_history(historial)
            
            messagebox.showinfo(
                "Exportación Exitosa", 
                f"Historial exportado a Excel:\n{filepath}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando historial: {e}")
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error en la aplicación: {e}")
            messagebox.showerror("Error Fatal", f"Error en la aplicación: {e}")


def main():
    """Función principal"""
    try:
        app = ReconciliationApp()
        app.run()
    except Exception as e:
        print(f"Error iniciando aplicación: {e}")
        messagebox.showerror("Error", f"Error iniciando aplicación: {e}")


if __name__ == "__main__":
    main()

