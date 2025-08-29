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
        self.root.geometry("1400x700")  # Aumentar ancho para acomodar botones laterales
        
        # 🔹 Centrar la ventana (usando el tamaño que ya definiste)
        self._centrar_ventana(1400, 700)
        
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
        
    def crear_interfaz(self):
        """Crea la interfaz principal de la aplicación"""
        # Frame principal con nueva disposición
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configurar grid para nueva disposición
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=0)  # Botones laterales (sin peso)
        main_frame.columnconfigure(1, weight=1)  # Contenido principal (se expande)
        main_frame.rowconfigure(0, weight=0)  # Título (sin peso)
        main_frame.rowconfigure(1, weight=1)  # Contenido (se expande)
        
        # Título centrado en la parte superior
        titulo = ttk.Label(main_frame, text="Sistema de Gestión de Empleados", 
                          font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="ew")
        
        # Configurar el título para que se vea
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Botones laterales y contenido principal
        self.crear_botones_laterales(main_frame)
        self.crear_contenido_principal(main_frame)
    
    def crear_pestanas_principales(self, parent):
        """Método obsoleto - reemplazado por botones laterales"""
        pass
        
    def crear_pestana_gestion_procesos(self):
        """Método obsoleto - reemplazado por crear_componente_gestion"""
        pass
        
    def crear_pestana_edicion_busqueda(self):
        """Método obsoleto - reemplazado por crear_componente_edicion"""
        pass
        
    def crear_pestana_creacion_persona(self):
        """Método obsoleto - reemplazado por crear_componente_creacion"""
        pass
    
    def crear_pestanas_tipo_proceso(self, parent):
        """Crea el sistema de pestañas para tipos de proceso"""
        # Frame para pestañas con centrado
        pestanas_frame = ttk.LabelFrame(parent, text="Tipo de Proceso", padding="20")
        pestanas_frame.grid(row=1, column=1, sticky="ew", pady=(0, 20), padx=(10, 20))  # Cambiar a row=1
        pestanas_frame.columnconfigure(0, weight=1)
        pestanas_frame.rowconfigure(1, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(pestanas_frame)
        self.notebook.grid(row=1, column=0, sticky="ew", pady=(15, 0), padx=10)
        
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
        try:
            self.componentes['onboarding'] = OnboardingFrame(self.notebook)
            self.pestanas_dinamicas['onboarding'] = self.componentes['onboarding'].frame
        except Exception as e:
            print(f"Error creando pestaña onboarding: {e}")
            # Crear un frame básico como fallback
            fallback_frame = ttk.Frame(self.notebook)
            ttk.Label(fallback_frame, text="Error cargando Onboarding", 
                     font=("Arial", 12, "bold")).pack(pady=20)
            self.componentes['onboarding'] = type('FallbackFrame', (), {
                'frame': fallback_frame,
                'obtener_datos': lambda: {}
            })()
            self.pestanas_dinamicas['onboarding'] = fallback_frame
    
    def crear_pestana_offboarding(self):
        """Crea la pestaña de offboarding"""
        try:
            self.componentes['offboarding'] = OffboardingFrame(self.notebook)
            self.pestanas_dinamicas['offboarding'] = self.componentes['offboarding'].frame
        except Exception as e:
            print(f"Error creando pestaña offboarding: {e}")
            # Crear un frame básico como fallback
            fallback_frame = ttk.Frame(self.notebook)
            ttk.Label(fallback_frame, text="Error cargando Offboarding", 
                     font=("Arial", 12, "bold")).pack(pady=20)
            self.componentes['offboarding'] = type('FallbackFrame', (), {
                'frame': fallback_frame,
                'obtener_datos': lambda: {}
            })()
            self.pestanas_dinamicas['offboarding'] = fallback_frame
    
    def crear_pestana_lateral(self):
        """Crea la pestaña de lateral movement"""
        try:
            self.componentes['lateral'] = LateralMovementFrame(self.notebook)
            self.pestanas_dinamicas['lateral'] = self.componentes['lateral'].frame
        except Exception as e:
            print(f"Error creando pestaña lateral: {e}")
            # Crear un frame básico como fallback
            fallback_frame = ttk.Frame(self.notebook)
            ttk.Label(fallback_frame, text="Error cargando Lateral Movement", 
                     font=("Arial", 12, "bold")).pack(pady=20)
            self.componentes['lateral'] = type('FallbackFrame', (), {
                'frame': fallback_frame,
                'obtener_datos': lambda: {}
            })()
            self.pestanas_dinamicas['lateral'] = fallback_frame
    
    def crear_botones(self, parent):
        """Crea los botones de acción"""
        # Frame para botones a la derecha
        botones_frame = ttk.Frame(parent)
        botones_frame.grid(row=1, column=2, pady=30, padx=(20, 0), sticky="n")  # Cambiar a row=1
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
            if 'generales' not in self.componentes:
                messagebox.showerror("Error", "No se encontró el componente de campos generales")
                return
                
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
                try:
                    if hasattr(self.componentes[tipo_proceso], 'obtener_datos'):
                        datos_especificos = self.componentes[tipo_proceso].obtener_datos()
                    else:
                        print(f"Advertencia: {tipo_proceso} no tiene método obtener_datos")
                        datos_especificos = {}
                except Exception as e:
                    print(f"Error obteniendo datos específicos de {tipo_proceso}: {e}")
                    datos_especificos = {}
            
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
            
            print(f"Datos a guardar: {datos_completos}")  # Debug
            
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
            import traceback
            traceback.print_exc()
    
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

    def crear_botones_laterales(self, parent):
        """Crea los botones laterales para navegación"""
        # Frame para botones laterales
        botones_frame = ttk.LabelFrame(parent, text="Navegación", padding="15")
        botones_frame.grid(row=1, column=0, sticky="n", padx=(0, 20), pady=(0, 20))
        botones_frame.columnconfigure(0, weight=1)
        
        # Botones de navegación
        opciones = [
            ("Gestión de Procesos", "gestion"),
            ("Edición y Búsqueda", "edicion"),
            ("Crear Persona", "creacion")
        ]
        
        self.botones_navegacion = {}
        for i, (texto, valor) in enumerate(opciones):
            btn = ttk.Button(botones_frame, text=texto, width=20,
                           command=lambda v=valor: self.cambiar_contenido(v))
            btn.grid(row=i, column=0, pady=8, sticky="ew")
            self.botones_navegacion[valor] = btn
        
        # Seleccionar gestión por defecto
        self.cambiar_contenido("gestion")

    def crear_contenido_principal(self, parent):
        """Crea el frame principal para mostrar el contenido"""
        # Frame para contenido principal
        self.contenido_principal_frame = ttk.Frame(parent)
        self.contenido_principal_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=(0, 20))
        self.contenido_principal_frame.columnconfigure(0, weight=1)
        self.contenido_principal_frame.rowconfigure(0, weight=1)
        
        # Inicializar componentes
        self.componentes = {}
        
        # Crear todos los componentes pero no mostrarlos aún
        self.crear_componente_gestion()
        self.crear_componente_edicion()
        self.crear_componente_creacion()
    
    def crear_componente_gestion(self):
        """Crea el componente de gestión de procesos"""
        gestion_frame = ttk.Frame(self.contenido_principal_frame)
        gestion_frame.columnconfigure(0, weight=1)
        gestion_frame.rowconfigure(0, weight=0)  # Título (sin peso)
        gestion_frame.rowconfigure(1, weight=1)  # Contenido (se expande)
        
        # Título de la sección
        titulo_gestion = ttk.Label(gestion_frame, text="Gestión de Procesos", 
                                  font=("Arial", 16, "bold"))
        titulo_gestion.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Frame principal para el contenido (sin scroll)
        contenido_frame = ttk.Frame(gestion_frame)
        contenido_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        contenido_frame.columnconfigure(0, weight=0)  # Campos generales
        contenido_frame.columnconfigure(1, weight=1)  # Tipo de proceso
        contenido_frame.columnconfigure(2, weight=0)  # Botones
        
        # Título interno para mejor organización
        titulo_interno = ttk.Label(contenido_frame, text="Complete la información del proceso", 
                                 font=("Arial", 12, "bold"), foreground="darkblue")
        titulo_interno.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        
        # Campos generales
        self.componentes['generales'] = CamposGeneralesFrame(contenido_frame)
        self.componentes['generales'].frame.grid(row=1, column=0, 
                                               sticky="ew", pady=(0, 15), padx=(20, 10))
        
        # Pestañas de tipo de proceso
        self.crear_pestanas_tipo_proceso(contenido_frame)
        
        # Botones
        self.crear_botones(contenido_frame)
        
        # Guardar referencia al frame
        self.componentes['gestion_frame'] = gestion_frame
    
    def crear_componente_edicion(self):
        """Crea el componente de edición y búsqueda"""
        self.componentes['edicion_busqueda'] = EdicionBusquedaFrame(self.contenido_principal_frame, self.service)
        self.componentes['edicion_busqueda'].frame.grid(row=0, column=0, sticky="nsew")
        self.componentes['edicion_busqueda'].frame.grid_remove()  # Ocultar inicialmente
    
    def crear_componente_creacion(self):
        """Crea el componente de creación de persona"""
        self.componentes['creacion_persona'] = CreacionPersonaFrame(self.contenido_principal_frame, self.service)
        self.componentes['creacion_persona'].frame.grid(row=0, column=0, sticky="nsew")
        self.componentes['creacion_persona'].frame.grid_remove()  # Ocultar inicialmente

    def cambiar_contenido(self, tipo_contenido):
        """Cambia el contenido mostrado según el botón seleccionado"""
        # Ocultar todos los componentes
        if 'gestion_frame' in self.componentes:
            self.componentes['gestion_frame'].grid_remove()
        if 'edicion_busqueda' in self.componentes:
            self.componentes['edicion_busqueda'].frame.grid_remove()
        if 'creacion_persona' in self.componentes:
            self.componentes['creacion_persona'].frame.grid_remove()
        
        # Mostrar el componente seleccionado
        if tipo_contenido == "gestion":
            if 'gestion_frame' in self.componentes:
                self.componentes['gestion_frame'].grid()
        elif tipo_contenido == "edicion":
            if 'edicion_busqueda' in self.componentes:
                self.componentes['edicion_busqueda'].frame.grid()
        elif tipo_contenido == "creacion":
            if 'creacion_persona' in self.componentes:
                self.componentes['creacion_persona'].frame.grid()
        
        # Actualizar estado visual de los botones
        for valor, btn in self.botones_navegacion.items():
            if valor == tipo_contenido:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AppEmpleadosRefactorizada(root)
    root.mainloop()

if __name__ == "__main__":
    main()
