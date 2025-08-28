import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from models import Empleado
from data import EmpleadoRepository
from services import EmpleadoService
from ui import (CamposGeneralesFrame, OnboardingFrame, OffboardingFrame, 
                LateralMovementFrame, EdicionBusquedaFrame, CreacionPersonaFrame)

class AppEmpleadosRefactorizada:
    """Aplicación principal refactorizada siguiendo buenas prácticas de POO"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Empleados - Refactorizado")
        self.root.geometry("1200x700")  # Aumentar ancho para aprovechar mejor la pantalla
        
        # 🔹 Centrar la ventana (usando el tamaño que ya definiste)
        self._centrar_ventana(1200, 700)
        
        # Inicializar servicios y componentes
        self.repository = EmpleadoRepository()
        self.service = EmpleadoService(self.repository)
        
        # Variables de control
        self.tipo_proceso_var = tk.StringVar()
        
        # Componentes de UI
        self.componentes = {}
        
        # Crear interfaz
        self.crear_interfaz()
    
    def _centrar_ventana(self, w=None, h=None):
        """Centra la ventana principal en la pantalla."""
        self.root.update_idletasks()
        if w is None or h is None:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        # Forzar el centrado después de un pequeño delay
        self.root.after(100, self._forzar_centrado)
    
    def _forzar_centrado(self):
        """Fuerza el centrado de la ventana"""
        self.root.update_idletasks()
        w = 1200
        h = 700
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
    def crear_interfaz(self):
        """Crea la interfaz principal de la aplicación"""
        # Frame principal con centrado
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Reducir padx de 50 a 20
        
        # Configurar grid para centrado
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título centrado
        titulo = ttk.Label(main_frame, text="Sistema de Gestión de Empleados", 
                          font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, pady=(0, 30), sticky="ew")
        
        # Pestañas principales
        self.crear_pestanas_principales(main_frame)
        
    def crear_pestanas_principales(self, parent):
        """Crea el sistema de pestañas principales"""
        # Frame para pestañas principales con centrado
        pestanas_principales_frame = ttk.Frame(parent)
        pestanas_principales_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)  # Reducir padx de 20 a 10
        pestanas_principales_frame.columnconfigure(0, weight=1)
        pestanas_principales_frame.rowconfigure(0, weight=1)
        
        # Notebook para pestañas principales
        self.notebook_principal = ttk.Notebook(pestanas_principales_frame)
        self.notebook_principal.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Reducir padx de 10 a 5
        
        # Pestaña de Gestión de Procesos
        self.crear_pestana_gestion_procesos()
        
        # Pestaña de Edición y Búsqueda
        self.crear_pestana_edicion_busqueda()
        
        # Pestaña de Creación de Persona
        self.crear_pestana_creacion_persona()
        
    def crear_pestana_gestion_procesos(self):
        """Crea la pestaña de gestión de procesos (onboarding, offboarding, lateral)"""
        gestion_frame = ttk.Frame(self.notebook_principal)
        self.notebook_principal.add(gestion_frame, text="Gestión de Procesos")
        
        # Configurar grid para centrado
        gestion_frame.columnconfigure(0, weight=1)
        gestion_frame.rowconfigure(0, weight=1)
        
        # Crear canvas con scrollbar
        canvas = tk.Canvas(gestion_frame, bg="white")
        scrollbar = ttk.Scrollbar(gestion_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Centrar el contenido en el canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar grid del frame scrolleable para centrado
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)  # Agregar columna para el lado derecho
        scrollable_frame.rowconfigure(1, weight=1)
        
        # Frame para organizar los componentes lado a lado
        contenido_frame = ttk.Frame(scrollable_frame)
        contenido_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        contenido_frame.columnconfigure(0, weight=1)
        contenido_frame.columnconfigure(1, weight=1)
        contenido_frame.columnconfigure(2, weight=0)  # Agregar columna para botones
        
        # Centrar el contenido en el frame
        contenido_frame.columnconfigure(0, weight=0)  # Cambiar a weight=0 para centrar
        contenido_frame.columnconfigure(1, weight=0)  # Cambiar a weight=0 para centrar
        contenido_frame.columnconfigure(2, weight=0)  # Botones sin peso
        
        # Campos generales (centrado)
        self.componentes['generales'] = CamposGeneralesFrame(contenido_frame)
        self.componentes['generales'].frame.grid(row=0, column=0, 
                                               sticky="ew", pady=(0, 20), padx=(20, 10))  # Aumentar padding izquierdo
        
        # Pestañas de tipo de proceso (centrado)
        self.crear_pestanas_tipo_proceso(contenido_frame)
        
        # Botones (a la derecha del frame de tipo de proceso)
        self.crear_botones(contenido_frame)
        
        # Empaquetar canvas y scrollbar con centrado
        canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=20)  # Reducir padx de 20 a 10
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar el canvas para que se expanda y centre
        canvas.configure(width=1250, height=650)  # Aumentar ancho para mejor centrado
        
        # Binding para scroll con mouse - corregido
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind del scroll del mouse al canvas específico
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
    def crear_pestanas_tipo_proceso(self, parent):
        """Crea el sistema de pestañas para tipos de proceso"""
        # Frame para pestañas con centrado
        pestanas_frame = ttk.LabelFrame(parent, text="Tipo de Proceso", padding="20")
        pestanas_frame.grid(row=0, column=1, sticky="ew", pady=(0, 20), padx=(10, 20))  # Aumentar padding derecho
        pestanas_frame.columnconfigure(0, weight=1)
        pestanas_frame.rowconfigure(1, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(pestanas_frame)
        self.notebook.grid(row=1, column=0, sticky="ew", pady=(15, 0), padx=10)  # Reducir padx de 20 a 10
        
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
        
        # Configurar grid para centrado
        seleccion_frame.columnconfigure(0, weight=1)
        seleccion_frame.rowconfigure(1, weight=1)
        
        # Título centrado
        ttk.Label(seleccion_frame, text="Seleccione el tipo de proceso:", 
                  font=("Arial", 14, "bold")).grid(row=0, column=0, pady=30, sticky="ew")
        
        # Opciones centradas
        opciones_frame = ttk.Frame(seleccion_frame)
        opciones_frame.grid(row=1, column=0, pady=20, sticky="ew")
        opciones_frame.columnconfigure(0, weight=1)
        
        # Radio buttons centrados
        opciones = [
            ("Onboarding", "onboarding"),
            ("Offboarding", "offboarding"),
            ("Lateral Movement", "lateral")
        ]
        
        for i, (texto, valor) in enumerate(opciones):
            ttk.Radiobutton(opciones_frame, text=texto, 
                           variable=self.tipo_proceso_var, value=valor,
                           command=self.cambiar_pestana).grid(row=i, column=0, pady=8, sticky="ew")
        
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
    
    def crear_pestana_edicion_busqueda(self):
        """Crea la pestaña de edición y búsqueda"""
        self.componentes['edicion_busqueda'] = EdicionBusquedaFrame(self.notebook_principal, self.service)
        self.notebook_principal.add(self.componentes['edicion_busqueda'].frame, text="Edición y Búsqueda")
        
    def crear_pestana_creacion_persona(self):
        """Crea la pestaña de creación de persona"""
        self.componentes['creacion_persona'] = CreacionPersonaFrame(self.notebook_principal, self.service)
        self.notebook_principal.add(self.componentes['creacion_persona'].frame, text="Crear Persona")
    
    def crear_botones(self, parent):
        """Crea los botones de acción"""
        # Frame para botones a la derecha
        botones_frame = ttk.Frame(parent)
        botones_frame.grid(row=0, column=2, pady=30, padx=(20, 0), sticky="n")  # Aumentar padding izquierdo
        botones_frame.columnconfigure(0, weight=1)
        
        # Botones apilados verticalmente
        ttk.Button(botones_frame, text="Guardar", command=self.guardar_datos).grid(row=0, column=0, pady=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_campos).grid(row=1, column=0, pady=5)
        ttk.Button(botones_frame, text="Estadísticas", command=self.mostrar_estadisticas).grid(row=2, column=0, pady=5)
        ttk.Button(botones_frame, text="Salir", command=self.root.quit).grid(row=3, column=0, pady=5)
    
    def guardar_datos(self):
        """Guarda los datos del formulario en la base de datos"""
        try:
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
            
            # Generar número de caso único
            from models import Empleado
            empleado_temp = Empleado(
                sid=datos_generales.get('sid', ''),
                nueva_sub_unidad=datos_generales.get('nueva_sub_unidad', ''),
                nuevo_cargo=datos_generales.get('nuevo_cargo', ''),
                ingreso_por=datos_generales.get('ingreso_por', ''),
                request_date=datos_generales.get('request_date'),
                fecha=datos_generales.get('fecha'),
                status=datos_generales.get('status', 'Pendiente')
            )
            
            # Combinar datos generales con específicos y agregar número de caso
            datos_completos = {**datos_generales, **datos_especificos}
            datos_completos['numero_caso'] = empleado_temp.numero_caso
            datos_completos['tipo_proceso'] = tipo_proceso
            
            # Guardar en la base de datos usando el repository directamente
            exito, mensaje = self.repository.guardar_proceso(datos_completos, tipo_proceso)
            
            if exito:
                messagebox.showinfo("Éxito", f"{mensaje}\nNúmero de caso: {empleado_temp.numero_caso}")
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            print(f"Error en guardar_datos: {e}")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        try:
            # Limpiar campos generales
            if 'generales' in self.componentes:
                self.componentes['generales'].limpiar()
            
            # Limpiar campos específicos
            for componente in self.componentes.values():
                if hasattr(componente, 'limpiar'):
                    componente.limpiar()
            
            # Limpiar selección de tipo de proceso
            self.tipo_proceso_var.set("")
            
            # Ocultar pestañas dinámicas
            if hasattr(self, 'pestanas_dinamicas'):
                for pestana in self.pestanas_dinamicas.values():
                    if pestana:
                        self.notebook.hide(pestana)
                        
        except Exception as e:
            print(f"Error en limpiar_campos: {e}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de los datos almacenados en la base de datos"""
        try:
            estadisticas = self.repository.obtener_estadisticas()
            
            mensaje = "Estadísticas de la aplicación:\n\n"
            mensaje += f"Onboardings: {estadisticas.get('onboarding', 0)}\n"
            mensaje += f"Offboardings: {estadisticas.get('offboarding', 0)}\n"
            mensaje += f"Lateral Movements: {estadisticas.get('lateral_movement', 0)}\n"
            mensaje += f"Personas en Headcount: {estadisticas.get('headcount', 0)}\n"
            mensaje += f"Total: {sum(estadisticas.values())}"
            
            messagebox.showinfo("Estadísticas", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo estadísticas: {str(e)}")
            print(f"Error en mostrar_estadisticas: {e}")

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AppEmpleadosRefactorizada(root)
    root.mainloop()

if __name__ == "__main__":
    main()
