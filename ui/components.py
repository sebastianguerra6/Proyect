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
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Aumentar padx de 15 a 20
        main_container.columnconfigure(1, weight=1)
        
        # Título
        ttk.Label(main_container, text="Información de Lateral Movement", 
                  style="Section.TLabel").pack(pady=(0, 20))
        
        # Frame para campos
        campos_frame = ttk.Frame(main_container)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        campos_frame.columnconfigure(1, weight=1)
        
        # Campo empleo anterior
        ttk.Label(campos_frame, text="Empleo Anterior:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 15))
        ttk.Entry(campos_frame, textvariable=self.variables['empleo_anterior'], width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5
        )
        
        # Título para radio buttons
        ttk.Label(campos_frame, text="Tipo de Movimiento:", style="Subsection.TLabel").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        # Submenú con radio buttons
        opciones_submenu = ["Movimiento Horizontal", "Reasignación de Proyecto", "Cambio de Equipo", "Rotación de Funciones"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(campos_frame, text=opcion, 
                           variable=self.variables['submenu_lateral'], 
                           value=opcion).grid(row=2+i, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Opción Other con campo de texto
        other_row = 2 + len(opciones_submenu)
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
            'comment_edicion': tk.StringVar(),
            'filtro_texto': tk.StringVar(),
            'columna_filtro': tk.StringVar(value="SID")
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
                  style="Title.TLabel").grid(row=0, column=0, pady=20, sticky="ew")
        
        # Frame principal
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=10)  # Reducir pady
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # La sección de resultados debe expandirse
        
        # Sección de búsqueda
        busqueda_frame = ttk.LabelFrame(main_frame, text="Búsqueda", padding="15")  # Reducir padding
        busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))  # Reducir pady
        busqueda_frame.columnconfigure(1, weight=1)
        
        # Búsqueda por número de caso
        ttk.Label(busqueda_frame, text="Número de Caso:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 15))
        ttk.Entry(busqueda_frame, textvariable=self.variables['numero_caso_busqueda'], width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=8
        )
        ttk.Button(busqueda_frame, text="Buscar por Caso", command=self.buscar_por_numero_caso).grid(
            row=0, column=2, padx=(15, 0), pady=8
        )
        
        # Búsqueda por SID
        ttk.Label(busqueda_frame, text="SID:").grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0, 15))
        ttk.Entry(busqueda_frame, textvariable=self.variables['sid_busqueda'], width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=8
        )
        ttk.Button(busqueda_frame, text="Buscar por SID", command=self.buscar_por_sid).grid(
            row=1, column=2, padx=(15, 0), pady=8
        )
        
        # Botón para buscar todos los registros
        ttk.Button(busqueda_frame, text="Mostrar Todos los Registros", 
                  command=self.buscar_todos_los_registros).grid(
            row=2, column=0, columnspan=3, pady=(15, 0)
        )
        
        # Sección de filtrado
        filtro_frame = ttk.LabelFrame(main_frame, text="Filtrado Avanzado", padding="15")  # Reducir padding
        filtro_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))  # Reducir pady
        filtro_frame.columnconfigure(1, weight=1)
        
        # Filtro por texto con selección de columna
        ttk.Label(filtro_frame, text="Filtrar por:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 15))
        
        # Combobox para seleccionar columna
        columnas_filtro = [
            "SID", "Sub Unidad", "Cargo", "Status", "Request Date", 
            "Ingreso Por", "Tipo", "APP Name", "Mail", "App Quality", 
            "Confirmation by User", "Comment"
        ]
        columna_combobox = ttk.Combobox(filtro_frame, textvariable=self.variables['columna_filtro'], 
                                       values=columnas_filtro, width=20, state="readonly")
        columna_combobox.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(0, 15))
        
        # Input para el texto del filtro
        filtro_entry = ttk.Entry(filtro_frame, textvariable=self.variables['filtro_texto'], 
                 width=40)
        filtro_entry.grid(row=0, column=2, sticky=(tk.W, tk.E), pady=8, padx=(0, 15))
        
        # Tooltip informativo
        ttk.Label(filtro_frame, text="💡 Escriba para filtrar en tiempo real", 
                 style="Normal.TLabel", foreground="gray").grid(
            row=1, column=2, sticky=tk.W, pady=(2, 0)
        )
        
        # Binding para filtrado en tiempo real (con delay)
        self.filtro_delay_id = None
        filtro_entry.bind('<KeyRelease>', self._on_filtro_change)
        
        # Botón para aplicar filtro
        ttk.Button(filtro_frame, text="🔍 Aplicar Filtro", 
                  command=self.aplicar_filtro).grid(
            row=0, column=3, padx=(15, 0), pady=8
        )
        
        # Botón para limpiar filtro
        ttk.Button(filtro_frame, text="🧹 Limpiar Filtro", 
                  command=self.limpiar_filtro).grid(
            row=2, column=0, columnspan=4, pady=(15, 0)
        )
        
        # Sección de edición
        edicion_frame = ttk.LabelFrame(main_frame, text="Edición de Campos", padding="15")  # Reducir padding
        edicion_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))  # Reducir pady
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
            ttk.Label(edicion_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=3, padx=(0, 15))  # Reducir pady
            
            if tipo == "entry":
                ttk.Entry(edicion_frame, textvariable=self.variables[var_name], width=50).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=3  # Reducir pady
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(edicion_frame, textvariable=self.variables[var_name], 
                            values=valores, width=47).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=3  # Reducir pady
                )
        
        # Separador
        ttk.Separator(edicion_frame, orient='horizontal').grid(
            row=len(campos_basicos), column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        
        # Crear campos adicionales
        for i, campo in enumerate(campos_adicionales):
            label_text, var_name, tipo = campo[:3]
            row = len(campos_basicos) + 1 + i
            ttk.Label(edicion_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3, padx=(0, 15))  # Reducir pady
            
            if tipo == "entry":
                ttk.Entry(edicion_frame, textvariable=self.variables[var_name], width=50).grid(
                    row=row, column=1, sticky=(tk.W, tk.E), pady=3  # Reducir pady
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(edicion_frame, textvariable=self.variables[var_name], 
                            values=valores, width=47).grid(
                    row=row, column=1, sticky=(tk.W, tk.E), pady=3  # Reducir pady
                )
        
        # Botones de acción
        botones_frame = ttk.Frame(edicion_frame)
        botones_frame.grid(row=len(campos_basicos) + len(campos_adicionales) + 1, column=0, columnspan=2, pady=10)  # Reducir pady
        
        ttk.Button(botones_frame, text="Guardar Cambios", command=self.guardar_cambios).pack(side=tk.LEFT, padx=10)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=10)
        
        # Sección de resultados de búsqueda
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados de Búsqueda", padding="15")  # Reducir padding
        resultados_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))  # Reducir pady
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Frame para la tabla con scrollbars
        tabla_frame = ttk.Frame(resultados_frame)
        tabla_frame.grid(row=0, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar resultados (aumentar altura para mejor visualización)
        self.tree = ttk.Treeview(tabla_frame, columns=("Número Caso", "SID", "Sub Unidad", "Cargo", "Status", "Request Date", "Ingreso Por", "Tipo", "APP Name", "Mail", "Closing Date App", "App Quality", "Confirmation by User", "Comment"), show="headings", height=12)
        
        # Configurar columnas
        self.tree.heading("Número Caso", text="Número Caso")
        self.tree.heading("SID", text="SID")
        self.tree.heading("Sub Unidad", text="Sub Unidad")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Request Date", text="Request Date")
        self.tree.heading("Ingreso Por", text="Ingreso Por")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("APP Name", text="APP Name")
        self.tree.heading("Mail", text="Mail")
        self.tree.heading("Closing Date App", text="Closing Date App")
        self.tree.heading("App Quality", text="App Quality")
        self.tree.heading("Confirmation by User", text="Confirmation by User")
        self.tree.heading("Comment", text="Comment")
        
        # Configurar anchos de columna (más compactos para mejor visualización)
        self.tree.column("Número Caso", width=100, minwidth=80)
        self.tree.column("SID", width=70, minwidth=60)
        self.tree.column("Sub Unidad", width=100, minwidth=80)
        self.tree.column("Cargo", width=80, minwidth=70)
        self.tree.column("Status", width=70, minwidth=60)
        self.tree.column("Request Date", width=80, minwidth=70)
        self.tree.column("Ingreso Por", width=80, minwidth=70)
        self.tree.column("Tipo", width=70, minwidth=60)
        self.tree.column("APP Name", width=120, minwidth=100)
        self.tree.column("Mail", width=100, minwidth=80)
        self.tree.column("Closing Date App", width=90, minwidth=80)
        self.tree.column("App Quality", width=80, minwidth=70)
        self.tree.column("Confirmation by User", width=100, minwidth=90)
        self.tree.column("Comment", width=80, minwidth=70)
        
        # Scrollbar vertical para treeview
        tree_scrollbar_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set)
        
        # Scrollbar horizontal para treeview
        tree_scrollbar_x = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=tree_scrollbar_x.set)
        
        # Empaquetar treeview y scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar_y.grid(row=0, column=1, sticky="ns")
        tree_scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Binding para selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_registro)
        
        # Empaquetar canvas y scrollbar principal
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar el canvas para que se expanda (reducir altura para dar más espacio a la tabla)
        canvas.configure(width=1200, height=400)
        
        # Binding para scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
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
    
    def buscar_por_sid(self):
        """Busca registros por SID usando la base de datos"""
        sid = self.variables['sid_busqueda'].get().strip()
        if not sid:
            messagebox.showwarning("Advertencia", "Por favor ingrese un SID para buscar")
            return
        
        try:
            if self.service and hasattr(self.service, 'buscar_procesos'):
                # Buscar en la base de datos
                filtros = {'sid': sid}
                resultados = self.service.buscar_procesos(filtros)
                self.mostrar_resultados_busqueda(resultados, f"SID: {sid}")
            else:
                messagebox.showerror("Error", "Servicio no disponible para búsqueda")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
            print(f"Error en buscar_por_sid: {e}")
    
    def mostrar_resultados_busqueda(self, resultados, busqueda):
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
            if self.service and hasattr(self.service, 'buscar_procesos'):
                # Buscar todos los registros
                resultados = self.service.buscar_procesos()
                self.mostrar_resultados_busqueda(resultados, "todos los registros")
            else:
                messagebox.showerror("Error", "Servicio no disponible para búsqueda")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
            print(f"Error en buscar_todos_los_registros: {e}")
    
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
            'coca': tk.StringVar(),
            'skip_level': tk.StringVar(),
            'coleadores': tk.StringVar(),
            'parents': tk.StringVar(),
            'personal_email': tk.StringVar(),
            'size': tk.StringVar(),
            'birthday': tk.StringVar(),
            'ubicacion': tk.StringVar(),
            'activo': tk.StringVar(value="Activo"),
            # Campos para filtros
            'filtro_texto': tk.StringVar(),
            'columna_filtro': tk.StringVar(value="scotia_id")
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
                  style="Title.TLabel").grid(row=0, column=0, pady=20, sticky="ew")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(len([
            ("SID:", "sid", "entry"),
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
        
        # Campos del formulario - Actualizados para coincidir con tabla headcount
        campos = [
            # Campos obligatorios
            ("Scotia ID:", "scotia_id", "entry"),
            ("Employee:", "employee", "entry"),
            ("Full Name:", "full_name", "entry"),
            ("Email:", "email", "entry"),
            
            # Campos de posición y organización
            ("Position:", "position", "entry"),
            ("Manager:", "manager", "entry"),
            ("Senior Manager:", "senior_manager", "entry"),
            ("Unit:", "unit", "combobox", ["Tecnología", "Recursos Humanos", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Start Date:", "start_date", "entry"),
            
            # Campos adicionales
            ("COCA:", "coca", "entry"),
            ("Skip Level:", "skip_level", "entry"),
            ("Coleadores:", "coleadores", "entry"),
            ("Parents:", "parents", "entry"),
            ("Personal Email:", "personal_email", "entry"),
            ("Size:", "size", "combobox", ["XS", "S", "M", "L", "XL"]),
            ("Birthday:", "birthday", "entry"),
            ("Ubicación:", "ubicacion", "entry"),
            ("Estado:", "activo", "combobox", ["Activo", "Inactivo"])
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 15))
            
            if tipo == "entry":
                ttk.Entry(main_frame, textvariable=self.variables[var_name], width=50).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(main_frame, textvariable=self.variables[var_name], 
                            values=valores, width=47).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), pady=5
                )
        
        # Frame para búsqueda
        busqueda_frame = ttk.LabelFrame(main_frame, text="Búsqueda de Personas", padding="15")
        busqueda_frame.grid(row=len(campos), column=0, columnspan=2, pady=20, sticky="ew")
        
        # Campo de búsqueda por SID
        ttk.Label(busqueda_frame, text="Buscar por SID:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.sid_busqueda = ttk.Entry(busqueda_frame, width=30)
        self.sid_busqueda.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(0, 10))
        
        # Botones de búsqueda
        botones_busqueda_frame = ttk.Frame(busqueda_frame)
        botones_busqueda_frame.grid(row=0, column=2, pady=5)
        
        ttk.Button(botones_busqueda_frame, text="Buscar por SID", 
                  command=self.buscar_por_sid).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_busqueda_frame, text="Mostrar Todos", 
                  command=self.mostrar_todos).pack(side=tk.LEFT, padx=5)
        
        # Sección de filtrado avanzado
        filtro_frame = ttk.LabelFrame(busqueda_frame, text="Filtrado Avanzado", padding="15")
        filtro_frame.grid(row=1, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        filtro_frame.columnconfigure(1, weight=1)
        
        # Filtro por texto con selección de columna
        ttk.Label(filtro_frame, text="Filtrar por:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 15))
        
        # Combobox para seleccionar columna
        columnas_filtro = [
            "SID", "Nombre", "Apellido", "Email", "Departamento", "Cargo", "Estado"
        ]
        columna_combobox = ttk.Combobox(filtro_frame, textvariable=self.variables['columna_filtro'], 
                                       values=columnas_filtro, width=20, state="readonly")
        columna_combobox.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(0, 15))
        
        # Input para el texto del filtro
        filtro_entry = ttk.Entry(filtro_frame, textvariable=self.variables['filtro_texto'], 
                 width=40)
        filtro_entry.grid(row=0, column=2, sticky=(tk.W, tk.E), pady=8, padx=(0, 15))
        
        # Tooltip informativo
        ttk.Label(filtro_frame, text="💡 Escriba para filtrar en tiempo real", 
                 style="Normal.TLabel", foreground="gray").grid(
            row=1, column=2, sticky=tk.W, pady=(2, 0)
        )
        
        # Binding para filtrado en tiempo real (con delay)
        self.filtro_delay_id = None
        filtro_entry.bind('<KeyRelease>', self._on_filtro_change)
        
        # Botón para aplicar filtro
        ttk.Button(filtro_frame, text="🔍 Aplicar Filtro", 
                  command=self.aplicar_filtro).grid(
            row=0, column=3, padx=(15, 0), pady=8
        )
        
        # Botón para limpiar filtro
        ttk.Button(filtro_frame, text="🧹 Limpiar Filtro", 
                  command=self.limpiar_filtro).grid(
            row=2, column=0, columnspan=4, pady=(15, 0)
        )
        
        # Tabla de resultados
        resultados_frame = ttk.Frame(busqueda_frame)
        resultados_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0), sticky="ew")
        
        # Crear Treeview para mostrar resultados
        self.tree = ttk.Treeview(resultados_frame, columns=("SID", "Nombre", "Apellido", "Email", "Departamento", "Cargo", "Estado"), 
                                show="headings", height=6)
        
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
        
        # Botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=20)
        
        ttk.Button(botones_frame, text="Crear Persona", command=self.crear_persona).pack(side=tk.LEFT, padx=10)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=10)
        
        # Empaquetar canvas y scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar el canvas para que se expanda
        canvas.configure(width=1000, height=700)  # Aumentar altura para acomodar la tabla
        
        # Binding para scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def buscar_por_sid(self):
        """Busca una persona por SID"""
        sid = self.sid_busqueda.get().strip()
        if not sid:
            messagebox.showwarning("Advertencia", "Por favor ingrese un SID para buscar")
            return
        
        try:
            # Buscar en la base de datos real
            resultados = self.service.buscar_headcount_por_sid(sid)
            self.mostrar_resultados_busqueda(resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
    
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
                self.tree.insert("", "end", values=(
                    resultado.get('employee', ''),
                    resultado.get('full_name', ''),
                    resultado.get('email', ''),
                    resultado.get('position', ''),
                    resultado.get('manager', ''),
                    resultado.get('unit', ''),
                    'Activo' if resultado.get('activo', True) else 'Inactivo'
                ))
    
    
    
    def crear_persona(self):
        """Crea una nueva persona en el headcount usando el nuevo servicio"""
        # Validación local
        campos_vacios = self.validar_campos_obligatorios()
        if campos_vacios:
            messagebox.showerror("Error", f"Por favor complete los campos obligatorios: {', '.join(campos_vacios)}")
            return
        
        # Obtener datos del formulario
        datos = self.obtener_datos()
        
        # Preparar datos para el nuevo servicio
        empleado_data = {
            'scotia_id': datos.get('scotia_id', ''),
            'employee': datos.get('employee', ''),
            'full_name': datos.get('full_name', ''),
            'email': datos.get('email', ''),
            'position': datos.get('position', ''),
            'manager': datos.get('manager', ''),
            'senior_manager': datos.get('senior_manager', ''),
            'unit': datos.get('unit', ''),
            'start_date': datos.get('start_date', ''),
            'coca': datos.get('coca', ''),
            'skip_level': datos.get('skip_level', ''),
            'coleadores': datos.get('coleadores', ''),
            'parents': datos.get('parents', ''),
            'personal_email': datos.get('personal_email', ''),
            'size': datos.get('size', ''),
            'birthday': datos.get('birthday', ''),
            'ubicacion': datos.get('ubicacion', ''),
            'activo': datos.get('activo', 'Activo') == 'Activo'
        }
        
        # Usar el nuevo servicio de gestión de accesos
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
            from access_management_service import access_service
            
            success, message = access_service.create_employee(empleado_data)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.limpiar()
                # Actualizar la tabla después de crear
                self.mostrar_todos()
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
    
    def mostrar_resultados_busqueda(self, resultados, busqueda=""):
        """Muestra los resultados de búsqueda en la tabla"""
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                self.tree.insert("", "end", values=(
                    resultado.get('employee', ''),
                    resultado.get('full_name', ''),
                    resultado.get('email', ''),
                    resultado.get('position', ''),
                    resultado.get('manager', ''),
                    resultado.get('unit', ''),
                    'Activo' if resultado.get('activo', True) else 'Inactivo'
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
