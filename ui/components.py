import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox

class CamposGeneralesFrame:
    """Componente para los campos generales del empleado"""
    
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            'sid': tk.StringVar(),
            'nueva_sub_unidad': tk.StringVar(),
            'nuevo_cargo': tk.StringVar(),
            'request_date': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'ingreso_por': tk.StringVar(),
            'fecha': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'status': tk.StringVar(value="Pendiente")
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.LabelFrame(self.parent, text="Información de Gestión de Proyectos", padding="20")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(1, weight=1)  # Cambiar a weight=1 para que se expanda
        
        # Centrar el contenido
        main_container = ttk.Frame(self.frame)
        main_container.grid(row=0, column=1, sticky="ew", padx=20)  # Aumentar padx de 15 a 20
        main_container.columnconfigure(1, weight=1)
        
        # Campos
        campos = [
            ("SID:", "sid", "entry"),
            ("Nueva Sub Unidad:", "nueva_sub_unidad", "combobox", [
                "Sub Unidad 1 - Desarrollo Frontend",
                "Sub Unidad 2 - Desarrollo Backend", 
                "Sub Unidad 3 - DevOps e Infraestructura",
                "Sub Unidad 4 - QA y Testing",
                "Sub Unidad 5 - Diseño UX/UI",
                "Sub Unidad 6 - Gestión de Proyectos",
                "Sub Unidad 7 - Soporte Técnico"
            ]),
            ("Nuevo Cargo:", "nuevo_cargo", "entry"),
            ("Request Date:", "request_date", "entry"),
            ("Quien hace el ingreso:", "ingreso_por", "combobox", ["Juan Pérez", "María García"]),
            ("Fecha:", "fecha", "entry"),
            ("Status:", "status", "combobox", ["Pendiente", "En Proceso", "Completado", "Cancelado", "Rechazado"])
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(main_container, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 15))
            
            if tipo == "entry":
                ttk.Entry(main_container, textvariable=self.variables[var_name], width=50).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(main_container, textvariable=self.variables[var_name], 
                            values=valores, width=47).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
        
        # Información del número de caso (solo informativo)
        info_frame = ttk.Frame(main_container)
        info_frame.grid(row=len(campos), column=0, columnspan=2, pady=(15, 0), sticky="ew")
        
        ttk.Label(info_frame, text="Nota: El número de caso se generará automáticamente al guardar", 
                  style="Normal.TLabel", foreground="gray").pack(anchor=tk.CENTER)
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")
        self.variables['request_date'].set(datetime.now().strftime("%Y-%m-%d"))
        self.variables['fecha'].set(datetime.now().strftime("%Y-%m-%d"))
        self.variables['status'].set("Pendiente")
    
    def validar_campos_obligatorios(self):
        """Valida que los campos obligatorios estén completos"""
        campos_obligatorios = ['sid', 'nueva_sub_unidad', 'nuevo_cargo', 'status']
        campos_vacios = []
        
        for campo in campos_obligatorios:
            if not self.variables[campo].get().strip():
                campos_vacios.append(campo)
        
        return campos_vacios

class OnboardingFrame:
    """Componente para la pestaña de onboarding"""
    
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            'submenu_onboarding': tk.StringVar(),
            'other_onboarding': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Centrar el contenido
        main_container = ttk.Frame(self.frame)
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Aumentar padx de 15 a 20
        main_container.columnconfigure(0, weight=1)
        
        # Título
        ttk.Label(main_container, text="Tipo de Onboarding", 
                  style="Section.TLabel").pack(pady=(0, 20))
        
        # Frame para radio buttons
        radio_frame = ttk.Frame(main_container)
        radio_frame.pack(fill=tk.BOTH, expand=True)
        
        # Submenú con radio buttons
        opciones_submenu = ["Nuevo Empleado", "Recontratación", "Transferencia Interna", "Promoción"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(radio_frame, text=opcion, 
                           variable=self.variables['submenu_onboarding'], 
                           value=opcion).pack(anchor=tk.CENTER, pady=8)
        
        # Opción Other con campo de texto
        other_frame = ttk.Frame(radio_frame)
        other_frame.pack(anchor=tk.CENTER, pady=8)
        
        ttk.Radiobutton(other_frame, text="Other:", 
                       variable=self.variables['submenu_onboarding'], 
                       value="other").pack(side=tk.LEFT)
        
        ttk.Entry(other_frame, textvariable=self.variables['other_onboarding'], 
                 width=35).pack(side=tk.LEFT, padx=(5, 0))  # Aumentar width de 30 a 35
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        datos = {name: var.get() for name, var in self.variables.items()}
        
        # Si se seleccionó "other", usar el valor del campo de texto
        if datos['submenu_onboarding'] == 'other':
            datos['submenu_onboarding'] = datos['other_onboarding']
        
        return datos
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")

class OffboardingFrame:
    """Componente para la pestaña de offboarding"""
    
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            'submenu_offboarding': tk.StringVar(),
            'other_offboarding': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Centrar el contenido
        main_container = ttk.Frame(self.frame)
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Aumentar padx de 15 a 20
        main_container.columnconfigure(0, weight=1)
        
        # Título
        ttk.Label(main_container, text="Tipo de Offboarding", 
                  style="Section.TLabel").pack(pady=(0, 20))
        
        # Frame para radio buttons
        radio_frame = ttk.Frame(main_container)
        radio_frame.pack(fill=tk.BOTH, expand=True)
        
        # Submenú con radio buttons
        opciones_submenu = ["Salida Definitiva", "Reducción de Personal", "Fin de Proyecto", "Cambio de Empresa"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(radio_frame, text=opcion, 
                           variable=self.variables['submenu_offboarding'], 
                           value=opcion).pack(anchor=tk.CENTER, pady=8)
        
        # Opción Other con campo de texto
        other_frame = ttk.Frame(radio_frame)
        other_frame.pack(anchor=tk.CENTER, pady=8)
        
        ttk.Radiobutton(other_frame, text="Other:", 
                       variable=self.variables['submenu_offboarding'], 
                       value="other").pack(side=tk.LEFT)
        
        ttk.Entry(other_frame, textvariable=self.variables['other_offboarding'], 
                 width=35).pack(side=tk.LEFT, padx=(5, 0))  # Aumentar width de 30 a 35
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        datos = {name: var.get() for name, var in self.variables.items()}
        
        # Si se seleccionó "other", usar el valor del campo de texto
        if datos['submenu_offboarding'] == 'other':
            datos['submenu_offboarding'] = datos['other_offboarding']
        
        return datos
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")

class LateralMovementFrame:
    """Componente para la pestaña de lateral movement"""
    
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            'submenu_lateral': tk.StringVar(),
            'other_lateral': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Centrar el contenido
        main_container = ttk.Frame(self.frame)
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Aumentar padx de 15 a 20
        main_container.columnconfigure(1, weight=1)
        
        # Título
        ttk.Label(main_container, text="Información de Lateral Movement", 
                  style="Section.TLabel").pack(pady=(0, 20))
        
        # Frame para campos
        campos_frame = ttk.Frame(main_container)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        campos_frame.columnconfigure(1, weight=1)
        
        # Título para radio buttons
        ttk.Label(campos_frame, text="Tipo de Movimiento:", style="Subsection.TLabel").grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Submenú con radio buttons
        opciones_submenu = ["Movimiento Horizontal", "Reasignación de Proyecto", "Cambio de Equipo", "Rotación de Funciones"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(campos_frame, text=opcion, 
                           variable=self.variables['submenu_lateral'], 
                           value=opcion).grid(row=1+i, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Opción Other con campo de texto
        other_row = 1 + len(opciones_submenu)
        other_frame = ttk.Frame(campos_frame)
        other_frame.grid(row=other_row, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Radiobutton(other_frame, text="Other:", 
                       variable=self.variables['submenu_lateral'], 
                       value="other").pack(side=tk.LEFT)
        
        ttk.Entry(other_frame, textvariable=self.variables['other_lateral'], 
                 width=35).pack(side=tk.LEFT, padx=(5, 0))  # Aumentar width de 30 a 35
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        datos = {name: var.get() for name, var in self.variables.items()}
        
        # Si se seleccionó "other", usar el valor del campo de texto
        if datos['submenu_lateral'] == 'other':
            datos['submenu_lateral'] = datos['other_lateral']
        
        return datos
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")

class EdicionBusquedaFrame:
    """Componente para la pestaña de edición y búsqueda de registros"""
    
    def __init__(self, parent, service=None):
        self.parent = parent
        self.service = service
        self.variables = {}
        self.registros_encontrados = []
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            'numero_caso_busqueda': tk.StringVar(),
            'numero_caso_edicion': tk.StringVar(),
            'nueva_sub_unidad_edicion': tk.StringVar(),
            'nuevo_cargo_edicion': tk.StringVar(),
            'request_date_edicion': tk.StringVar(),
            'ingreso_por_edicion': tk.StringVar(),
            'fecha_edicion': tk.StringVar(),
            'status_edicion': tk.StringVar(),
            'mail_edicion': tk.StringVar(),
            'closing_date_app_edicion': tk.StringVar(),
            'app_quality_edicion': tk.StringVar(),
            'confirmation_by_user_edicion': tk.StringVar(),
            'comment_edicion': tk.StringVar(),
            'filtro_texto': tk.StringVar(),
            'columna_filtro': tk.StringVar(value="SID")
        }
        
        # Variables para filtros múltiples
        self.filtros_activos = {}
        self.campos_filtro = {
            "SID": "sid",
            "Número de Caso": "numero_caso", 
            "Proceso": "proceso",
            "Aplicación": "aplicacion",
            "Estado": "estado",
            "Fecha": "fecha",
            "Responsable": "responsable",
            "Descripción": "descripcion"
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz simplificada"""
        self.frame = ttk.Frame(self.parent)
        
        # Configurar grid del frame principal
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Título
        ttk.Label(self.frame, text="🔍 Edición y Búsqueda - Historial de Procesos", 
                  style="Title.TLabel").grid(row=0, column=0, pady=20, sticky="ew")
        
        # Frame principal simplificado
        main_frame = ttk.Frame(self.frame)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Cambiar de row 1 a row 3 para la tabla
        
        # Frame para búsqueda y herramientas
        busqueda_frame = ttk.LabelFrame(main_frame, text="📊 Historial de Procesos y Asignaciones", padding="15")
        busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        busqueda_frame.columnconfigure(1, weight=1)
        
        # Barra de herramientas para la tabla
        toolbar_frame = ttk.Frame(busqueda_frame)
        toolbar_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        
        # Botones de edición
        ttk.Button(toolbar_frame, text="✏️ Editar Registro", command=self.editar_registro_historial, 
                  style="Info.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="🗑️ Eliminar", command=self.eliminar_registro, 
                  style="Danger.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de estadísticas
        ttk.Button(toolbar_frame, text="📊 Ver Estadísticas", command=self.mostrar_estadisticas, 
                  style="Success.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="📤 Exportar Excel", command=self.exportar_estadisticas, 
                  style="Warning.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botón para crear registro manual
        ttk.Button(toolbar_frame, text="➕ Registro Manual", command=self.crear_registro_manual, 
                  style="Info.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de actualizar y mostrar todos
        ttk.Button(toolbar_frame, text="🔄 Actualizar", command=self.actualizar_tabla).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="📋 Mostrar Todo el Historial", 
                  command=self.mostrar_todo_el_historial).pack(side=tk.LEFT, padx=(0, 10))
        
        # Panel de filtros múltiples
        self._crear_panel_filtros(busqueda_frame)
        
        # Tabla de resultados - Actualizada para mostrar historial
        resultados_frame = ttk.Frame(busqueda_frame)
        resultados_frame.grid(row=3, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        
        # Crear Treeview para mostrar resultados del historial
        self.tree = ttk.Treeview(resultados_frame, columns=("SID", "Caso", "Proceso", "Aplicación", "Estado", "Fecha", "Fecha Solicitud", "Responsable", "Descripción"), 
                                show="headings", height=12)
        
        # Configurar columnas
        self.tree.heading("SID", text="SID")
        self.tree.heading("Caso", text="Caso")
        self.tree.heading("Proceso", text="Proceso")
        self.tree.heading("Aplicación", text="Aplicación")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Fecha Solicitud", text="Fecha Solicitud")
        self.tree.heading("Responsable", text="Responsable")
        self.tree.heading("Descripción", text="Descripción")
        
        # Configurar anchos de columna
        self.tree.column("SID", width=100)
        self.tree.column("Caso", width=120)
        self.tree.column("Proceso", width=120)
        self.tree.column("Aplicación", width=150)
        self.tree.column("Estado", width=100)
        self.tree.column("Fecha", width=120)
        self.tree.column("Fecha Solicitud", width=120)
        self.tree.column("Responsable", width=120)
        self.tree.column("Descripción", width=200)
        
        # Scrollbar para la tabla
        tree_scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar grid para que la tabla se expanda
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Eventos de la tabla
        self.tree.bind('<Double-1>', self._on_doble_clic)
        self.tree.bind('<Delete>', lambda e: self.eliminar_registro())
        
        # Inicializar filtro delay
        self.filtro_delay_id = None
    
    def _on_doble_clic(self, event):
        """Maneja el doble clic en la tabla"""
        self.editar_registro_historial()
    
    def actualizar_tabla(self):
        """Actualiza la tabla con todos los registros del historial"""
        try:
            # Limpiar tabla primero
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener todos los registros del historial
            self.mostrar_todo_el_historial()
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Actualización", "Tabla actualizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando tabla: {str(e)}")
    
    
    def editar_registro_historial(self):
        """Edita el registro del historial seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro para editar")
            return
        
        try:
            # Obtener el registro seleccionado
            item = selection[0]
            values = self.tree.item(item, 'values')
            
            # Ahora los valores son: SID, Caso, Proceso, Aplicación, Estado, Fecha, Responsable, Descripción
            scotia_id = values[0]  # SID
            case_id = values[1]    # Caso
            process_access = values[2]  # Proceso
            app_access_name = values[3]  # Aplicación
            
            # Buscar los datos completos del registro del historial
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            # Obtener el registro completo del historial usando una combinación de campos
            conn = access_service.get_connection()
            cursor = conn.cursor()
            
            # Debug: imprimir los valores que estamos buscando
            print(f"DEBUG: Buscando registro con SID: {scotia_id}, Caso: {case_id}, Proceso: {process_access}")
            
            cursor.execute('''
                SELECT * FROM historico 
                WHERE scotia_id = ? AND case_id = ? AND process_access = ? AND app_access_name = ?
            ''', (scotia_id, case_id, process_access, app_access_name))
            row = cursor.fetchone()
            
            # Debug: imprimir si se encontró algo
            print(f"DEBUG: Registro encontrado: {row is not None}")
            
            if not row:
                conn.close()
                messagebox.showerror("Error", f"No se encontró el registro del historial con SID: {scotia_id}, Caso: {case_id}")
                return
            
            # Convertir a diccionario
            columns = [description[0] for description in cursor.description]
            historial_data = dict(zip(columns, row))
            conn.close()
            
            print(f"DEBUG: Datos del historial: {historial_data}")
            
            # Crear diálogo de edición del historial
            dialog = HistorialDialog(self.parent, f"Editar Registro de Historial - SID: {scotia_id}", historial_data)
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                success, message = self.actualizar_registro_historial_por_campos(scotia_id, case_id, process_access, app_access_name, dialog.result)
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    # Actualizar la tabla después de editar
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", message)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error editando registro: {str(e)}")
            print(f"Error en editar_registro_historial: {e}")
    
    def actualizar_registro_historial_por_campos(self, scotia_id, case_id, process_access, app_access_name, data):
        """Actualiza un registro del historial usando una combinación de campos para identificarlo"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            conn = access_service.get_connection()
            cursor = conn.cursor()
            
            # Construir query de actualización
            set_clauses = []
            params = []
            
            for campo, valor in data.items():
                if campo not in ['scotia_id', 'case_id', 'process_access', 'app_access_name']:  # No actualizar los campos de identificación
                    set_clauses.append(f"{campo} = ?")
                    params.append(valor)
            
            if not set_clauses:
                return False, "No hay datos para actualizar"
            
            # Agregar los campos de identificación al WHERE
            where_clause = "scotia_id = ? AND case_id = ? AND process_access = ? AND app_access_name = ?"
            params.extend([scotia_id, case_id, process_access, app_access_name])
            
            query = f"UPDATE historico SET {', '.join(set_clauses)} WHERE {where_clause}"
            
            print(f"DEBUG: Query de actualización: {query}")
            print(f"DEBUG: Parámetros: {params}")
            
            cursor.execute(query, params)
            
            if cursor.rowcount == 0:
                conn.close()
                return False, f"Registro con SID {scotia_id}, Caso {case_id} no encontrado"
            
            conn.commit()
            conn.close()
            
            return True, f"Registro actualizado exitosamente"
            
        except Exception as e:
            return False, f"Error actualizando registro: {str(e)}"
    
    def eliminar_registro(self):
        """Elimina el registro seleccionado del historial"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro para eliminar")
            return
        
        # Obtener datos del registro seleccionado
        item = self.tree.item(selection[0])
        values = item['values']
        
        if len(values) < 3:
            messagebox.showerror("Error", "Datos de registro no válidos")
            return
        
        scotia_id = values[0]
        case_id = values[1]
        app_name = values[3]
        
        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar este registro?\n\n"
            f"SID: {scotia_id}\n"
            f"Caso: {case_id}\n"
            f"Aplicación: {app_name}\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if result:
            try:
                # Eliminar el registro del historial pasando también el app_name para ser específico
                success, message = self._eliminar_registro_historico(scotia_id, case_id, app_name)
                
                if success:
                    messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                    # Actualizar la tabla refrescando desde la base de datos
                    self.mostrar_todo_el_historial()
                else:
                    messagebox.showerror("Error", f"Error al eliminar registro: {message}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def _eliminar_registro_historico(self, scotia_id, case_id, app_name=None):
        """Elimina un registro específico del historial"""
        try:
            if not self.service:
                return False, "Servicio no disponible"
            
            # Usar el servicio para eliminar el registro específico
            success = self.service.delete_historical_record(scotia_id, case_id, app_name)
            
            if success:
                return True, "Registro eliminado exitosamente"
            else:
                return False, "No se pudo eliminar el registro"
            
        except Exception as e:
            return False, f"Error eliminando registro: {str(e)}"
    
    def mostrar_resultados_busqueda(self, resultados, busqueda=""):
        """Muestra los resultados de búsqueda en la tabla"""
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for i, resultado in enumerate(resultados):
                if i < 2:  # Debug para los primeros 2 registros
                    print(f"DEBUG: Insertando registro {i}:")
                    print(f"  scotia_id: {resultado.get('scotia_id', '')}")
                    print(f"  employee: {resultado.get('employee', '')}")
                    print(f"  unit: {resultado.get('unit', '')}")
                    print(f"  position: {resultado.get('position', '')}")
                    print(f"  activo: {resultado.get('activo', True)}")
                    print(f"  start_date: {resultado.get('start_date', '')}")
                    print(f"  email: {resultado.get('email', '')}")
                
                # Mapear los campos correctos de la base de datos headcount
                values = (
                    resultado.get('scotia_id', ''),  # Caso
                    resultado.get('employee', ''),   # SID (usando employee como nombre)
                    resultado.get('unit', ''),       # Sub Unidad
                    resultado.get('position', ''),   # Cargo
                    'Activo' if resultado.get('activo', True) else 'Inactivo',  # Status
                    resultado.get('start_date', ''), # Request Date
                    resultado.get('email', '')       # Mail
                )
                
                if i < 2:  # Debug para los primeros 2 registros
                    print(f"  Valores a insertar: {values}")
                
                self.tree.insert("", "end", values=values)
        else:
            messagebox.showinfo("Búsqueda", "No se encontraron registros")
    
    def buscar_por_numero_caso(self):
        """Busca registros por número de caso usando la base de datos"""
        numero_caso = self.variables['numero_caso_busqueda'].get().strip()
        if not numero_caso:
            messagebox.showwarning("Advertencia", "Por favor ingrese un número de caso para buscar")
            return
        
        try:
            if self.service and hasattr(self.service, 'buscar_procesos'):
                # Buscar en la base de datos
                filtros = {'numero_caso': numero_caso}
                resultados = self.service.buscar_procesos(filtros)
                self.mostrar_resultados_busqueda(resultados, f"número de caso: {numero_caso}")
            else:
                messagebox.showerror("Error", "Servicio no disponible para búsqueda")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
            print(f"Error en buscar_por_numero_caso: {e}")
    
    def _crear_panel_filtros(self, parent):
        """Crea el panel de filtros múltiples"""
        # Frame para filtros
        filtros_frame = ttk.LabelFrame(parent, text="Filtros Múltiples", padding="10")
        filtros_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(15, 0))
        filtros_frame.columnconfigure(1, weight=1)
        
        # Lista de filtros activos
        ttk.Label(filtros_frame, text="Filtros Activos:").grid(row=0, column=0, sticky="w", pady=5)
        self.filtros_listbox = tk.Listbox(filtros_frame, height=3)
        self.filtros_listbox.grid(row=0, column=1, sticky="ew", padx=(10, 5), pady=5)
        
        # Scrollbar para la lista
        scrollbar_filtros = ttk.Scrollbar(filtros_frame, orient="vertical", command=self.filtros_listbox.yview)
        scrollbar_filtros.grid(row=0, column=2, sticky="ns")
        self.filtros_listbox.configure(yscrollcommand=scrollbar_filtros.set)
        
        # Botones para gestionar filtros
        botones_filtros = ttk.Frame(filtros_frame)
        botones_filtros.grid(row=0, column=3, padx=(5, 0), pady=5)
        
        ttk.Button(botones_filtros, text="Eliminar", command=self._eliminar_filtro_seleccionado).pack(side=tk.TOP, pady=2)
        ttk.Button(botones_filtros, text="Limpiar", command=self._limpiar_todos_filtros).pack(side=tk.TOP, pady=2)
        
        # Frame para agregar nuevo filtro
        nuevo_filtro_frame = ttk.Frame(filtros_frame)
        nuevo_filtro_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        nuevo_filtro_frame.columnconfigure(1, weight=1)
        
        # Campo de texto para el valor del filtro
        ttk.Label(nuevo_filtro_frame, text="Valor:").grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        self.entry_filtro = ttk.Entry(nuevo_filtro_frame, width=30)
        self.entry_filtro.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5)
        
        # Combo para seleccionar campo
        ttk.Label(nuevo_filtro_frame, text="Campo:").grid(row=0, column=2, padx=(0, 5), pady=5, sticky="w")
        self.combo_campo = ttk.Combobox(nuevo_filtro_frame, values=list(self.campos_filtro.keys()), width=15)
        self.combo_campo.grid(row=0, column=3, padx=(0, 10), pady=5)
        
        # Botón para agregar filtro
        ttk.Button(nuevo_filtro_frame, text="Agregar Filtro", command=self._agregar_filtro).grid(row=0, column=4, padx=(0, 5), pady=5)
        
        # Botones de acción
        botones_accion = ttk.Frame(filtros_frame)
        botones_accion.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(botones_accion, text="Aplicar Filtros", command=self._aplicar_filtros_multiples).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botones_accion, text="Mostrar Todos", command=self.mostrar_todo_el_historial).pack(side=tk.LEFT)
        
        # Bind para Enter en el campo de texto
        self.entry_filtro.bind('<Return>', lambda e: self._agregar_filtro())
    
    def _agregar_filtro(self):
        """Agrega un nuevo filtro a la lista"""
        valor = self.entry_filtro.get().strip()
        campo = self.combo_campo.get()
        
        if not valor:
            messagebox.showwarning("Advertencia", "Por favor ingrese un valor para el filtro")
            return
        
        if not campo:
            messagebox.showwarning("Advertencia", "Por favor seleccione un campo para filtrar")
            return
        
        # Agregar filtro al diccionario
        campo_bd = self.campos_filtro.get(campo)
        if campo_bd:
            self.filtros_activos[campo] = valor
            self._actualizar_lista_filtros()
            
            # Limpiar campos
            self.entry_filtro.delete(0, tk.END)
            self.combo_campo.set("")
    
    def _eliminar_filtro_seleccionado(self):
        """Elimina el filtro seleccionado de la lista"""
        seleccion = self.filtros_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            campo = list(self.filtros_activos.keys())[indice]
            del self.filtros_activos[campo]
            self._actualizar_lista_filtros()
    
    def _limpiar_todos_filtros(self):
        """Limpia todos los filtros activos"""
        self.filtros_activos.clear()
        self._actualizar_lista_filtros()
    
    def _actualizar_lista_filtros(self):
        """Actualiza la lista visual de filtros activos"""
        self.filtros_listbox.delete(0, tk.END)
        for campo, valor in self.filtros_activos.items():
            self.filtros_listbox.insert(tk.END, f"{campo}: {valor}")
    
    def _aplicar_filtros_multiples(self):
        """Aplica todos los filtros activos"""
        if not self.filtros_activos:
            messagebox.showwarning("Advertencia", "No hay filtros activos para aplicar")
            return
        
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            # Obtener todos los registros del historial
            todos_resultados = access_service.buscar_procesos({})
            
            # Aplicar filtros múltiples
            resultados_filtrados = self._aplicar_filtros_en_memoria(todos_resultados)
            
            # Mostrar resultados
            if resultados_filtrados:
                mensaje = f"Se encontraron {len(resultados_filtrados)} registros con los filtros aplicados"
                self.mostrar_resultados_historial(resultados_filtrados, mensaje)
            else:
                messagebox.showinfo("Filtros", "No se encontraron registros que coincidan con los filtros aplicados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error aplicando filtros: {str(e)}")
    
    def _aplicar_filtros_en_memoria(self, resultados):
        """Aplica los filtros activos a los resultados en memoria"""
        if not resultados:
            return resultados
        
        resultados_filtrados = []
        for resultado in resultados:
            cumple_filtros = True
            
            for campo_ui, valor_filtro in self.filtros_activos.items():
                campo_bd = self.campos_filtro.get(campo_ui)
                if campo_bd:
                    valor_campo = str(resultado.get(campo_bd, '')).lower()
                    if valor_filtro.lower() not in valor_campo:
                        cumple_filtros = False
                        break
            
            if cumple_filtros:
                resultados_filtrados.append(resultado)
        
        return resultados_filtrados
    
    def mostrar_todo_el_historial(self):
        """Muestra todo el historial de procesos"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            # Obtener todo el historial usando el método del servicio
            conn = access_service.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT h.*, a.logical_access_name, a.description as app_description
                FROM historico h
                LEFT JOIN (
                    SELECT 
                        logical_access_name,
                        description,
                        ROW_NUMBER() OVER (PARTITION BY logical_access_name ORDER BY id) as rn
                    FROM applications
                ) a ON h.app_access_name = a.logical_access_name AND a.rn = 1
                ORDER BY h.record_date DESC
            ''')
            rows = cursor.fetchall()
            conn.close()
            
            # Convertir a diccionarios
            columns = [description[0] for description in cursor.description]
            historial = [dict(zip(columns, row)) for row in rows]
            
            print(f"DEBUG: Historial obtenido: {len(historial)} registros")
            
            # Analizar registros de lateral movement para debug
            lateral_records = [r for r in historial if r.get('event_description') and 'lateral movement' in r.get('event_description', '')]
            onboarding_count = len([r for r in lateral_records if r.get('process_access') == 'onboarding'])
            offboarding_count = len([r for r in lateral_records if r.get('process_access') == 'offboarding'])
            
            print(f"DEBUG: Registros de lateral movement: {len(lateral_records)} (Onboarding: {onboarding_count}, Offboarding: {offboarding_count})")
            
            self.mostrar_resultados_historial(historial, "")
            
            # Mostrar información de debug al usuario
            if lateral_records:
                messagebox.showinfo("Información de Debug", 
                    f"Se encontraron {len(lateral_records)} registros de lateral movement:\n"
                    f"• Onboarding: {onboarding_count}\n"
                    f"• Offboarding: {offboarding_count}\n\n"
                    f"Si no ves todos los registros, verifica:\n"
                    f"1. Filtros activos en la interfaz\n"
                    f"2. Búsqueda por SID específico\n"
                    f"3. Scroll en la tabla")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo historial: {str(e)}")
            print(f"Error completo: {e}")
    
    def crear_datos_ejemplo_historial(self, conn, cursor):
        """Crea datos de ejemplo en la tabla historico si está vacía"""
        try:
            # Insertar algunos registros de ejemplo
            datos_ejemplo = [
                {
                    'scotia_id': 'S001',
                    'case_id': 'CASE-20241201-001',
                    'responsible': 'Admin',
                    'record_date': '2024-12-01 10:00:00',
                    'process_access': 'onboarding',
                    'sid': 'S001',
                    'area': 'Tecnología',
                    'subunit': 'Desarrollo',
                    'event_description': 'Acceso requerido para sistema de desarrollo',
                    'ticket_email': 'admin@empresa.com',
                    'app_access_name': 'Sistema Desarrollo',
                    'computer_system_type': 'Desktop',
                    'status': 'Pendiente',
                    'general_status': 'En Proceso'
                },
                {
                    'scotia_id': 'S002',
                    'case_id': 'CASE-20241201-002',
                    'responsible': 'Admin',
                    'record_date': '2024-12-01 11:00:00',
                    'process_access': 'offboarding',
                    'sid': 'S002',
                    'area': 'Tecnología',
                    'subunit': 'QA',
                    'event_description': 'Revocación de acceso para sistema de testing',
                    'ticket_email': 'admin@empresa.com',
                    'app_access_name': 'Sistema Testing',
                    'computer_system_type': 'Desktop',
                    'status': 'Completado',
                    'general_status': 'Completado'
                }
            ]
            
            for dato in datos_ejemplo:
                cursor.execute('''
                    INSERT INTO historico 
                    (scotia_id, case_id, responsible, record_date, process_access, sid, area, subunit,
                     event_description, ticket_email, app_access_name, computer_system_type, status, general_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    dato['scotia_id'], dato['case_id'], dato['responsible'], dato['record_date'],
                    dato['process_access'], dato['sid'], dato['area'], dato['subunit'],
                    dato['event_description'], dato['ticket_email'], dato['app_access_name'],
                    dato['computer_system_type'], dato['status'], dato['general_status']
                ))
            
            print("DEBUG: Datos de ejemplo creados en historico")
            
        except Exception as e:
            print(f"Error creando datos de ejemplo: {e}")
    
    def mostrar_resultados_historial(self, resultados, busqueda=""):
        """Muestra los resultados del historial en la tabla"""
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        print(f"DEBUG: Mostrando {len(resultados) if resultados else 0} resultados del historial")
        
        if resultados:
            for i, resultado in enumerate(resultados):
                # Debug: imprimir los primeros 3 registros
                if i < 3:
                    print(f"DEBUG: Registro {i}: {resultado}")
                
                # Formatear fecha
                fecha = resultado.get('record_date', '')
                try:
                    from datetime import datetime
                    fecha_formatted = datetime.fromisoformat(fecha).strftime('%d/%m/%Y %H:%M') if fecha else 'N/A'
                except:
                    fecha_formatted = fecha or 'N/A'
                
                # Formatear fecha de solicitud
                request_fecha = resultado.get('request_date', '')
                try:
                    from datetime import datetime
                    request_fecha_formatted = datetime.fromisoformat(request_fecha).strftime('%d/%m/%Y') if request_fecha else 'N/A'
                except:
                    request_fecha_formatted = request_fecha or 'N/A'
                
                # Mapear los campos del historial
                values = (
                    resultado.get('scotia_id', ''),             # SID
                    resultado.get('case_id', ''),               # Caso
                    resultado.get('process_access', ''),        # Proceso
                    resultado.get('app_access_name', ''),       # Aplicación
                    resultado.get('status', ''),                # Estado
                    fecha_formatted,                            # Fecha
                    request_fecha_formatted,                    # Fecha Solicitud
                    resultado.get('responsible', ''),           # Responsable
                    resultado.get('event_description', '')      # Descripción
                )
                
                if i < 3:  # Debug para los primeros 3 registros
                    print(f"DEBUG: Valores a insertar: {values}")
                
                self.tree.insert("", "end", values=values)
            
            if busqueda and busqueda.strip():
                messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} registros para: {busqueda}")
        else:
            if busqueda and busqueda.strip():
                messagebox.showinfo("Búsqueda", f"No se encontraron registros para: {busqueda}")
            elif busqueda == "":
                # Solo mostrar mensaje si no hay resultados y no es una búsqueda específica
                pass
            else:
                messagebox.showinfo("Búsqueda", "No se encontraron registros")
    
    def mostrar_resultados_busqueda(self, resultados, busqueda=""):
        """Muestra los resultados de búsqueda en el treeview"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                # Extraer valores del resultado de la base de datos real
                valores = (
                    resultado.get('case_id', ''),
                    resultado.get('sid', ''),
                    resultado.get('scotia_id', ''),
                    resultado.get('process_access', ''),
                    resultado.get('status', ''),
                    resultado.get('record_date', ''),
                    resultado.get('responsible', ''),
                    resultado.get('area', ''),
                    resultado.get('subunit', ''),
                    resultado.get('event_description', ''),
                    resultado.get('ticket_email', ''),
                    resultado.get('app_access_name', ''),
                    resultado.get('closing_date_app', ''),
                    resultado.get('app_quality', ''),
                    resultado.get('confirmation_by_user', ''),
                    resultado.get('comment', '')
                )
                self.tree.insert("", "end", values=valores)
            
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} registros para: {busqueda}")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron registros para: {busqueda}")
    
    def buscar_todos_los_registros(self):
        """Busca todos los registros en la base de datos"""
        try:
            # Buscar todos los registros del historial
            self.mostrar_todo_el_historial()
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
    
    def aplicar_filtro(self):
        """Aplica un filtro por texto en la columna seleccionada"""
        texto_filtro = self.variables['filtro_texto'].get().strip()
        columna = self.variables['columna_filtro'].get()
        
        if not texto_filtro:
            messagebox.showwarning("Advertencia", "Por favor ingrese texto para filtrar")
            return
        
        try:
            if self.service and hasattr(self.service, 'buscar_procesos'):
                # Mapear nombres de columnas a campos de la base de datos
                mapeo_columnas = {
                    "SID": "sid",
                    "Sub Unidad": "nueva_sub_unidad",
                    "Cargo": "nuevo_cargo",
                    "Status": "status",
                    "Request Date": "request_date",
                    "Ingreso Por": "ingreso_por",
                    "Tipo": "tipo_proceso",
                    "APP Name": "app_name",
                    "Mail": "mail",
                    "App Quality": "app_quality",
                    "Confirmation by User": "confirmation_by_user",
                    "Comment": "comment"
                }
                
                campo_bd = mapeo_columnas.get(columna, "sid")
                
                # Crear filtro para la búsqueda
                filtros = {campo_bd: texto_filtro}
                resultados = self.service.buscar_procesos(filtros)
                
                # Aplicar filtro adicional en memoria si es necesario
                if resultados:
                    resultados_filtrados = []
                    for resultado in resultados:
                        valor_campo = str(resultado.get(campo_bd, '')).lower()
                        if texto_filtro.lower() in valor_campo:
                            resultados_filtrados.append(resultado)
                    resultados = resultados_filtrados
                
                # Mostrar resultados con mensaje de confirmación
                self.mostrar_resultados_busqueda(resultados, f"filtro '{texto_filtro}' en columna '{columna}'")
            else:
                messagebox.showerror("Error", "Servicio no disponible para búsqueda")
        except Exception as e:
            messagebox.showerror("Error", f"Error aplicando filtro: {str(e)}")
            print(f"Error en aplicar_filtro: {e}")
    
    def limpiar_filtro(self):
        """Limpia el filtro y muestra todos los registros"""
        self.variables['filtro_texto'].set("")
        self.variables['columna_filtro'].set("SID")
        self.buscar_todos_los_registros()
    
    def _on_filtro_change(self, event):
        """Maneja el cambio en el campo de filtro para filtrado en tiempo real"""
        # Cancelar el delay anterior si existe
        if self.filtro_delay_id:
            self.parent.after_cancel(self.filtro_delay_id)
        
        # Programar nuevo filtrado con delay de 500ms
        self.filtro_delay_id = self.parent.after(500, self._aplicar_filtro_tiempo_real)
    
    def _aplicar_filtro_tiempo_real(self):
        """Aplica el filtro en tiempo real sin mostrar mensajes"""
        texto_filtro = self.variables['filtro_texto'].get().strip()
        columna = self.variables['columna_filtro'].get()
        
        if not texto_filtro:
            # Si no hay texto, mostrar todos los registros
            self.buscar_todos_los_registros()
            return
        
        try:
            if self.service and hasattr(self.service, 'buscar_procesos'):
                # Mapear nombres de columnas a campos de la base de datos
                mapeo_columnas = {
                    "SID": "sid",
                    "Sub Unidad": "nueva_sub_unidad",
                    "Cargo": "nuevo_cargo",
                    "Status": "status",
                    "Request Date": "request_date",
                    "Ingreso Por": "ingreso_por",
                    "Tipo": "tipo_proceso",
                    "APP Name": "app_name",
                    "Mail": "mail",
                    "App Quality": "app_quality",
                    "Confirmation by User": "confirmation_by_user",
                    "Comment": "comment"
                }
                
                campo_bd = mapeo_columnas.get(columna, "sid")
                
                # Crear filtro para la búsqueda
                filtros = {campo_bd: texto_filtro}
                resultados = self.service.buscar_procesos(filtros)
                
                # Aplicar filtro adicional en memoria si es necesario
                if resultados:
                    resultados_filtrados = []
                    for resultado in resultados:
                        valor_campo = str(resultado.get(campo_bd, '')).lower()
                        if texto_filtro.lower() in valor_campo:
                            resultados_filtrados.append(resultado)
                    resultados = resultados_filtrados
                
                # Mostrar resultados sin mensaje de confirmación
                self._mostrar_resultados_sin_mensaje(resultados)
            else:
                print("Servicio no disponible para filtrado en tiempo real")
        except Exception as e:
            print(f"Error en filtrado en tiempo real: {e}")
    
    def _mostrar_resultados_sin_mensaje(self, resultados):
        """Muestra los resultados sin mostrar mensajes de confirmación"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                # Extraer valores del resultado de la base de datos
                valores = (
                    resultado.get('numero_caso', ''),
                    resultado.get('sid', ''),
                    resultado.get('nueva_sub_unidad', ''),
                    resultado.get('nuevo_cargo', ''),
                    resultado.get('status', ''),
                    resultado.get('request_date', ''),
                    resultado.get('ingreso_por', ''),
                    resultado.get('tipo_proceso', ''),
                    resultado.get('app_name', ''),
                    resultado.get('mail', ''),
                    resultado.get('closing_date_app', ''),
                    resultado.get('app_quality', ''),
                    resultado.get('confirmation_by_user', ''),
                    resultado.get('comment', '')
                )
                self.tree.insert("", "end", values=valores)
    
    
    def seleccionar_registro(self, event):
        """Maneja la selección de un registro en el treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            valores = item['values']
            
            # Cargar valores en los campos de edición
            if len(valores) >= 14:  # Ahora tenemos 14 columnas
                # Campos básicos
                self.variables['numero_caso_edicion'].set(valores[0])
                self.variables['nueva_sub_unidad_edicion'].set(valores[2])
                self.variables['nuevo_cargo_edicion'].set(valores[3])
                self.variables['status_edicion'].set(valores[4])
                self.variables['request_date_edicion'].set(valores[5])
                self.variables['ingreso_por_edicion'].set(valores[6])
                
                # Campos adicionales
                self.variables['mail_edicion'].set(valores[9] if valores[9] else '')
                self.variables['closing_date_app_edicion'].set(valores[10] if valores[10] else '')
                self.variables['app_quality_edicion'].set(valores[11] if valores[11] else '')
                self.variables['confirmation_by_user_edicion'].set(valores[12] if valores[12] else '')
                self.variables['comment_edicion'].set(valores[13] if valores[13] else '')
    
    def guardar_cambios(self):
        """Guarda los cambios realizados en los campos"""
        try:
            numero_caso = self.variables['numero_caso_edicion'].get().strip()
            if not numero_caso:
                messagebox.showwarning("Advertencia", "Por favor seleccione un registro para editar")
                return
            
            # Preparar datos para actualizar
            datos_actualizados = {
                'status': self.variables['status_edicion'].get(),
                'mail': self.variables['mail_edicion'].get(),
                'closing_date_app': self.variables['closing_date_app_edicion'].get(),
                'app_quality': self.variables['app_quality_edicion'].get(),
                'confirmation_by_user': self.variables['confirmation_by_user_edicion'].get(),
                'comment': self.variables['comment_edicion'].get()
            }
            
            # Filtrar campos vacíos
            datos_actualizados = {k: v for k, v in datos_actualizados.items() if v.strip()}
            
            if not datos_actualizados:
                messagebox.showwarning("Advertencia", "No hay cambios para guardar")
                return
            
            # Guardar cambios usando el servicio
            if self.service and hasattr(self.service, 'actualizar_proceso'):
                exito, mensaje = self.service.actualizar_proceso(numero_caso, datos_actualizados)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    # Limpiar campos de edición
                    self.limpiar_campos_edicion()
                    # Refrescar la búsqueda actual
                    self.refrescar_busqueda_actual()
                else:
                    messagebox.showerror("Error", mensaje)
            else:
                messagebox.showerror("Error", "Servicio no disponible para actualizar")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando cambios: {str(e)}")
            print(f"Error en guardar_cambios: {e}")
    
    def limpiar_campos_edicion(self):
        """Limpia solo los campos de edición"""
        campos_edicion = [
            'mail_edicion', 'closing_date_app_edicion', 'app_quality_edicion',
            'confirmation_by_user_edicion', 'comment_edicion'
        ]
        for campo in campos_edicion:
            if campo in self.variables:
                self.variables[campo].set("")
    
    def refrescar_busqueda_actual(self):
        """Refresca la búsqueda actual para mostrar los cambios"""
        # Si hay un SID en búsqueda, refrescar esa búsqueda
        sid = self.variables['sid_busqueda'].get().strip()
        if sid:
            self.buscar_por_sid()
        else:
            # Si no hay búsqueda específica, mostrar todos los registros
            self.buscar_todos_los_registros()
    
    def obtener_datos(self):
        """Obtiene los datos de los campos de edición"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")
        
        # Limpiar resultados de búsqueda
        for item in self.tree.get_children():
            self.tree.delete(item)

    def mostrar_estadisticas(self):
        """Muestra las estadísticas del historial en una ventana"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            # Obtener estadísticas
            stats = access_service.get_historial_statistics()
            
            if "error" in stats:
                messagebox.showerror("Error", stats["error"])
                return
            
            # Crear ventana de estadísticas
            stats_window = tk.Toplevel(self.frame)
            stats_window.title("📊 Estadísticas del Historial")
            stats_window.geometry("800x600")
            stats_window.transient(self.frame)
            stats_window.grab_set()
            
            # Frame principal con scroll
            main_frame = ttk.Frame(stats_window)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Canvas para scroll
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Título
            ttk.Label(scrollable_frame, text="📊 Estadísticas del Historial", 
                     font=("Arial", 16, "bold")).pack(pady=(0, 20))
            
            # Estadísticas generales
            if 'generales' in stats:
                generales = stats['generales']
                ttk.Label(scrollable_frame, text="📈 Resumen General", 
                         font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
                
                generales_text = f"""
Total de Registros: {generales.get('total_registros', 0)}
Completados: {generales.get('completados', 0)}
Pendientes: {generales.get('pendientes', 0)}
En Proceso: {generales.get('en_proceso', 0)}
Cancelados: {generales.get('cancelados', 0)}
Rechazados: {generales.get('rechazados', 0)}
Empleados Únicos: {generales.get('empleados_unicos', 0)}
Aplicaciones Únicas: {generales.get('aplicaciones_unicas', 0)}
                """
                ttk.Label(scrollable_frame, text=generales_text, 
                         font=("Arial", 10)).pack(anchor="w", pady=(0, 20))
            
            # Estadísticas por unidad
            if 'por_unidad' in stats and stats['por_unidad']:
                ttk.Label(scrollable_frame, text="🏢 Por Unidad", 
                         font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
                
                # Crear tabla para unidades
                unidad_frame = ttk.Frame(scrollable_frame)
                unidad_frame.pack(fill=tk.X, pady=(0, 20))
                
                # Headers
                headers = ["Unidad", "Total", "Completados", "Pendientes", "En Proceso", "Cancelados", "Rechazados"]
                for i, header in enumerate(headers):
                    ttk.Label(unidad_frame, text=header, font=("Arial", 10, "bold")).grid(
                        row=0, column=i, padx=5, pady=2, sticky="w")
                
                # Datos
                for row_idx, unidad in enumerate(stats['por_unidad'][:10]):  # Mostrar solo top 10
                    ttk.Label(unidad_frame, text=unidad.get('unidad', '')[:20]).grid(
                        row=row_idx+1, column=0, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('total_registros', 0))).grid(
                        row=row_idx+1, column=1, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('completados', 0))).grid(
                        row=row_idx+1, column=2, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('pendientes', 0))).grid(
                        row=row_idx+1, column=3, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('en_proceso', 0))).grid(
                        row=row_idx+1, column=4, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('cancelados', 0))).grid(
                        row=row_idx+1, column=5, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('rechazados', 0))).grid(
                        row=row_idx+1, column=6, padx=5, pady=1, sticky="w")
            
            # Botón de cerrar
            ttk.Button(scrollable_frame, text="Cerrar", command=stats_window.destroy).pack(pady=20)
            
            # Configurar scroll
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando estadísticas: {str(e)}")

    def exportar_estadisticas(self):
        """Exporta las estadísticas del historial a Excel"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            from export_service import export_service
            
            # Obtener estadísticas
            stats = access_service.get_historial_statistics()
            
            if "error" in stats:
                messagebox.showerror("Error", stats["error"])
                return
            
            # Exportar a Excel
            filepath = export_service.export_historial_statistics(stats)
            
            messagebox.showinfo("Éxito", f"Estadísticas exportadas exitosamente a:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando estadísticas: {str(e)}")

    def crear_registro_manual(self):
        """Abre el diálogo para crear un registro manual de acceso"""
        try:
            from ui.manual_access_component import ManualAccessDialog
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            # Abrir diálogo de registro manual
            dialog = ManualAccessDialog(self.frame, access_service)
            self.frame.wait_window(dialog.dialog)
            
            # Si se creó un registro, actualizar la tabla
            if dialog.result:
                self.actualizar_tabla()
                messagebox.showinfo("Éxito", "Registro manual creado exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error abriendo diálogo de registro manual: {str(e)}")

class CreacionPersonaFrame:
    """Componente para la gestión completa de headcount y applications"""
    
    def __init__(self, parent, service=None):
        self.parent = parent
        self.service = service
        self.variables = {}
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            # Campos básicos
            'scotia_id': tk.StringVar(),
            'employee': tk.StringVar(),
            'full_name': tk.StringVar(),
            'email': tk.StringVar(),
            'position': tk.StringVar(),
            'manager': tk.StringVar(),
            'senior_manager': tk.StringVar(),
            'unit': tk.StringVar(),
            'start_date': tk.StringVar(),
            'ceco': tk.StringVar(),
            'skip_level': tk.StringVar(),
            'cafe_alcides': tk.StringVar(),
            'parents': tk.StringVar(),
            'personal_email': tk.StringVar(),
            'size': tk.StringVar(),
            'birthday': tk.StringVar(),
            'validacion': tk.StringVar(),
            'activo': tk.StringVar(value="Activo"),
            'inactivation_date': tk.StringVar(),
            # Campos para filtros
            'filtro_texto': tk.StringVar(),
            'columna_filtro': tk.StringVar(value="scotia_id")
        }
        
        # Variables para filtros múltiples
        self.filtros_activos = {}
        self.campos_filtro = {
            "SID": "scotia_id",
            "Nombre": "full_name",
            "Email": "email",
            "Posición": "position",
            "Manager": "manager",
            "Unidad": "unit",
            "CECO": "ceco",
            "Cafe Alcides": "cafe_alcides",
            "Validación": "validacion"
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz simplificada"""
        self.frame = ttk.Frame(self.parent)
        
        # Configurar grid del frame principal
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Título
        ttk.Label(self.frame, text="Gestión de Personas en Headcount", 
                  style="Title.TLabel").grid(row=0, column=0, pady=20, sticky="ew")
        
        # Frame principal simplificado
        main_frame = ttk.Frame(self.frame)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Cambiar de row 1 a row 3 para la tabla
        
        # Frame para búsqueda y herramientas
        busqueda_frame = ttk.LabelFrame(main_frame, text="Gestión de Personas", padding="15")
        busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        busqueda_frame.columnconfigure(1, weight=1)
        
        # Barra de herramientas para la tabla
        toolbar_frame = ttk.Frame(busqueda_frame)
        toolbar_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        
        # Botones de edición
        ttk.Button(toolbar_frame, text="➕ Nueva Persona", command=self.crear_persona, 
                  style="Success.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="✏️ Editar", command=self.editar_persona, 
                  style="Info.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="🗑️ Eliminar", command=self.eliminar_persona, 
                  style="Danger.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de estadísticas
        ttk.Button(toolbar_frame, text="📊 Ver Estadísticas", command=self.mostrar_estadisticas_headcount, 
                  style="Success.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="📤 Exportar Excel", command=self.exportar_estadisticas_headcount, 
                  style="Warning.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de actualizar y mostrar todos
        ttk.Button(toolbar_frame, text="🔄 Actualizar", command=self.actualizar_tabla).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar_frame, text="📋 Mostrar Todos", 
                  command=self.mostrar_todos).pack(side=tk.LEFT, padx=(0, 10))
        
        # Panel de filtros múltiples
        self._crear_panel_filtros_personas(busqueda_frame)
        
        # Tabla de resultados
        resultados_frame = ttk.Frame(busqueda_frame)
        resultados_frame.grid(row=3, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        
        # Crear Treeview para mostrar resultados
        self.tree = ttk.Treeview(resultados_frame, columns=("SID", "Nombre", "Apellido", "Email", "Departamento", "Cargo", "Estado"), 
                                show="headings", height=12)
        
        # Configurar columnas
        self.tree.heading("SID", text="SID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Departamento", text="Departamento")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Estado", text="Estado")
        
        # Configurar anchos de columna
        self.tree.column("SID", width=100)
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Email", width=200)
        self.tree.column("Departamento", width=150)
        self.tree.column("Cargo", width=150)
        self.tree.column("Estado", width=100)
        
        # Scrollbar para la tabla
        tree_scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar grid para que la tabla se expanda
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Eventos de la tabla
        self.tree.bind('<Double-1>', self._on_doble_clic)
        self.tree.bind('<Delete>', lambda e: self.eliminar_persona())
        
        # Inicializar filtro delay
        self.filtro_delay_id = None
    
    def _crear_panel_filtros_personas(self, parent):
        """Crea el panel de filtros múltiples para personas"""
        # Frame para filtros
        filtros_frame = ttk.LabelFrame(parent, text="Filtros Múltiples", padding="10")
        filtros_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(15, 0))
        filtros_frame.columnconfigure(1, weight=1)
        
        # Lista de filtros activos
        ttk.Label(filtros_frame, text="Filtros Activos:").grid(row=0, column=0, sticky="w", pady=5)
        self.filtros_listbox = tk.Listbox(filtros_frame, height=3)
        self.filtros_listbox.grid(row=0, column=1, sticky="ew", padx=(10, 5), pady=5)
        
        # Scrollbar para la lista
        scrollbar_filtros = ttk.Scrollbar(filtros_frame, orient="vertical", command=self.filtros_listbox.yview)
        scrollbar_filtros.grid(row=0, column=2, sticky="ns")
        self.filtros_listbox.configure(yscrollcommand=scrollbar_filtros.set)
        
        # Botones para gestionar filtros
        botones_filtros = ttk.Frame(filtros_frame)
        botones_filtros.grid(row=0, column=3, padx=(5, 0), pady=5)
        
        ttk.Button(botones_filtros, text="Eliminar", command=self._eliminar_filtro_seleccionado_personas).pack(side=tk.TOP, pady=2)
        ttk.Button(botones_filtros, text="Limpiar", command=self._limpiar_todos_filtros_personas).pack(side=tk.TOP, pady=2)
        
        # Frame para agregar nuevo filtro
        nuevo_filtro_frame = ttk.Frame(filtros_frame)
        nuevo_filtro_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        nuevo_filtro_frame.columnconfigure(1, weight=1)
        
        # Campo de texto para el valor del filtro
        ttk.Label(nuevo_filtro_frame, text="Valor:").grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        self.entry_filtro = ttk.Entry(nuevo_filtro_frame, width=30)
        self.entry_filtro.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5)
        
        # Combo para seleccionar campo
        ttk.Label(nuevo_filtro_frame, text="Campo:").grid(row=0, column=2, padx=(0, 5), pady=5, sticky="w")
        self.combo_campo = ttk.Combobox(nuevo_filtro_frame, values=list(self.campos_filtro.keys()), width=15)
        self.combo_campo.grid(row=0, column=3, padx=(0, 10), pady=5)
        
        # Botón para agregar filtro
        ttk.Button(nuevo_filtro_frame, text="Agregar Filtro", command=self._agregar_filtro_personas).grid(row=0, column=4, padx=(0, 5), pady=5)
        
        # Botones de acción
        botones_accion = ttk.Frame(filtros_frame)
        botones_accion.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(botones_accion, text="Aplicar Filtros", command=self._aplicar_filtros_multiples_personas).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botones_accion, text="Mostrar Todos", command=self.mostrar_todos).pack(side=tk.LEFT)
        
        # Bind para Enter en el campo de texto
        self.entry_filtro.bind('<Return>', lambda e: self._agregar_filtro_personas())
    
    def _agregar_filtro_personas(self):
        """Agrega un nuevo filtro a la lista de personas"""
        valor = self.entry_filtro.get().strip()
        campo = self.combo_campo.get()
        
        if not valor:
            messagebox.showwarning("Advertencia", "Por favor ingrese un valor para el filtro")
            return
        
        if not campo:
            messagebox.showwarning("Advertencia", "Por favor seleccione un campo para filtrar")
            return
        
        # Agregar filtro al diccionario
        campo_bd = self.campos_filtro.get(campo)
        if campo_bd:
            self.filtros_activos[campo] = valor
            self._actualizar_lista_filtros_personas()
            
            # Limpiar campos
            self.entry_filtro.delete(0, tk.END)
            self.combo_campo.set("")
    
    def _eliminar_filtro_seleccionado_personas(self):
        """Elimina el filtro seleccionado de la lista de personas"""
        seleccion = self.filtros_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            campo = list(self.filtros_activos.keys())[indice]
            del self.filtros_activos[campo]
            self._actualizar_lista_filtros_personas()
    
    def _limpiar_todos_filtros_personas(self):
        """Limpia todos los filtros activos de personas"""
        self.filtros_activos.clear()
        self._actualizar_lista_filtros_personas()
    
    def _actualizar_lista_filtros_personas(self):
        """Actualiza la lista visual de filtros activos de personas"""
        self.filtros_listbox.delete(0, tk.END)
        for campo, valor in self.filtros_activos.items():
            self.filtros_listbox.insert(tk.END, f"{campo}: {valor}")
    
    def _aplicar_filtros_multiples_personas(self):
        """Aplica todos los filtros activos para personas"""
        if not self.filtros_activos:
            messagebox.showwarning("Advertencia", "No hay filtros activos para aplicar")
            return
        
        try:
            # Obtener todos los registros del headcount
            todos_resultados = self.service.obtener_todo_headcount()
            
            # Aplicar filtros múltiples
            resultados_filtrados = self._aplicar_filtros_en_memoria_personas(todos_resultados)
            
            # Mostrar resultados
            if resultados_filtrados:
                mensaje = f"Se encontraron {len(resultados_filtrados)} personas con los filtros aplicados"
                self.mostrar_resultados_busqueda(resultados_filtrados, mensaje)
            else:
                messagebox.showinfo("Filtros", "No se encontraron personas que coincidan con los filtros aplicados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error aplicando filtros: {str(e)}")
    
    def _aplicar_filtros_en_memoria_personas(self, resultados):
        """Aplica los filtros activos a los resultados de personas en memoria"""
        if not resultados:
            return resultados
        
        resultados_filtrados = []
        for resultado in resultados:
            cumple_filtros = True
            
            for campo_ui, valor_filtro in self.filtros_activos.items():
                campo_bd = self.campos_filtro.get(campo_ui)
                if campo_bd:
                    valor_campo = str(resultado.get(campo_bd, '')).lower()
                    if valor_filtro.lower() not in valor_campo:
                        cumple_filtros = False
                        break
            
            if cumple_filtros:
                resultados_filtrados.append(resultado)
        
        return resultados_filtrados
    
    def mostrar_todos(self):
        """Muestra todos los registros del headcount"""
        try:
            # Obtener todos los registros de la base de datos real
            resultados = self.service.obtener_todo_headcount()
            self.mostrar_resultados_busqueda(resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo registros: {str(e)}")
    
    def aplicar_filtro(self):
        """Aplica un filtro por texto en la columna seleccionada"""
        texto_filtro = self.variables['filtro_texto'].get().strip()
        columna = self.variables['columna_filtro'].get()
        
        if not texto_filtro:
            messagebox.showwarning("Advertencia", "Por favor ingrese texto para filtrar")
            return
        
        try:
            # Obtener todos los registros de la base de datos real
            todos_resultados = self.service.obtener_todo_headcount()
            
            # Mapear nombres de columnas a campos de la base de datos real
            mapeo_columnas = {
                "SID": "employee",
                "Nombre": "full_name",
                "Email": "email",
                "Posición": "position",
                "Manager": "manager",
                "Unidad": "unit",
                "Estado": "activo"
            }
            
            campo_bd = mapeo_columnas.get(columna, "employee")
            
            # Aplicar filtro en memoria
            if todos_resultados:
                resultados_filtrados = []
                for resultado in todos_resultados:
                    valor_campo = str(resultado.get(campo_bd, '')).lower()
                    if texto_filtro.lower() in valor_campo:
                        resultados_filtrados.append(resultado)
                todos_resultados = resultados_filtrados
            
            self.mostrar_resultados_busqueda(todos_resultados)
            messagebox.showinfo("Filtro", f"Se encontraron {len(todos_resultados)} registros para: filtro '{texto_filtro}' en columna '{columna}'")
        except Exception as e:
            messagebox.showerror("Error", f"Error aplicando filtro: {str(e)}")
            print(f"Error en aplicar_filtro: {e}")
    
    def limpiar_filtro(self):
        """Limpia el filtro y muestra todos los registros"""
        self.variables['filtro_texto'].set("")
        self.variables['columna_filtro'].set("SID")
        self.mostrar_todos()
    
    def _on_filtro_change(self, event):
        """Maneja el cambio en el campo de filtro para filtrado en tiempo real"""
        # Cancelar el delay anterior si existe
        if self.filtro_delay_id:
            self.parent.after_cancel(self.filtro_delay_id)
        
        # Programar nuevo filtrado con delay de 500ms
        self.filtro_delay_id = self.parent.after(500, self._aplicar_filtro_tiempo_real)
    
    def _aplicar_filtro_tiempo_real(self):
        """Aplica el filtro en tiempo real sin mostrar mensajes"""
        texto_filtro = self.variables['filtro_texto'].get().strip()
        columna = self.variables['columna_filtro'].get()
        
        if not texto_filtro:
            # Si no hay texto, mostrar todos los registros
            self.mostrar_todos()
            return
        
        try:
            # Obtener todos los registros de la base de datos real
            todos_resultados = self.service.obtener_todo_headcount()
            
            # Mapear nombres de columnas a campos de la base de datos real
            mapeo_columnas = {
                "SID": "employee",
                "Nombre": "full_name",
                "Email": "email",
                "Posición": "position",
                "Manager": "manager",
                "Unidad": "unit",
                "Estado": "activo"
            }
            
            campo_bd = mapeo_columnas.get(columna, "employee")
            
            # Aplicar filtro en memoria
            if todos_resultados:
                resultados_filtrados = []
                for resultado in todos_resultados:
                    valor_campo = str(resultado.get(campo_bd, '')).lower()
                    if texto_filtro.lower() in valor_campo:
                        resultados_filtrados.append(resultado)
                todos_resultados = resultados_filtrados
            
            # Mostrar resultados sin mensaje de confirmación
            self._mostrar_resultados_sin_mensaje(todos_resultados)
        except Exception as e:
            print(f"Error en filtrado en tiempo real: {e}")
    
    
    def _mostrar_resultados_sin_mensaje(self, resultados):
        """Muestra los resultados sin mostrar mensajes de confirmación"""
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                # Separar nombre y apellido del full_name
                full_name = resultado.get('full_name', '')
                nombre_parts = full_name.split(' ', 1)
                nombre = nombre_parts[0] if nombre_parts else ''
                apellido = nombre_parts[1] if len(nombre_parts) > 1 else ''
                
                self.tree.insert("", "end", values=(
                    resultado.get('scotia_id', ''),  # SID
                    nombre,                          # Nombre
                    apellido,                        # Apellido
                    resultado.get('email', ''),      # Email
                    resultado.get('unit', ''),       # Departamento
                    resultado.get('position', ''),   # Cargo
                    'Activo' if resultado.get('activo', True) else 'Inactivo'  # Estado
                ))
    
    
    
    def crear_persona(self):
        """Crea una nueva persona usando el diálogo de edición"""
        try:
            # Crear diálogo de edición sin datos (para nueva persona)
            dialog = PersonaDialog(self.parent, "Nueva Persona", None)
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
                from access_management_service import access_service
                
                success, message = access_service.create_employee(dialog.result)
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    # Actualizar la tabla después de crear
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", message)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error creando empleado: {str(e)}")
    
    def validar_campos_obligatorios(self):
        """Valida que los campos obligatorios estén completos"""
        campos_obligatorios = ['scotia_id', 'employee', 'full_name', 'email']
        campos_vacios = []
        
        for campo in campos_obligatorios:
            if not self.variables[campo].get().strip():
                campos_vacios.append(campo)
        
        return campos_vacios
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")
        self.variables['activo'].set("Activo")
    
    def actualizar_tabla(self):
        """Actualiza la tabla con todos los registros"""
        try:
            resultados = self.service.obtener_todo_headcount()
            self.mostrar_resultados_busqueda(resultados)
            messagebox.showinfo("Actualización", f"Tabla actualizada. Se encontraron {len(resultados)} registros.")
        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando tabla: {str(e)}")
    
    def _on_doble_clic(self, event):
        """Maneja doble clic en la tabla"""
        self.editar_persona()
    
    def editar_persona(self):
        """Edita la persona seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una persona para editar")
            return
        
        item = self.tree.item(selection[0])
        scotia_id = item['values'][0]
        
        # Buscar la persona en la base de datos
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            persona_data = access_service.get_employee_by_id(scotia_id)
            if not persona_data:
                messagebox.showerror("Error", "No se pudo encontrar la persona seleccionada")
                return
            
            # Crear diálogo de edición
            dialog = PersonaDialog(self.parent, "Editar Persona", persona_data)
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                success, message = access_service.update_employee(scotia_id, dialog.result)
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", message)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error editando persona: {str(e)}")
    
    def eliminar_persona(self):
        """Elimina la persona seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una persona para eliminar")
            return
        
        item = self.tree.item(selection[0])
        scotia_id = item['values'][0]
        nombre = f"{item['values'][1]} {item['values'][2]}"
        
        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar a {nombre} (SID: {scotia_id})?\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if result:
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
                from access_management_service import access_service
                
                success, message = access_service.delete_employee(scotia_id)
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", message)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando persona: {str(e)}")
    
    def mostrar_resultados_busqueda(self, resultados, busqueda=""):
        """Muestra los resultados de búsqueda en la tabla"""
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                # Separar nombre y apellido del full_name
                full_name = resultado.get('full_name', '')
                nombre_parts = full_name.split(' ', 1)
                nombre = nombre_parts[0] if nombre_parts else ''
                apellido = nombre_parts[1] if len(nombre_parts) > 1 else ''
                
                self.tree.insert("", "end", values=(
                    resultado.get('scotia_id', ''),  # SID
                    nombre,                          # Nombre
                    apellido,                        # Apellido
                    resultado.get('email', ''),      # Email
                    resultado.get('unit', ''),       # Departamento
                    resultado.get('position', ''),   # Cargo
                    'Activo' if resultado.get('activo', True) else 'Inactivo'  # Estado
                ))
            
            # Mostrar mensaje de confirmación si se especifica
            if busqueda:
                messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} registros para: {busqueda}")
        else:
            # Mostrar mensaje si no hay resultados
            if busqueda:
                messagebox.showinfo("Búsqueda", f"No se encontraron registros para: {busqueda}")
            else:
                messagebox.showinfo("Búsqueda", "No se encontraron registros")

    def mostrar_estadisticas_headcount(self):
        """Muestra las estadísticas del headcount en una ventana"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            # Obtener estadísticas
            stats = access_service.get_headcount_statistics()
            
            if "error" in stats:
                messagebox.showerror("Error", stats["error"])
                return
            
            # Crear ventana de estadísticas
            stats_window = tk.Toplevel(self.frame)
            stats_window.title("📊 Estadísticas del Headcount")
            stats_window.geometry("900x700")
            stats_window.transient(self.frame)
            stats_window.grab_set()
            
            # Frame principal con scroll
            main_frame = ttk.Frame(stats_window)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Canvas para scroll
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Título
            ttk.Label(scrollable_frame, text="📊 Estadísticas del Headcount", 
                     font=("Arial", 16, "bold")).pack(pady=(0, 20))
            
            # Estadísticas generales
            if 'generales' in stats:
                generales = stats['generales']
                ttk.Label(scrollable_frame, text="📈 Resumen General", 
                         font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
                
                generales_text = f"""
Total de Empleados: {generales.get('total_empleados', 0)}
Activos: {generales.get('activos', 0)}
Inactivos: {generales.get('inactivos', 0)}
Con Posición: {generales.get('con_posicion', 0)}
Con Unidad: {generales.get('con_unidad', 0)}
Con Fecha de Inicio: {generales.get('con_fecha_inicio', 0)}
Con Fecha de Inactivación: {generales.get('con_fecha_inactivacion', 0)}
Unidades Únicas: {generales.get('unidades_unicas', 0)}
Puestos Únicos: {generales.get('puestos_unicos', 0)}
                """
                ttk.Label(scrollable_frame, text=generales_text, 
                         font=("Arial", 10)).pack(anchor="w", pady=(0, 20))
            
            # Estadísticas por unidad
            if 'por_unidad' in stats and stats['por_unidad']:
                ttk.Label(scrollable_frame, text="🏢 Por Unidad", 
                         font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
                
                # Crear tabla para unidades
                unidad_frame = ttk.Frame(scrollable_frame)
                unidad_frame.pack(fill=tk.X, pady=(0, 20))
                
                # Headers
                headers = ["Unidad", "Total", "Activos", "Inactivos", "Con Posición", "Con Fecha Inicio"]
                for i, header in enumerate(headers):
                    ttk.Label(unidad_frame, text=header, font=("Arial", 10, "bold")).grid(
                        row=0, column=i, padx=5, pady=2, sticky="w")
                
                # Datos
                for row_idx, unidad in enumerate(stats['por_unidad'][:15]):  # Mostrar top 15
                    ttk.Label(unidad_frame, text=unidad.get('unidad', '')[:20]).grid(
                        row=row_idx+1, column=0, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('total_empleados', 0))).grid(
                        row=row_idx+1, column=1, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('activos', 0))).grid(
                        row=row_idx+1, column=2, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('inactivos', 0))).grid(
                        row=row_idx+1, column=3, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('con_posicion', 0))).grid(
                        row=row_idx+1, column=4, padx=5, pady=1, sticky="w")
                    ttk.Label(unidad_frame, text=str(unidad.get('con_fecha_inicio', 0))).grid(
                        row=row_idx+1, column=5, padx=5, pady=1, sticky="w")
            
            # Estadísticas por puesto
            if 'por_puesto' in stats and stats['por_puesto']:
                ttk.Label(scrollable_frame, text="👔 Por Puesto", 
                         font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
                
                # Crear tabla para puestos
                puesto_frame = ttk.Frame(scrollable_frame)
                puesto_frame.pack(fill=tk.X, pady=(0, 20))
                
                # Headers
                headers = ["Puesto", "Unidad", "Total", "Activos", "Inactivos", "Con Fecha Inicio"]
                for i, header in enumerate(headers):
                    ttk.Label(puesto_frame, text=header, font=("Arial", 10, "bold")).grid(
                        row=0, column=i, padx=5, pady=2, sticky="w")
                
                # Datos
                for row_idx, puesto in enumerate(stats['por_puesto'][:15]):  # Mostrar top 15
                    ttk.Label(puesto_frame, text=puesto.get('puesto', '')[:15]).grid(
                        row=row_idx+1, column=0, padx=5, pady=1, sticky="w")
                    ttk.Label(puesto_frame, text=puesto.get('unidad', '')[:15]).grid(
                        row=row_idx+1, column=1, padx=5, pady=1, sticky="w")
                    ttk.Label(puesto_frame, text=str(puesto.get('total_empleados', 0))).grid(
                        row=row_idx+1, column=2, padx=5, pady=1, sticky="w")
                    ttk.Label(puesto_frame, text=str(puesto.get('activos', 0))).grid(
                        row=row_idx+1, column=3, padx=5, pady=1, sticky="w")
                    ttk.Label(puesto_frame, text=str(puesto.get('inactivos', 0))).grid(
                        row=row_idx+1, column=4, padx=5, pady=1, sticky="w")
                    ttk.Label(puesto_frame, text=str(puesto.get('con_fecha_inicio', 0))).grid(
                        row=row_idx+1, column=5, padx=5, pady=1, sticky="w")
            
            # Detalle por unidad (lista de empleados)
            if 'detalle_por_unidad' in stats and stats['detalle_por_unidad']:
                ttk.Label(scrollable_frame, text="👥 Detalle por Unidad - Lista de Empleados", 
                         font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
                
                # Agrupar por unidad
                unidades_empleados = {}
                for emp in stats['detalle_por_unidad']:
                    unidad = emp.get('unidad', 'Sin Unidad')
                    if unidad not in unidades_empleados:
                        unidades_empleados[unidad] = []
                    unidades_empleados[unidad].append(emp)
                
                # Mostrar cada unidad
                for unidad, empleados in list(unidades_empleados.items())[:5]:  # Mostrar top 5 unidades
                    ttk.Label(scrollable_frame, text=f"🏢 {unidad} ({len(empleados)} empleados)", 
                             font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
                    
                    # Crear tabla para empleados de esta unidad
                    emp_frame = ttk.Frame(scrollable_frame)
                    emp_frame.pack(fill=tk.X, pady=(0, 15))
                    
                    # Headers
                    headers = ["ID", "Nombre", "Puesto", "Manager", "Estado", "Fecha Inicio"]
                    for i, header in enumerate(headers):
                        ttk.Label(emp_frame, text=header, font=("Arial", 9, "bold")).grid(
                            row=0, column=i, padx=3, pady=1, sticky="w")
                    
                    # Datos de empleados
                    for row_idx, emp in enumerate(empleados[:10]):  # Mostrar max 10 empleados por unidad
                        ttk.Label(emp_frame, text=emp.get('scotia_id', '')[:8]).grid(
                            row=row_idx+1, column=0, padx=3, pady=1, sticky="w")
                        ttk.Label(emp_frame, text=emp.get('full_name', '')[:20]).grid(
                            row=row_idx+1, column=1, padx=3, pady=1, sticky="w")
                        ttk.Label(emp_frame, text=emp.get('puesto', '')[:15]).grid(
                            row=row_idx+1, column=2, padx=3, pady=1, sticky="w")
                        ttk.Label(emp_frame, text=emp.get('manager', '')[:15]).grid(
                            row=row_idx+1, column=3, padx=3, pady=1, sticky="w")
                        ttk.Label(emp_frame, text=emp.get('estado', '')[:8]).grid(
                            row=row_idx+1, column=4, padx=3, pady=1, sticky="w")
                        ttk.Label(emp_frame, text=emp.get('start_date', '')[:10]).grid(
                            row=row_idx+1, column=5, padx=3, pady=1, sticky="w")
                    
                    if len(empleados) > 10:
                        ttk.Label(emp_frame, text=f"... y {len(empleados) - 10} empleados más", 
                                 font=("Arial", 9, "italic")).grid(
                            row=len(empleados)+1, column=0, columnspan=6, padx=3, pady=1, sticky="w")
            
            # Botón de cerrar
            ttk.Button(scrollable_frame, text="Cerrar", command=stats_window.destroy).pack(pady=20)
            
            # Configurar scroll
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando estadísticas: {str(e)}")

    def exportar_estadisticas_headcount(self):
        """Exporta las estadísticas del headcount a Excel"""
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            from export_service import export_service
            
            # Obtener estadísticas
            stats = access_service.get_headcount_statistics()
            
            if "error" in stats:
                messagebox.showerror("Error", stats["error"])
                return
            
            # Exportar a Excel
            filepath = export_service.export_headcount_statistics(stats)
            
            messagebox.showinfo("Éxito", f"Estadísticas del headcount exportadas exitosamente a:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando estadísticas: {str(e)}")


class PersonaDialog:
    """Diálogo para agregar/editar personas"""
    
    def __init__(self, parent, title: str, persona_data: dict = None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar el diálogo
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.persona_data = persona_data
        self.result = None
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_label = ttk.Label(scrollable_frame, text="Información de la Persona", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos del formulario
        campos = [
            ("SID (Scotia ID):", "scotia_id", "entry"),
            ("Employee ID:", "employee", "entry"),
            ("Nombre Completo:", "full_name", "entry"),
            ("Email:", "email", "entry"),
            ("Posición:", "position", "entry"),
            ("Manager:", "manager", "entry"),
            ("Senior Manager:", "senior_manager", "entry"),
            ("Unidad:", "unit", "combobox", ["Tecnología", "Recursos Humanos", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Fecha de Inicio:", "start_date", "entry"),
            ("CECO:", "ceco", "entry"),
            ("Skip Level:", "skip_level", "entry"),
            ("Cafe Alcides:", "cafe_alcides", "entry"),
            ("Parents:", "parents", "entry"),
            ("Email Personal:", "personal_email", "entry"),
            ("Tamaño:", "size", "combobox", ["XS", "S", "M", "L", "XL", "XXL"]),
            ("Cumpleaños:", "birthday", "entry"),
            ("Validación:", "validacion", "entry"),
            ("Estado:", "activo", "combobox", ["Activo", "Inactivo"]),
            ("Fecha de Inactivación:", "inactivation_date", "entry")
        ]
        
        # Crear campos dinámicamente
        self.variables = {}
        self.widgets = {}
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(scrollable_frame, text=label_text).grid(row=i+1, column=0, sticky="w", pady=5)
            
            if tipo == "entry":
                self.variables[var_name] = tk.StringVar()
                entry = ttk.Entry(scrollable_frame, textvariable=self.variables[var_name], width=40)
                entry.grid(row=i+1, column=1, sticky="ew", pady=5, padx=(10, 0))
                self.widgets[var_name] = entry
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                self.variables[var_name] = tk.StringVar()
                combo = ttk.Combobox(scrollable_frame, textvariable=self.variables[var_name], values=valores, width=37)
                combo.grid(row=i+1, column=1, sticky="ew", pady=5, padx=(10, 0))
                self.widgets[var_name] = combo
        
        # Configurar grid
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ttk.Button(button_frame, text="Guardar", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self._cancel).pack(side=tk.LEFT, padx=5)
        
        # Configurar validación
        if 'scotia_id' in self.widgets:
            self.widgets['scotia_id'].focus()
        
        self.dialog.bind('<Return>', lambda e: self._save())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _load_data(self):
        """Carga los datos existentes si es una edición"""
        if self.persona_data:
            for var_name, var in self.variables.items():
                if var_name in self.persona_data:
                    if var_name == 'activo':
                        var.set('Activo' if self.persona_data[var_name] else 'Inactivo')
                    else:
                        var.set(str(self.persona_data[var_name]) if self.persona_data[var_name] is not None else '')
    
    def _save(self):
        """Guarda los datos del formulario"""
        # Validaciones
        if not self.variables['scotia_id'].get().strip():
            messagebox.showerror("Error", "El SID es obligatorio")
            return
        
        if not self.variables['employee'].get().strip():
            messagebox.showerror("Error", "El Employee ID es obligatorio")
            return
        
        if not self.variables['full_name'].get().strip():
            messagebox.showerror("Error", "El nombre completo es obligatorio")
            return
        
        if not self.variables['email'].get().strip():
            messagebox.showerror("Error", "El email es obligatorio")
            return
        
        # Preparar datos
        self.result = {}
        for var_name, var in self.variables.items():
            if var_name == 'activo':
                self.result[var_name] = var.get() == 'Activo'
            else:
                self.result[var_name] = var.get().strip()
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class HistorialDialog:
    """Diálogo para editar registros del historial"""
    
    def __init__(self, parent, title: str, historial_data: dict = None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar el diálogo
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.historial_data = historial_data
        self.result = None
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_label = ttk.Label(scrollable_frame, text="Editar Registro de Historial", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos del formulario
        campos = [
            ("SID:", "scotia_id", "entry"),
            ("ID de Caso:", "case_id", "entry"),
            ("Responsable:", "responsible", "entry"),
            ("Fecha de Registro:", "record_date", "entry"),
            ("Fecha de Solicitud:", "request_date", "entry"),
            ("Proceso de Acceso:", "process_access", "combobox", ["onboarding", "offboarding", "lateral_movement"]),
            ("SID (interno):", "sid", "entry"),
            ("Área:", "area", "entry"),
            ("Sub Unidad:", "subunit", "entry"),
            ("Descripción del Evento:", "event_description", "text"),
            ("Email del Ticket:", "ticket_email", "entry"),
            ("Nombre de Aplicación:", "app_access_name", "entry"),
            ("Tipo de Sistema:", "computer_system_type", "combobox", ["Desktop", "Laptop", "Mobile", "Server"]),
            ("Estado:", "status", "combobox", ["Pendiente", "En Proceso", "Completado", "Cancelado", "Rechazado"]),
            ("Fecha de Cierre App:", "closing_date_app", "entry"),
            ("Fecha de Cierre Ticket:", "closing_date_ticket", "entry"),
            ("Calidad de App:", "app_quality", "combobox", ["Excelente", "Buena", "Regular", "Mala"]),
            ("Confirmación por Usuario:", "confirmation_by_user", "entry"),
            ("Comentario:", "comment", "text"),
            ("Calidad del Ticket:", "ticket_quality", "combobox", ["Excelente", "Buena", "Regular", "Mala"]),
            ("Estado General:", "general_status", "combobox", ["Pendiente", "En Proceso", "Completado", "Cancelado"]),
            ("Tiempo Promedio de Apertura:", "average_time_open_ticket", "entry")
        ]
        
        # Crear campos dinámicamente
        self.variables = {}
        self.widgets = {}
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(scrollable_frame, text=label_text).grid(row=i+1, column=0, sticky="w", pady=5)
            
            if tipo == "entry":
                self.variables[var_name] = tk.StringVar()
                entry = ttk.Entry(scrollable_frame, textvariable=self.variables[var_name], width=50)
                entry.grid(row=i+1, column=1, sticky="ew", pady=5, padx=(10, 0))
                self.widgets[var_name] = entry
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                self.variables[var_name] = tk.StringVar()
                combo = ttk.Combobox(scrollable_frame, textvariable=self.variables[var_name], values=valores, width=47)
                combo.grid(row=i+1, column=1, sticky="ew", pady=5, padx=(10, 0))
                self.widgets[var_name] = combo
            elif tipo == "text":
                text_widget = tk.Text(scrollable_frame, height=3, width=50)
                text_widget.grid(row=i+1, column=1, sticky="ew", pady=5, padx=(10, 0))
                self.variables[var_name] = text_widget  # Para Text widgets, guardamos el widget directamente
                self.widgets[var_name] = text_widget
        
        # Configurar grid
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ttk.Button(button_frame, text="Guardar", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self._cancel).pack(side=tk.LEFT, padx=5)
        
        # Configurar validación
        if 'scotia_id' in self.widgets:
            self.widgets['scotia_id'].focus()
        
        self.dialog.bind('<Return>', lambda e: self._save())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _load_data(self):
        """Carga los datos existentes si es una edición"""
        if self.historial_data:
            for var_name, var in self.variables.items():
                if var_name in self.historial_data:
                    if isinstance(var, tk.StringVar):
                        var.set(str(self.historial_data[var_name]) if self.historial_data[var_name] is not None else '')
                    elif isinstance(var, tk.Text):
                        var.delete('1.0', tk.END)
                        var.insert('1.0', str(self.historial_data[var_name]) if self.historial_data[var_name] is not None else '')
    
    def _save(self):
        """Guarda los datos del formulario"""
        # Validaciones básicas
        if not self.variables['scotia_id'].get().strip():
            messagebox.showerror("Error", "El SID es obligatorio")
            return
        
        if not self.variables['process_access'].get().strip():
            messagebox.showerror("Error", "El proceso de acceso es obligatorio")
            return
        
        # Preparar datos
        self.result = {}
        for var_name, var in self.variables.items():
            if isinstance(var, tk.StringVar):
                self.result[var_name] = var.get().strip()
            elif isinstance(var, tk.Text):
                self.result[var_name] = var.get('1.0', tk.END).strip()
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()
