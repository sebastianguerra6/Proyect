import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from models import Empleado, Onboarding, Offboarding, LateralMovement
from data import EmpleadoRepository
from services import EmpleadoService
from ui import CamposGeneralesFrame, OnboardingFrame, OffboardingFrame, LateralMovementFrame

class AppEmpleadosRefactorizada:
    """Aplicación principal refactorizada siguiendo buenas prácticas de POO"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Empleados - Refactorizado")
        self.root.geometry("800x600")
        
        # Inicializar servicios y componentes
        self.repository = EmpleadoRepository()
        self.service = EmpleadoService(self.repository)
        
        # Variables de control
        self.tipo_proceso_var = tk.StringVar()
        
        # Componentes de UI
        self.componentes = {}
        
        # Crear interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea la interfaz principal de la aplicación"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Gestión de Empleados", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos generales
        self.componentes['generales'] = CamposGeneralesFrame(main_frame)
        self.componentes['generales'].frame.grid(row=1, column=0, columnspan=2, 
                                               sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Pestañas
        self.crear_pestanas(main_frame)
        
        # Botones
        self.crear_botones(main_frame)
        
    def crear_pestanas(self, parent):
        """Crea el sistema de pestañas"""
        # Frame para pestañas
        pestanas_frame = ttk.LabelFrame(parent, text="Tipo de Proceso", padding="10")
        pestanas_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                           pady=(0, 10))
        pestanas_frame.columnconfigure(0, weight=1)
        pestanas_frame.rowconfigure(1, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(pestanas_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Pestaña de selección
        self.crear_pestana_seleccion()
        
        # Inicializar pestañas dinámicas como None
        self.pestanas_dinamicas = {
            'onboarding': None,
            'offboarding': None,
            'lateral': None
        }
        
    def crear_pestana_seleccion(self):
        """Crea la pestaña de selección de tipo de proceso"""
        seleccion_frame = ttk.Frame(self.notebook)
        self.notebook.add(seleccion_frame, text="Seleccionar Proceso")
        
        # Título
        ttk.Label(seleccion_frame, text="Seleccione el tipo de proceso:", 
                  font=("Arial", 12, "bold")).pack(pady=20)
        
        # Opciones
        opciones_frame = ttk.Frame(seleccion_frame)
        opciones_frame.pack(pady=20)
        
        # Radio buttons
        opciones = [
            ("Onboarding", "onboarding"),
            ("Offboarding", "offboarding"),
            ("Lateral Movement", "lateral")
        ]
        
        for texto, valor in opciones:
            ttk.Radiobutton(opciones_frame, text=texto, 
                           variable=self.tipo_proceso_var, value=valor,
                           command=self.cambiar_pestana).pack(anchor=tk.W, pady=5)
        
    def cambiar_pestana(self):
        """Cambia la pestaña según la selección del usuario"""
        # Ocultar todas las pestañas dinámicas
        for pestana in self.pestanas_dinamicas.values():
            if pestana:
                self.notebook.hide(pestana)
        
        tipo_seleccionado = self.tipo_proceso_var.get()
        
        # Mostrar pestaña correspondiente
        if tipo_seleccionado == "onboarding":
            if not self.pestanas_dinamicas['onboarding']:
                self.crear_pestana_onboarding()
            self.notebook.add(self.pestanas_dinamicas['onboarding'], text="Onboarding")
            
        elif tipo_seleccionado == "offboarding":
            if not self.pestanas_dinamicas['offboarding']:
                self.crear_pestana_offboarding()
            self.notebook.add(self.pestanas_dinamicas['offboarding'], text="Offboarding")
            
        elif tipo_seleccionado == "lateral":
            if not self.pestanas_dinamicas['lateral']:
                self.crear_pestana_lateral()
            self.notebook.add(self.pestanas_dinamicas['lateral'], text="Lateral Movement")
    
    def crear_pestana_onboarding(self):
        """Crea la pestaña de onboarding"""
        self.componentes['onboarding'] = OnboardingFrame(self.notebook)
        self.pestanas_dinamicas['onboarding'] = self.componentes['onboarding'].frame
    
    def crear_pestana_offboarding(self):
        """Crea la pestaña de offboarding"""
        self.componentes['offboarding'] = OffboardingFrame(self.notebook)
        self.pestanas_dinamicas['offboarding'] = self.componentes['offboarding'].frame
    
    def crear_pestana_lateral(self):
        """Crea la pestaña de lateral movement"""
        self.componentes['lateral'] = LateralMovementFrame(self.notebook)
        self.pestanas_dinamicas['lateral'] = self.componentes['lateral'].frame
    
    def crear_botones(self, parent):
        """Crea los botones de acción"""
        # Frame para botones
        botones_frame = ttk.Frame(parent)
        botones_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Botones
        ttk.Button(botones_frame, text="Guardar", command=self.guardar_datos).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Estadísticas", command=self.mostrar_estadisticas).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def guardar_datos(self):
        """Guarda los datos del formulario"""
        # Obtener datos generales
        datos_generales = self.componentes['generales'].obtener_datos()
        
        # Validar campos obligatorios
        campos_vacios = self.componentes['generales'].validar_campos_obligatorios()
        if campos_vacios:
            messagebox.showerror("Error", f"Por favor complete los campos obligatorios: {', '.join(campos_vacios)}")
            return
        
        # Obtener tipo de proceso
        tipo_proceso = self.tipo_proceso_var.get()
        if not tipo_proceso:
            messagebox.showerror("Error", "Por favor seleccione un tipo de proceso")
            return
        
        # Obtener datos específicos según el tipo
        datos_especificos = {}
        if tipo_proceso in self.componentes:
            datos_especificos = self.componentes[tipo_proceso].obtener_datos()
        
        # Guardar usando el servicio
        exito, mensaje = self.service.guardar_proceso(tipo_proceso, datos_generales, datos_especificos)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        # Limpiar campos generales
        self.componentes['generales'].limpiar()
        
        # Limpiar campos específicos
        for componente in self.componentes.values():
            if hasattr(componente, 'limpiar'):
                componente.limpiar()
        
        # Limpiar selección de tipo de proceso
        self.tipo_proceso_var.set("")
        
        # Ocultar pestañas dinámicas
        for pestana in self.pestanas_dinamicas.values():
            if pestana:
                self.notebook.hide(pestana)
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de los datos almacenados"""
        estadisticas = self.service.obtener_estadisticas()
        
        mensaje = "Estadísticas de la aplicación:\n\n"
        mensaje += f"Onboardings: {estadisticas['onboarding']}\n"
        mensaje += f"Offboardings: {estadisticas['offboarding']}\n"
        mensaje += f"Lateral Movements: {estadisticas['lateral']}\n"
        mensaje += f"Total: {sum(estadisticas.values())}"
        
        messagebox.showinfo("Estadísticas", mensaje)

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AppEmpleadosRefactorizada(root)
    root.mainloop()

if __name__ == "__main__":
    main()
