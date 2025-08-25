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
            'area': tk.StringVar(),
            'subarea': tk.StringVar(),
            'ingreso_por': tk.StringVar(),
            'fecha': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.LabelFrame(self.parent, text="Información General", padding="10")
        self.frame.columnconfigure(1, weight=1)
        
        # Campos
        campos = [
            ("SID:", "sid", "entry"),
            ("Área:", "area", "combobox", ["Recursos Humanos", "Tecnología", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Subárea:", "subarea", "entry"),
            ("Quien hace el ingreso:", "ingreso_por", "combobox", ["Juan Pérez", "María García"]),
            ("Fecha:", "fecha", "entry")
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(self.frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
            
            if tipo == "entry":
                ttk.Entry(self.frame, textvariable=self.variables[var_name], width=30).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(self.frame, textvariable=self.variables[var_name], 
                            values=valores, width=27).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for var in self.variables.values():
            var.set("")
        self.variables['fecha'].set(datetime.now().strftime("%Y-%m-%d"))
    
    def validar_campos_obligatorios(self):
        """Valida que los campos obligatorios estén completos"""
        campos_obligatorios = ['sid', 'area']
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
        
        # Título
        ttk.Label(self.frame, text="Tipo de Onboarding", 
                  font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para radio buttons
        radio_frame = ttk.Frame(self.frame)
        radio_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Submenú con radio buttons
        opciones_submenu = ["Nuevo Empleado", "Recontratación", "Transferencia Interna", "Promoción"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(radio_frame, text=opcion, 
                           variable=self.variables['submenu_onboarding'], 
                           value=opcion).pack(anchor=tk.W, pady=5)
        
        # Opción Other con campo de texto
        other_frame = ttk.Frame(radio_frame)
        other_frame.pack(anchor=tk.W, pady=5)
        
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
        
        # Título
        ttk.Label(self.frame, text="Tipo de Offboarding", 
                  font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para radio buttons
        radio_frame = ttk.Frame(self.frame)
        radio_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Submenú con radio buttons
        opciones_submenu = ["Salida Definitiva", "Reducción de Personal", "Fin de Proyecto", "Cambio de Empresa"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(radio_frame, text=opcion, 
                           variable=self.variables['submenu_offboarding'], 
                           value=opcion).pack(anchor=tk.W, pady=5)
        
        # Opción Other con campo de texto
        other_frame = ttk.Frame(radio_frame)
        other_frame.pack(anchor=tk.W, pady=5)
        
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
        
        # Título
        ttk.Label(self.frame, text="Información de Lateral Movement", 
                  font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para campos
        campos_frame = ttk.Frame(self.frame)
        campos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        campos_frame.columnconfigure(1, weight=1)
        
        # Campo empleo anterior
        ttk.Label(campos_frame, text="Empleo Anterior:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(campos_frame, textvariable=self.variables['empleo_anterior'], width=30).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )
        
        # Título para radio buttons
        ttk.Label(campos_frame, text="Tipo de Movimiento:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(15, 5))
        
        # Submenú con radio buttons
        opciones_submenu = ["Movimiento Horizontal", "Reasignación de Proyecto", "Cambio de Equipo", "Rotación de Funciones"]
        for i, opcion in enumerate(opciones_submenu):
            ttk.Radiobutton(campos_frame, text=opcion, 
                           variable=self.variables['submenu_lateral'], 
                           value=opcion).grid(row=2+i, column=1, sticky=tk.W, pady=2)
        
        # Opción Other con campo de texto
        other_row = 2 + len(opciones_submenu)
        ttk.Radiobutton(campos_frame, text="Other:", 
                       variable=self.variables['submenu_lateral'], 
                       value="other").grid(row=other_row, column=0, sticky=tk.W, pady=2)
        
        ttk.Entry(campos_frame, textvariable=self.variables['other_lateral'], 
                 width=25).grid(row=other_row, column=1, sticky=tk.W, padx=(10, 0), pady=2)
    
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
            'sid_busqueda': tk.StringVar(),
            'area_edicion': tk.StringVar(),
            'subarea_edicion': tk.StringVar(),
            'ingreso_por_edicion': tk.StringVar(),
            'fecha_edicion': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        
        # Título
        ttk.Label(self.frame, text="Edición y Búsqueda de Registros", 
                  font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sección de búsqueda
        busqueda_frame = ttk.LabelFrame(main_frame, text="Búsqueda por SID", padding="10")
        busqueda_frame.pack(fill=tk.X, pady=(0, 20))
        busqueda_frame.columnconfigure(1, weight=1)
        
        ttk.Label(busqueda_frame, text="SID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(busqueda_frame, textvariable=self.variables['sid_busqueda'], width=30).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5
        )
        ttk.Button(busqueda_frame, text="Buscar", command=self.buscar_por_sid).grid(
            row=0, column=2, padx=(10, 0), pady=5
        )
        
        # Sección de edición
        edicion_frame = ttk.LabelFrame(main_frame, text="Edición de Campos", padding="10")
        edicion_frame.pack(fill=tk.X, pady=(0, 20))
        edicion_frame.columnconfigure(1, weight=1)
        
        campos_edicion = [
            ("Área:", "area_edicion", "combobox", ["Recursos Humanos", "Tecnología", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Subárea:", "subarea_edicion", "entry"),
            ("Quien hace el ingreso:", "ingreso_por_edicion", "combobox", ["Juan Pérez", "María García"]),
            ("Fecha:", "fecha_edicion", "entry")
        ]
        
        for i, campo in enumerate(campos_edicion):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(edicion_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=3)
            
            if tipo == "entry":
                ttk.Entry(edicion_frame, textvariable=self.variables[var_name], width=30).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=3
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(edicion_frame, textvariable=self.variables[var_name], 
                            values=valores, width=27).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=3
                )
        
        # Botones de acción
        botones_frame = ttk.Frame(edicion_frame)
        botones_frame.grid(row=len(campos_edicion), column=0, columnspan=2, pady=15)
        
        ttk.Button(botones_frame, text="Guardar Cambios", command=self.guardar_cambios).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=5)
        
        # Sección de resultados de búsqueda
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados de Búsqueda", padding="10")
        resultados_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview para mostrar resultados
        self.tree = ttk.Treeview(resultados_frame, columns=("SID", "Área", "Subárea", "Ingreso Por", "Fecha", "Tipo"), show="headings")
        
        # Configurar columnas
        self.tree.heading("SID", text="SID")
        self.tree.heading("Área", text="Área")
        self.tree.heading("Subárea", text="Subárea")
        self.tree.heading("Ingreso Por", text="Ingreso Por")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Tipo", text="Tipo")
        
        # Configurar anchos de columna
        self.tree.column("SID", width=100)
        self.tree.column("Área", width=120)
        self.tree.column("Subárea", width=120)
        self.tree.column("Ingreso Por", width=120)
        self.tree.column("Fecha", width=100)
        self.tree.column("Tipo", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(resultados_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar treeview y scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Binding para selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_registro)
    
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
    
    def mostrar_resultados_busqueda(self, resultados, sid):
        """Muestra los resultados reales de la búsqueda"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if resultados:
            for resultado in resultados:
                # Los datos del empleado están directamente en el resultado
                # porque el método to_dict() ya incluye todos los datos
                valores = (
                    resultado.get('sid', ''),
                    resultado.get('area', ''),
                    resultado.get('subarea', ''),
                    resultado.get('ingreso_por', ''),
                    resultado.get('fecha', ''),
                    resultado.get('tipo_proceso', '')
                )
                self.tree.insert("", "end", values=valores)
            
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} registros para el SID: {sid}")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron registros para el SID: {sid}")
    
    def simular_busqueda(self, sid):
        """Simula la búsqueda de registros (placeholder)"""
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Simular datos encontrados
        datos_simulados = [
            (sid, "Tecnología", "Desarrollo", "Juan Pérez", "2024-01-15", "Onboarding"),
            (sid, "Tecnología", "Desarrollo", "Juan Pérez", "2024-01-15", "Lateral Movement")
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
            if len(valores) >= 5:
                self.variables['area_edicion'].set(valores[1])
                self.variables['subarea_edicion'].set(valores[2])
                self.variables['ingreso_por_edicion'].set(valores[3])
                self.variables['fecha_edicion'].set(valores[4])
    
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
        
        # Título
        ttk.Label(self.frame, text="Crear Nueva Persona en Headcount", 
                  font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
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
            ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=3)
            
            if tipo == "entry":
                ttk.Entry(main_frame, textvariable=self.variables[var_name], width=35).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=3
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(main_frame, textvariable=self.variables[var_name], 
                            values=valores, width=32).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=3
                )
        
        # Botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        ttk.Button(botones_frame, text="Crear Persona", command=self.crear_persona).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=5)
    
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
