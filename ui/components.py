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
            'id': tk.StringVar(),
            'area': tk.StringVar(),
            'empleo': tk.StringVar(),
            'ingreso_por': tk.StringVar(),
            'fecha': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.LabelFrame(self.parent, text="Información General", padding="10")
        self.frame.columnconfigure(1, weight=1)
        
        # Campos
        campos = [
            ("ID:", "id", "entry"),
            ("Área:", "area", "entry"),
            ("Empleo:", "empleo", "entry"),
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
        campos_obligatorios = ['id', 'area', 'empleo']
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
            'fecha_ingreso': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'departamento_destino': tk.StringVar(),
            'supervisor': tk.StringVar(),
            'salario': tk.StringVar(),
            'tipo_contrato': tk.StringVar(),
            'observaciones': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        
        # Título
        ttk.Label(self.frame, text="Información de Onboarding", 
                  font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para campos
        campos_frame = ttk.Frame(self.frame)
        campos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        campos_frame.columnconfigure(1, weight=1)
        
        # Campos específicos
        campos = [
            ("Fecha de Ingreso:", "fecha_ingreso", "entry"),
            ("Departamento Destino:", "departamento_destino", "entry"),
            ("Supervisor:", "supervisor", "entry"),
            ("Salario:", "salario", "entry"),
            ("Tipo de Contrato:", "tipo_contrato", "combobox", 
             ["Indefinido", "Temporal", "Prácticas", "Otro"]),
            ("Observaciones:", "observaciones", "entry")
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(campos_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
            
            if tipo == "entry":
                ttk.Entry(campos_frame, textvariable=self.variables[var_name], width=30).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(campos_frame, textvariable=self.variables[var_name], 
                            values=valores).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for name, var in self.variables.items():
            if name == 'fecha_ingreso':
                var.set(datetime.now().strftime("%Y-%m-%d"))
            else:
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
            'fecha_salida': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'motivo_salida': tk.StringVar(),
            'tipo_salida': tk.StringVar(),
            'entrevista_salida': tk.StringVar(),
            'equipos_devueltos': tk.StringVar(),
            'observaciones': tk.StringVar()
        }
    
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        self.frame = ttk.Frame(self.parent)
        
        # Título
        ttk.Label(self.frame, text="Información de Offboarding", 
                  font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para campos
        campos_frame = ttk.Frame(self.frame)
        campos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        campos_frame.columnconfigure(1, weight=1)
        
        # Campos específicos
        campos = [
            ("Fecha de Salida:", "fecha_salida", "entry"),
            ("Motivo de Salida:", "motivo_salida", "combobox", 
             ["Renuncia", "Despido", "Fin de contrato", "Jubilación", "Otro"]),
            ("Tipo de Salida:", "tipo_salida", "combobox", 
             ["Voluntaria", "Involuntaria", "Mutuo acuerdo"]),
            ("Entrevista de Salida:", "entrevista_salida", "combobox", 
             ["Sí", "No", "Pendiente"]),
            ("Equipos Devueltos:", "equipos_devueltos", "combobox", 
             ["Completo", "Pendiente", "No aplica"]),
            ("Observaciones:", "observaciones", "entry")
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(campos_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
            
            if tipo == "entry":
                ttk.Entry(campos_frame, textvariable=self.variables[var_name], width=30).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(campos_frame, textvariable=self.variables[var_name], 
                            values=valores).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for name, var in self.variables.items():
            if name == 'fecha_salida':
                var.set(datetime.now().strftime("%Y-%m-%d"))
            else:
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
            'fecha_movimiento': tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            'departamento_origen': tk.StringVar(),
            'departamento_destino': tk.StringVar(),
            'cargo_anterior': tk.StringVar(),
            'cargo_nuevo': tk.StringVar(),
            'motivo_movimiento': tk.StringVar(),
            'observaciones': tk.StringVar()
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
        
        # Campos específicos
        campos = [
            ("Fecha de Movimiento:", "fecha_movimiento", "entry"),
            ("Departamento Origen:", "departamento_origen", "entry"),
            ("Departamento Destino:", "departamento_destino", "entry"),
            ("Cargo Anterior:", "cargo_anterior", "entry"),
            ("Cargo Nuevo:", "cargo_nuevo", "entry"),
            ("Motivo del Movimiento:", "motivo_movimiento", "combobox", 
             ["Promoción", "Reorganización", "Desarrollo profesional", "Necesidad del negocio", "Otro"]),
            ("Observaciones:", "observaciones", "entry")
        ]
        
        for i, campo in enumerate(campos):
            label_text, var_name, tipo = campo[:3]
            ttk.Label(campos_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
            
            if tipo == "entry":
                ttk.Entry(campos_frame, textvariable=self.variables[var_name], width=30).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
            elif tipo == "combobox":
                valores = campo[3] if len(campo) > 3 else []
                ttk.Combobox(campos_frame, textvariable=self.variables[var_name], 
                            values=valores).grid(
                    row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
                )
    
    def obtener_datos(self):
        """Obtiene los datos de los campos"""
        return {name: var.get() for name, var in self.variables.items()}
    
    def limpiar(self):
        """Limpia todos los campos"""
        for name, var in self.variables.items():
            if name == 'fecha_movimiento':
                var.set(datetime.now().strftime("%Y-%m-%d"))
            else:
                var.set("")
