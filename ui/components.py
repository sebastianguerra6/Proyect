import tkinter as tk
from tkinter import ttk
from datetime import datetime

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
