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
        self.frame.columnconfigure(1, weight=0)
        
        # Centrar el contenido
        main_container = ttk.Frame(self.frame)
        main_container.grid(row=0, column=1, sticky="ew", padx=20)
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
                ttk.Entry(main_container, textvariable=self.variables[var_name], width=35).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(main_container, textvariable=self.variables[var_name], 
                            values=valores, width=32).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
        
        # Información del número de caso (solo informativo)
        info_frame = ttk.Frame(main_container)
        info_frame.grid(row=len(campos), column=0, columnspan=2, pady=(15, 0), sticky="ew")
        
        ttk.Label(info_frame, text="Nota: El número de caso se generará automáticamente al guardar", 
                  font=("Arial", 9, "italic"), foreground="gray").pack(anchor=tk.CENTER)
    
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
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        main_container.columnconfigure(0, weight=1)
        
        # Título
        ttk.Label(main_container, text="Tipo de Onboarding", 
                  font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
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
                 width=25).pack(side=tk.LEFT, padx=(5, 0))
    
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
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        main_container.columnconfigure(0, weight=1)
        
        # Título
        ttk.Label(main_container, text="Tipo de Offboarding", 
                  font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
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
                 width=25).pack(side=tk.LEFT, padx=(5, 0))
    
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
            'empleo_anterior': tk.StringVar(),
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
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        main_container.columnconfigure(1, weight=1)
        
        # Título
        ttk.Label(main_container, text="Información de Lateral Movement", 
                  font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Frame para campos
        campos_frame = ttk.Frame(main_container)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        campos_frame.columnconfigure(1, weight=1)
        
        # Campo empleo anterior
        ttk.Label(campos_frame, text="Empleo Anterior:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 15))
        ttk.Entry(campos_frame, textvariable=self.variables['empleo_anterior'], width=35).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5
        )
        
        # Título para radio buttons
        ttk.Label(campos_frame, text="Tipo de Movimiento:", font=("Arial", 12, "bold")).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Submenú con radio buttons
        opciones_submenu = ["Movimiento Horizontal", "Reasignación de Proyecto", "Cambio de Equipo", "Rotación de Funciones"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(campos_frame, text=opcion, 
                           variable=self.variables['submenu_lateral'], 
                           value=opcion).grid(row=2+i, column=0, columnspan=2, sticky=tk.CENTER, pady=5)
        
        # Opción Other con campo de texto
        other_row = 2 + len(opciones_submenu)
        other_frame = ttk.Frame(campos_frame)
        other_frame.grid(row=other_row, column=0, columnspan=2, sticky=tk.CENTER, pady=5)
        
        ttk.Radiobutton(other_frame, text="Other:", 
                       variable=self.variables['submenu_lateral'], 
                       value="other").pack(side=tk.LEFT)
        
        ttk.Entry(other_frame, textvariable=self.variables['other_lateral'], 
                 width=25).pack(side=tk.LEFT, padx=(5, 0))
    
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
            'sid_busqueda': tk.StringVar(),
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
            'comment_edicion': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        
        # Configurar grid del frame principal
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Crear canvas con scrollbar
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar grid del frame scrolleable
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(2, weight=1)  # La sección de resultados debe expandirse
        
        # Título
        ttk.Label(scrollable_frame, text="Edición y Búsqueda de Registros", 
                  font=("Arial", 16, "bold")).grid(row=0, column=0, pady=20, sticky="ew")
        
        # Frame principal
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=60, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # La sección de resultados debe expandirse
        
        # Sección de búsqueda
        busqueda_frame = ttk.LabelFrame(main_frame, text="Búsqueda", padding="20")
        busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        busqueda_frame.columnconfigure(1, weight=1)
        
        # Búsqueda por número de caso
        ttk.Label(busqueda_frame, text="Número de Caso:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 15))
        ttk.Entry(busqueda_frame, textvariable=self.variables['numero_caso_busqueda'], width=35).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=8
        )
        ttk.Button(busqueda_frame, text="Buscar por Caso", command=self.buscar_por_numero_caso).grid(
            row=0, column=2, padx=(15, 0), pady=8
        )
        
        # Búsqueda por SID
        ttk.Label(busqueda_frame, text="SID:").grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0, 15))
        ttk.Entry(busqueda_frame, textvariable=self.variables['sid_busqueda'], width=35).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=8
        )
        ttk.Button(busqueda_frame, text="Buscar por SID", command=self.buscar_por_sid).grid(
            row=1, column=2, padx=(15, 0), pady=8
        )
        
        # Sección de edición
        edicion_frame = ttk.LabelFrame(main_frame, text="Edición de Campos", padding="20")
        edicion_frame.grid(row=1, column=0, sticky="ew", pady=(0, 30))
        edicion_frame.columnconfigure(1, weight=1)
        
        # Campos básicos
        campos_basicos = [
            ("Número de Caso:", "numero_caso_edicion", "entry"),
            ("Nueva Sub Unidad:", "nueva_sub_unidad_edicion", "combobox", [
                "Sub Unidad 1 - Desarrollo Frontend",
                "Sub Unidad 2 - Desarrollo Backend", 
                "Sub Unidad 3 - DevOps e Infraestructura",
                "Sub Unidad 4 - QA y Testing",
                "Sub Unidad 5 - Diseño UX/UI",
                "Sub Unidad 6 - Gestión de Proyectos",
                "Sub Unidad 7 - Soporte Técnico"
            ]),
            ("Nuevo Cargo:", "nuevo_cargo_edicion", "entry"),
            ("Request Date:", "request_date_edicion", "entry"),
            ("Quien hace el ingreso:", "ingreso_por_edicion", "combobox", ["Juan Pérez", "María García"]),
            ("Fecha:", "fecha_edicion", "entry"),
            ("Status:", "status_edicion", "combobox", ["Pendiente", "En Proceso", "Completado", "Cancelado", "Rechazado"])
        ]
        
        # Campos adicionales
        campos_adicionales = [
            ("Mail:", "mail_edicion", "entry"),
            ("Closing Date App:", "closing_date_app_edicion", "entry"),
            ("App Quality:", "app_quality_edicion", "combobox", ["Excelente", "Buena", "Regular", "Mala", "Pendiente"]),
            ("Confirmation by User:", "confirmation_by_user_edicion", "combobox", ["Sí", "No", "Pendiente"]),
            ("Comment:", "comment_edicion", "entry")
        ]
        
        # Crear campos básicos
        for i, campo in enumerate(campos_basicos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(edicion_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 15))
            
            if tipo == "entry":
                ttk.Entry(edicion_frame, textvariable=self.variables[var_name], width=35).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(edicion_frame, textvariable=self.variables[var_name], 
                            values=valores, width=32).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
        
        # Separador
        ttk.Separator(edicion_frame, orient='horizontal').grid(
            row=len(campos_basicos), column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        
        # Crear campos adicionales
        for i, campo in enumerate(campos_adicionales):
            label_text, var_name, tipo = campo[:3]
            row = len(campos_basicos) + 1 + i
            ttk.Label(edicion_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5, padx=(0, 15))
            
            if tipo == "entry":
                ttk.Entry(edicion_frame, textvariable=self.variables[var_name], width=35).grid(
                    row=row, column=1, sticky=(tk.W, tk.E), pady=5
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(edicion_frame, textvariable=self.variables[var_name], 
                            values=valores, width=32).grid(
                    row=row, column=1, sticky=(tk.W, tk.E), pady=5
                )
        
        # Botones de acción
        botones_frame = ttk.Frame(edicion_frame)
        botones_frame.grid(row=len(campos_basicos) + len(campos_adicionales) + 1, column=0, columnspan=2, pady=20)
        
        ttk.Button(botones_frame, text="Guardar Cambios", command=self.guardar_cambios).pack(side=tk.LEFT, padx=10)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=10)
        
        # Sección de resultados de búsqueda
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados de Búsqueda", padding="20")
        resultados_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 30))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar resultados
        self.tree = ttk.Treeview(resultados_frame, columns=("Número Caso", "SID", "Sub Unidad", "Cargo", "Status", "Request Date", "Ingreso Por", "Tipo"), show="headings")
        
        # Configurar columnas
        self.tree.heading("Número Caso", text="Número Caso")
        self.tree.heading("SID", text="SID")
        self.tree.heading("Sub Unidad", text="Sub Unidad")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Request Date", text="Request Date")
        self.tree.heading("Ingreso Por", text="Ingreso Por")
        self.tree.heading("Tipo", text="Tipo")
        
        # Configurar anchos de columna
        self.tree.column("Número Caso", width=150)
        self.tree.column("SID", width=100)
        self.tree.column("Sub Unidad", width=150)
        self.tree.column("Cargo", width=120)
        self.tree.column("Status", width=100)
        self.tree.column("Request Date", width=100)
        self.tree.column("Ingreso Por", width=120)
        self.tree.column("Tipo", width=100)
        
        # Scrollbar para treeview
        tree_scrollbar = ttk.Scrollbar(resultados_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Empaquetar treeview y scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Binding para selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_registro)
        
        # Empaquetar canvas y scrollbar principal
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar el canvas para que se expanda
        canvas.configure(width=800, height=600)
        
        # Binding para scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def buscar_por_numero_caso(self):
        """Busca registros por número de caso"""
        numero_caso = self.variables['numero_caso_busqueda'].get().strip()
        if not numero_caso:
            messagebox.showwarning("Advertencia", "Por favor ingrese un número de caso para buscar")
            return
        
        if self.service:
            # Búsqueda real usando el servicio
            resultados = self.service.buscar_por_numero_caso(numero_caso)
            self.mostrar_resultados_busqueda(resultados, f"caso {numero_caso}")
        else:
            # Búsqueda simulada si no hay servicio
            self.simular_busqueda_por_caso(numero_caso)
    
    def buscar_por_sid(self):
        """Busca registros por SID"""
        sid = self.variables['sid_busqueda'].get().strip()
        if not sid:
            messagebox.showwarning("Advertencia", "Por favor ingrese un SID para buscar")
            return
        
        if self.service:
            # Búsqueda real usando el servicio
            resultados = self.service.buscar_por_sid(sid)
            self.mostrar_resultados_busqueda(resultados, sid)
        else:
            # Búsqueda simulada si no hay servicio
            self.simular_busqueda(sid)
    
    def mostrar_resultados_busqueda(self, resultados, busqueda):
        """Muestra los resultados reales de la búsqueda"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                # Los datos del empleado están anidados dentro de la clave 'empleado'
                empleado = resultado.get('empleado', {})
                
                # Determinar el tipo de proceso basado en las claves disponibles
                tipo_proceso = ""
                if 'tipo_onboarding' in resultado:
                    tipo_proceso = resultado['tipo_onboarding']
                elif 'tipo_offboarding' in resultado:
                    tipo_proceso = resultado['tipo_offboarding']
                elif 'tipo_lateral' in resultado:
                    tipo_proceso = resultado['tipo_lateral']
                else:
                    tipo_proceso = resultado.get('tipo_proceso', '')
                
                valores = (
                    empleado.get('numero_caso', ''),
                    empleado.get('sid', ''),
                    empleado.get('nueva_sub_unidad', ''),
                    empleado.get('nuevo_cargo', ''),
                    empleado.get('status', ''),
                    empleado.get('request_date', ''),
                    empleado.get('ingreso_por', ''),
                    tipo_proceso
                )
                self.tree.insert("", "end", values=valores)
            
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} registros para: {busqueda}")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron registros para: {busqueda}")
    
    def simular_busqueda_por_caso(self, numero_caso):
        """Simula la búsqueda de registros por número de caso (placeholder)"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Simular datos encontrados
        datos_simulados = [
            (numero_caso, "EMP001", "Sub Unidad 1 - Desarrollo Frontend", "Desarrollador Frontend", "En Proceso", "2024-01-15", "Juan Pérez", "Onboarding"),
            (numero_caso, "EMP002", "Sub Unidad 2 - Desarrollo Backend", "Desarrollador Backend", "Completado", "2024-01-20", "Juan Pérez", "Lateral Movement")
        ]
        
        for dato in datos_simulados:
            self.tree.insert("", "end", values=dato)
        
        if datos_simulados:
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(datos_simulados)} registros para el caso: {numero_caso}")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron registros para el caso: {numero_caso}")
    
    def simular_busqueda(self, sid):
        """Simula la búsqueda de registros (placeholder)"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Simular datos encontrados
        datos_simulados = [
            ("CASE-20240115120000-12345678", sid, "Sub Unidad 1 - Desarrollo Frontend", "Desarrollador Frontend", "En Proceso", "2024-01-15", "Juan Pérez", "Onboarding"),
            ("CASE-20240120120000-87654321", sid, "Sub Unidad 2 - Desarrollo Backend", "Desarrollador Backend", "Completado", "2024-01-20", "Juan Pérez", "Lateral Movement")
        ]
        
        for dato in datos_simulados:
            self.tree.insert("", "end", values=dato)
        
        if datos_simulados:
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(datos_simulados)} registros para el SID: {sid}")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron registros para el SID: {sid}")
    
    def seleccionar_registro(self, event):
        """Maneja la selección de un registro en el treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            valores = item['values']
            
            # Cargar valores en los campos de edición
            if len(valores) >= 8:
                # Campos básicos
                self.variables['numero_caso_edicion'].set(valores[0])
                self.variables['nueva_sub_unidad_edicion'].set(valores[2])
                self.variables['nuevo_cargo_edicion'].set(valores[3])
                self.variables['status_edicion'].set(valores[4])
                self.variables['request_date_edicion'].set(valores[5])
                self.variables['ingreso_por_edicion'].set(valores[6])
                
                # Los campos adicionales se mantienen vacíos para ser editados
                # ya que no están en la tabla de resultados
    
    def guardar_cambios(self):
        """Guarda los cambios realizados en los campos"""
        # Aquí se implementaría la lógica para guardar los cambios
        # Por ahora solo mostramos un mensaje
        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")
    
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

class CreacionPersonaFrame:
    """Componente para la pestaña de creación de persona en headcount"""
    
    def __init__(self, parent, service=None):
        self.parent = parent
        self.service = service
        self.variables = {}
        self._crear_variables()
        self._crear_widgets()
    
    def _crear_variables(self):
        """Crea las variables de control"""
        self.variables = {
            'nombre': tk.StringVar(),
            'apellido': tk.StringVar(),
            'email': tk.StringVar(),
            'telefono': tk.StringVar(),
            'departamento': tk.StringVar(),
            'cargo': tk.StringVar(),
            'fecha_contratacion': tk.StringVar(),
            'salario': tk.StringVar(),
            'estado': tk.StringVar(value="Activo")
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        
        # Configurar grid del frame principal
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Crear canvas con scrollbar
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar grid del frame scrolleable
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(1, weight=1)
        
        # Título
        ttk.Label(scrollable_frame, text="Crear Nueva Persona en Headcount", 
                  font=("Arial", 16, "bold")).grid(row=0, column=0, pady=20, sticky="ew")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=60, pady=20)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(len([
            ("Nombre:", "nombre", "entry"),
            ("Apellido:", "apellido", "entry"),
            ("Email:", "email", "entry"),
            ("Teléfono:", "telefono", "entry"),
            ("Departamento:", "departamento", "combobox", ["Recursos Humanos", "Tecnología", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Cargo:", "cargo", "entry"),
            ("Fecha de Contratación:", "fecha_contratacion", "entry"),
            ("Salario:", "salario", "entry"),
            ("Estado:", "estado", "combobox", ["Activo", "Inactivo", "Vacaciones", "Licencia"])
        ]), weight=1)
        
        # Campos del formulario
        campos = [
            ("Nombre:", "nombre", "entry"),
            ("Apellido:", "apellido", "entry"),
            ("Email:", "email", "entry"),
            ("Teléfono:", "telefono", "entry"),
            ("Departamento:", "departamento", "combobox", ["Recursos Humanos", "Tecnología", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Cargo:", "cargo", "entry"),
            ("Fecha de Contratación:", "fecha_contratacion", "entry"),
            ("Salario:", "salario", "entry"),
            ("Estado:", "estado", "combobox", ["Activo", "Inactivo", "Vacaciones", "Licencia"])
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 15))
            
            if tipo == "entry":
                ttk.Entry(main_frame, textvariable=self.variables[var_name], width=35).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(main_frame, textvariable=self.variables[var_name], 
                            values=valores, width=32).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
        
        # Botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        ttk.Button(botones_frame, text="Crear Persona", command=self.crear_persona).pack(side=tk.LEFT, padx=10)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=10)
        
        # Empaquetar canvas y scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar el canvas para que se expanda
        canvas.configure(width=800, height=600)
        
        # Binding para scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def crear_persona(self):
        """Crea una nueva persona en el headcount"""
        if self.service:
            # Crear persona usando el servicio
            datos = self.obtener_datos()
            exito, mensaje = self.service.guardar_persona_headcount(datos)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar()
            else:
                messagebox.showerror("Error", mensaje)
        else:
            # Validación local si no hay servicio
            campos_vacios = self.validar_campos_obligatorios()
            if campos_vacios:
                messagebox.showerror("Error", f"Por favor complete los campos obligatorios: {', '.join(campos_vacios)}")
                return
            
            # Simular creación exitosa
            messagebox.showinfo("Éxito", "Persona creada exitosamente en el headcount")
            self.limpiar()
    
    def validar_campos_obligatorios(self):
        """Valida que los campos obligatorios estén completos"""
        campos_obligatorios = ['nombre', 'apellido', 'email', 'departamento', 'cargo']
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
        self.variables['estado'].set("Activo")
