import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from models import Empleado
from data import EmpleadoRepository
from services import EmpleadoService, reconciliation_service, export_service, history_service
from ui import (CamposGeneralesFrame, OnboardingFrame, OffboardingFrame, 
                LateralMovementFrame, EdicionBusquedaFrame, CreacionPersonaFrame)
from ui.styles import aplicar_estilos_personalizados


class AppEmpleadosRefactorizada:
    """Aplicación principal integrada con sistema de conciliación"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integrado de Gestión de Empleados y Conciliación de Accesos")
        
        # Configuración responsive
        self.configurar_ventana_responsive()
        
        aplicar_estilos_personalizados()
        
        # Inicializar servicios
        self.repository = EmpleadoRepository()
        self.service = EmpleadoService(self.repository)
        
        # Variables de control
        self.tipo_proceso_var = tk.StringVar()
        self.componentes = {}
        
        # Configurar eventos de redimensionamiento
        self.root.bind('<Configure>', self._on_window_resize)
        
        self.crear_interfaz()
    
    def configurar_ventana_responsive(self):
        """Configura la ventana para ser responsive"""
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Detectar tipo de pantalla
        self._detectar_tipo_pantalla(screen_width, screen_height)
        
        # Calcular dimensiones óptimas según el tipo de pantalla
        if self.tipo_pantalla == "pequena":
            window_width = min(int(screen_width * 0.95), 1200)
            window_height = min(int(screen_height * 0.9), 700)
        elif self.tipo_pantalla == "mediana":
            window_width = min(int(screen_width * 0.85), 1400)
            window_height = min(int(screen_height * 0.85), 800)
        else:  # grande
            window_width = min(int(screen_width * 0.8), 1600)
            window_height = min(int(screen_height * 0.8), 900)
        
        # Asegurar tamaño mínimo
        window_width = max(window_width, 800)
        window_height = max(window_height, 500)
        
        # Centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configurar tamaño mínimo
        self.root.minsize(800, 500)
        
        # Permitir redimensionamiento
        self.root.resizable(True, True)
        
        print(f"Pantalla detectada: {self.tipo_pantalla} ({screen_width}x{screen_height})")
        print(f"Ventana configurada: {window_width}x{window_height}")
    
    def _detectar_tipo_pantalla(self, width, height):
        """Detecta el tipo de pantalla basado en las dimensiones"""
        if width < 1366 or height < 768:
            self.tipo_pantalla = "pequena"
        elif width < 1920 or height < 1080:
            self.tipo_pantalla = "mediana"
        else:
            self.tipo_pantalla = "grande"
    
    def _centrar_ventana(self, w, h):
        """Centra la ventana en la pantalla (método legacy)"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
    
    def _on_window_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        # Solo procesar eventos de la ventana principal
        if event.widget == self.root:
            # Ajustar tamaños de fuente y widgets según el tamaño de la ventana
            self._ajustar_tamanos_responsive()
    
    def _ajustar_tamanos_responsive(self):
        """Ajusta tamaños de widgets según el tamaño de la ventana"""
        try:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # Ajustar tamaños de botones según el ancho de la ventana
            if width < 1200:
                # Pantalla pequeña
                button_width = 20
                font_size = 9
            elif width < 1400:
                # Pantalla mediana
                button_width = 22
                font_size = 10
            else:
                # Pantalla grande
                button_width = 25
                font_size = 11
            
            # Aplicar ajustes a los botones de navegación
            for btn in self.botones_navegacion.values():
                btn.configure(width=button_width)
            
            # Ajustar padding y márgenes
            self._ajustar_espaciado_responsive(width, height)
            
            # Ajustar grid weights si está disponible
            if hasattr(self, '_ajustar_grid_weights'):
                self._ajustar_grid_weights()
            
            # Ajustar componentes individuales
            self._ajustar_componentes_responsive(width, height)
            
        except Exception as e:
            print(f"Error ajustando tamaños responsive: {e}")
    
    def _ajustar_componentes_responsive(self, width, height):
        """Ajusta todos los componentes para ser responsive"""
        try:
            # Ajustar componente de gestión si existe
            if 'gestion_frame' in self.componentes:
                gestion_frame = self.componentes['gestion_frame']
                if hasattr(gestion_frame, '_ajustar_layout'):
                    gestion_frame._ajustar_layout()
            
            # Ajustar otros componentes según sea necesario
            if width < 1200:
                # Pantalla pequeña: ajustar tamaños de fuente y espaciado
                self._ajustar_para_pantalla_pequena()
            elif width < 1400:
                # Pantalla mediana: ajustes moderados
                self._ajustar_para_pantalla_mediana()
            else:
                # Pantalla grande: ajustes estándar
                self._ajustar_para_pantalla_grande()
                
        except Exception as e:
            print(f"Error ajustando componentes responsive: {e}")
    
    def _ajustar_para_pantalla_pequena(self):
        """Ajusta la interfaz para pantallas pequeñas"""
        try:
            # Reducir padding y márgenes
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(padding="15")
            
            # Ajustar tamaños de botones
            for btn in self.botones_navegacion.values():
                btn.configure(width=18)
                
        except Exception as e:
            print(f"Error ajustando para pantalla pequeña: {e}")
    
    def _ajustar_para_pantalla_mediana(self):
        """Ajusta la interfaz para pantallas medianas"""
        try:
            # Padding moderado
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(padding="20")
            
            # Tamaños de botones estándar
            for btn in self.botones_navegacion.values():
                btn.configure(width=22)
                
        except Exception as e:
            print(f"Error ajustando para pantalla mediana: {e}")
    
    def _ajustar_para_pantalla_grande(self):
        """Ajusta la interfaz para pantallas grandes"""
        try:
            # Padding generoso
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(padding="25")
            
            # Tamaños de botones grandes
            for btn in self.botones_navegacion.values():
                btn.configure(width=25)
                
        except Exception as e:
            print(f"Error ajustando para pantalla grande: {e}")
    
    def _mostrar_info_responsive(self):
        """Muestra información sobre el estado responsive de la aplicación"""
        try:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            info = f"📱 Información Responsive\n\n"
            info += f"Tipo de pantalla: {getattr(self, 'tipo_pantalla', 'No detectado')}\n"
            info += f"Resolución de pantalla: {screen_width}x{screen_height}\n"
            info += f"Tamaño de ventana: {width}x{height}\n"
            info += f"Tamaño mínimo: 800x500\n\n"
            
            if width < 1200:
                info += "🎯 Modo: Pantalla pequeña (compacto)"
            elif width < 1400:
                info += "🎯 Modo: Pantalla mediana (balanceado)"
            else:
                info += "🎯 Modo: Pantalla grande (espacioso)"
            
            info += "\n\n💡 La aplicación se ajusta automáticamente al redimensionar la ventana"
            
            messagebox.showinfo("Información Responsive", info)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando información responsive: {str(e)}")
    
    def _ajustar_espaciado_responsive(self, width, height):
        """Ajusta el espaciado según el tamaño de la ventana"""
        try:
            # Ajustar padding del frame principal
            if width < 1200:
                main_padding = "15"
                nav_padding = "15"
            elif width < 1400:
                main_padding = "20"
                nav_padding = "20"
            else:
                main_padding = "25"
                nav_padding = "25"
            
            # Aplicar padding al frame principal si existe
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(padding=main_padding)
            
            # Ajustar padding de navegación si existe
            if hasattr(self, 'nav_frame'):
                self.nav_frame.configure(padding=nav_padding)
                
        except Exception as e:
            print(f"Error ajustando espaciado responsive: {e}")
        
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Guardar referencia al frame principal para ajustes responsive
        self.main_frame = ttk.Frame(self.root, padding="25", style="Main.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Título responsive
        titulo_label = ttk.Label(self.main_frame, text="Sistema Integrado de Gestión", 
                                style="Title.TLabel")
        titulo_label.grid(row=0, column=0, columnspan=2, pady=(0, 35), sticky="ew")
        
        self.crear_botones_laterales(self.main_frame)
        self.crear_contenido_principal(self.main_frame)
    
    def crear_botones_laterales(self, parent):
        """Crea la navegación lateral"""
        # Guardar referencia al frame de navegación para ajustes responsive
        self.nav_frame = ttk.LabelFrame(parent, text="Navegación", padding="25", style="Nav.TLabelframe")
        self.nav_frame.grid(row=1, column=0, sticky="n", padx=(0, 30), pady=(0, 20))
        self.nav_frame.columnconfigure(0, weight=1)
        
        # Botones de navegación
        opciones = [
            ("📋 Gestión de Procesos", "gestion"),
            ("🔍 Edición y Búsqueda", "edicion"),
            ("👤 Crear Persona", "creacion"),
            ("🔐 Conciliación de Accesos", "conciliacion")
        ]
        
        self.botones_navegacion = {}
        for i, (texto, valor) in enumerate(opciones):
            btn_container = ttk.Frame(self.nav_frame)
            btn_container.grid(row=i, column=0, pady=12, sticky="ew")
            btn_container.columnconfigure(0, weight=1)
            
            btn = ttk.Button(btn_container, text=texto, width=25, 
                           command=lambda v=valor: self.cambiar_contenido(v), style="Nav.TButton")
            btn.grid(row=0, column=0, sticky="ew", pady=5)
            self.botones_navegacion[valor] = btn
        
        # Botón de salida
        ttk.Button(self.nav_frame, text="🚪 Salir", width=25, 
                  command=self.root.quit, style="Salir.TButton").grid(row=len(opciones), column=0, pady=(20, 5))
        
        self.cambiar_contenido("gestion")
    
    def crear_contenido_principal(self, parent):
        """Crea el área de contenido principal"""
        self.contenido_principal_frame = ttk.Frame(parent)
        self.contenido_principal_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 30), pady=(0, 20))
        self.contenido_principal_frame.columnconfigure(0, weight=1)
        self.contenido_principal_frame.rowconfigure(0, weight=1)
        
        # Crear componentes
        self.crear_componente_gestion()
        self.crear_componente_edicion()
        self.crear_componente_creacion()
        self.crear_componente_conciliacion()
        
        # Configurar contenido responsive
        self._configurar_contenido_responsive()
    
    def _configurar_contenido_responsive(self):
        """Configura el contenido principal para ser responsive"""
        # Configurar grid weights para diferentes tamaños de pantalla
        def ajustar_grid_weights():
            width = self.root.winfo_width()
            
            if width < 1200:
                # Pantalla pequeña: navegación más compacta
                self.main_frame.columnconfigure(0, weight=0)  # Navegación fija
                self.main_frame.columnconfigure(1, weight=1)  # Contenido expandible
                self.nav_frame.configure(padding="15")
            elif width < 1400:
                # Pantalla mediana: balance entre navegación y contenido
                self.main_frame.columnconfigure(0, weight=0)
                self.main_frame.columnconfigure(1, weight=1)
                self.nav_frame.configure(padding="20")
            else:
                # Pantalla grande: navegación cómoda
                self.main_frame.columnconfigure(0, weight=0)
                self.main_frame.columnconfigure(1, weight=1)
                self.nav_frame.configure(padding="25")
        
        # Aplicar configuración inicial
        ajustar_grid_weights()
        
        # Guardar función para uso posterior
        self._ajustar_grid_weights = ajustar_grid_weights
        

    
    def crear_componente_gestion(self):
        """Crea el componente de gestión de procesos"""
        gestion_frame = ttk.Frame(self.contenido_principal_frame)
        gestion_frame.columnconfigure(0, weight=1)
        gestion_frame.rowconfigure(0, weight=0)
        gestion_frame.rowconfigure(1, weight=1)
        
        # Título
        ttk.Label(gestion_frame, text="Gestión de Procesos", 
                  style="Section.TLabel").grid(row=0, column=0, pady=(0, 25), sticky="ew")
        
        # Contenido
        contenido_frame = ttk.Frame(gestion_frame)
        contenido_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 25))
        contenido_frame.columnconfigure(0, weight=0)
        contenido_frame.columnconfigure(1, weight=1)
        contenido_frame.columnconfigure(2, weight=0)
        
        ttk.Label(contenido_frame, text="Complete la información del proceso", 
                 style="Subsection.TLabel").grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="ew")
        
        # Campos generales
        self.componentes['generales'] = CamposGeneralesFrame(contenido_frame)
        self.componentes['generales'].frame.grid(row=1, column=0, sticky="ew", pady=(0, 20), padx=(25, 15))
        
        # Pestañas de proceso
        self.crear_pestanas_proceso(contenido_frame)
        
        # Botones de acción
        self.crear_botones_accion(contenido_frame)
        
        self.componentes['gestion_frame'] = gestion_frame
        
        # Configurar responsive para este componente
        self._configurar_componente_responsive(gestion_frame, contenido_frame)
    
    def _configurar_componente_responsive(self, gestion_frame, contenido_frame):
        """Configura un componente para ser responsive"""
        def ajustar_layout():
            width = self.root.winfo_width()
            
            if width < 1200:
                # Pantalla pequeña: layout más compacto
                contenido_frame.columnconfigure(0, weight=0)  # Campos generales
                contenido_frame.columnconfigure(1, weight=1)  # Pestañas
                contenido_frame.columnconfigure(2, weight=0)  # Botones
                
                # Ajustar padding
                gestion_frame.configure(padding="15")
                contenido_frame.configure(padding="10")
                
            elif width < 1400:
                # Pantalla mediana: layout balanceado
                contenido_frame.columnconfigure(0, weight=0)
                contenido_frame.columnconfigure(1, weight=1)
                contenido_frame.columnconfigure(2, weight=0)
                
                gestion_frame.configure(padding="20")
                contenido_frame.configure(padding="15")
                
            else:
                # Pantalla grande: layout espacioso
                contenido_frame.columnconfigure(0, weight=0)
                contenido_frame.columnconfigure(1, weight=1)
                contenido_frame.columnconfigure(2, weight=0)
                
                gestion_frame.configure(padding="25")
                contenido_frame.configure(padding="20")
        
        # Aplicar configuración inicial
        ajustar_layout()
        
        # Guardar función para ajustes posteriores
        gestion_frame._ajustar_layout = ajustar_layout
    
    def crear_pestanas_proceso(self, parent):
        """Crea el sistema de pestañas para tipos de proceso"""
        pestanas_frame = ttk.LabelFrame(parent, text="Tipo de Proceso", padding="15")
        pestanas_frame.grid(row=1, column=1, sticky="ew", pady=(0, 20), padx=(15, 25))
        pestanas_frame.columnconfigure(0, weight=1)
        pestanas_frame.rowconfigure(1, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(pestanas_frame)
        self.notebook.grid(row=1, column=0, sticky="ew", pady=(15, 0), padx=15)
        
        # Pestaña de selección
        seleccion_frame = ttk.Frame(self.notebook)
        self.notebook.add(seleccion_frame, text="Seleccionar Proceso")
        seleccion_frame.columnconfigure(0, weight=1)
        
        ttk.Label(seleccion_frame, text="Seleccione el tipo de proceso:", 
                 style="Normal.TLabel").grid(row=0, column=0, pady=20, sticky="ew")
        
        # Opciones de proceso
        opciones = [("Onboarding", "onboarding"), ("Offboarding", "offboarding"), ("Lateral Movement", "lateral")]
        for i, (texto, valor) in enumerate(opciones):
            ttk.Radiobutton(seleccion_frame, text=texto, variable=self.tipo_proceso_var, 
                           value=valor, command=self.cambiar_pestana).grid(row=i+1, column=0, pady=8, sticky="ew")
        
        # Inicializar pestañas dinámicas
        self.pestanas_dinamicas = {'onboarding': None, 'offboarding': None, 'lateral': None}
    
    def cambiar_pestana(self):
        """Cambia la pestaña según la selección"""
        # Ocultar todas las pestañas dinámicas
        for pestana in self.pestanas_dinamicas.values():
            if pestana:
                self.notebook.hide(pestana)
        
        tipo_seleccionado = self.tipo_proceso_var.get()
        
        # Crear y mostrar pestaña correspondiente
        if tipo_seleccionado in self.pestanas_dinamicas:
            if not self.pestanas_dinamicas[tipo_seleccionado]:
                self.crear_pestana_dinamica(tipo_seleccionado)
            self.notebook.add(self.pestanas_dinamicas[tipo_seleccionado], text=tipo_seleccionado.title())
    
    def crear_pestana_dinamica(self, tipo):
        """Crea una pestaña dinámica según el tipo"""
        try:
            frame_classes = {
                'onboarding': OnboardingFrame,
                'offboarding': OffboardingFrame,
                'lateral': LateralMovementFrame
            }
            
            if tipo in frame_classes:
                self.componentes[tipo] = frame_classes[tipo](self.notebook)
                self.pestanas_dinamicas[tipo] = self.componentes[tipo].frame
            else:
                self._crear_pestana_fallback(f"Error: Tipo {tipo} no soportado")
                
        except Exception as e:
            print(f"Error creando pestaña {tipo}: {e}")
            self._crear_pestana_fallback(f"Error cargando {tipo}")
    
    def _crear_pestana_fallback(self, mensaje):
        """Crea una pestaña de fallback en caso de error"""
        fallback_frame = ttk.Frame(self.notebook)
        ttk.Label(fallback_frame, text=mensaje, style="Subsection.TLabel").pack(pady=20)
        
        # Crear objeto fallback con método obtener_datos
        fallback_obj = type('FallbackFrame', (), {
            'frame': fallback_frame,
            'obtener_datos': lambda: {}
        })()
        
        return fallback_obj
    
    def crear_botones_accion(self, parent):
        """Crea los botones de acción"""
        botones_frame = ttk.Frame(parent)
        botones_frame.grid(row=1, column=2, pady=40, padx=(30, 0), sticky="n")  # Aumentar espaciado
        botones_frame.columnconfigure(0, weight=1)
        
        # Botones con estilos predefinidos
        botones_info = [
            ("💾 Guardar", self.guardar_datos, "Success.TButton"),
            ("🧹 Limpiar", self.limpiar_campos, "Info.TButton"),
            ("📊 Estadísticas", self.mostrar_estadisticas, "Warning.TButton"),
            ("🚪 Salir", self.root.quit, "Danger.TButton")
        ]
        
        for i, (texto, comando, estilo) in enumerate(botones_info):
            btn = ttk.Button(botones_frame, text=texto, command=comando, width=25, style=estilo)  # Aumentar ancho
            btn.grid(row=i, column=0, pady=12, sticky="ew")  # Aumentar espaciado
    
    def crear_componente_edicion(self):
        """Crea el componente de edición y búsqueda"""
        self.componentes['edicion_busqueda'] = EdicionBusquedaFrame(self.contenido_principal_frame, self.service)
        self.componentes['edicion_busqueda'].frame.grid(row=0, column=0, sticky="nsew")
        self.componentes['edicion_busqueda'].frame.grid_remove()
    
    def crear_componente_creacion(self):
        """Crea el componente de creación de persona"""
        try:
            print("Creando componente de creación...")
            self.componentes['creacion_persona'] = CreacionPersonaFrame(self.contenido_principal_frame, self.service)
            self.componentes['creacion_persona'].frame.grid(row=0, column=0, sticky="nsew")
            self.componentes['creacion_persona'].frame.grid_remove()
            print("Componente de creación creado exitosamente")
        except Exception as e:
            print(f"Error creando componente de creación: {e}")
            import traceback
            traceback.print_exc()
    
    def crear_componente_conciliacion(self):
        """Crea el componente de conciliación de accesos"""
        self.componentes['conciliacion'] = ConciliacionFrame(self.contenido_principal_frame)
        self.componentes['conciliacion'].frame.grid(row=0, column=0, sticky="nsew")
        self.componentes['conciliacion'].frame.grid_remove()
    
    def cambiar_contenido(self, tipo_contenido):
        """Cambia el contenido mostrado según el botón seleccionado"""
        # Ocultar todos los componentes
        componentes_a_ocultar = ['gestion_frame', 'edicion_busqueda', 'creacion_persona', 'conciliacion']
        for comp in componentes_a_ocultar:
            if comp in self.componentes:
                if comp == 'gestion_frame':
                    self.componentes[comp].grid_remove()
                else:
                    self.componentes[comp].frame.grid_remove()
        
        # Mostrar el componente seleccionado
        if tipo_contenido == "gestion" and 'gestion_frame' in self.componentes:
            self.componentes['gestion_frame'].grid()
        elif tipo_contenido == "edicion" and 'edicion_busqueda' in self.componentes:
            self.componentes['edicion_busqueda'].frame.grid()
        elif tipo_contenido == "creacion" and 'creacion_persona' in self.componentes:
            self.componentes['creacion_persona'].frame.grid()
        elif tipo_contenido == "conciliacion" and 'conciliacion' in self.componentes:
            self.componentes['conciliacion'].frame.grid()
        
        # Actualizar estado visual de los botones
        for valor, btn in self.botones_navegacion.items():
            btn.state(['pressed'] if valor == tipo_contenido else ['!pressed'])
    
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
                except Exception as e:
                    print(f"Error obteniendo datos específicos de {tipo_proceso}: {e}")
            
            # Generar número de caso único
            empleado_temp = Empleado(
                sid=datos_generales.get('sid', ''),
                nueva_sub_unidad=datos_generales.get('nueva_sub_unidad', ''),
                nuevo_cargo=datos_generales.get('nuevo_cargo', ''),
                ingreso_por=datos_generales.get('ingreso_por', ''),
                request_date=datos_generales.get('request_date'),
                fecha=datos_generales.get('fecha'),
                status=datos_generales.get('status', 'Pendiente')
            )
            
            # Combinar datos y guardar
            datos_completos = {**datos_generales, **datos_especificos}
            datos_completos['numero_caso'] = empleado_temp.numero_caso
            datos_completos['tipo_proceso'] = tipo_proceso
            
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
        """Muestra estadísticas de los datos almacenados"""
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


class ConciliacionFrame:
    """Frame simplificado para la conciliación de accesos"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Variables de control
        self.sid_var = tk.StringVar()
        self.resultado_conciliacion = None
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de conciliación"""
        # Título principal
        ttk.Label(self.frame, text="🔐 Sistema de Conciliación de Accesos", 
                  style="Title.TLabel").grid(row=0, column=0, pady=(0, 30), sticky="ew")
        
        # Frame principal con dos columnas
        main_content = ttk.Frame(self.frame)
        main_content.grid(row=1, column=0, sticky="nsew", padx=20)
        main_content.columnconfigure(0, weight=1)
        main_content.columnconfigure(1, weight=1)
        main_content.rowconfigure(1, weight=1)
        
        # Columna izquierda - Entrada de datos
        self._crear_seccion_entrada(main_content)
        
        # Columna derecha - Resultados y acciones
        self._crear_seccion_acciones(main_content)
    
    def _crear_seccion_entrada(self, parent):
        """Crea la sección de entrada de datos"""
        entrada_frame = ttk.LabelFrame(parent, text="📝 Datos de Entrada", padding="20")
        entrada_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        entrada_frame.columnconfigure(0, weight=1)
        
        # Campo SID
        ttk.Label(entrada_frame, text="SID del Empleado:", 
                 style="Subsection.TLabel").grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        sid_entry = ttk.Entry(entrada_frame, textvariable=self.sid_var, width=30)
        sid_entry.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        
        # Botones de conciliación
        ttk.Button(entrada_frame, text="🔍 Conciliar Accesos", 
                  command=self._conciliar_accesos, style="Success.TButton").grid(row=2, column=0, pady=(0, 10), sticky="ew")
        
        ttk.Button(entrada_frame, text="🌐 Conciliar Todos", 
                  command=self._conciliar_todos, style="Info.TButton").grid(row=3, column=0, pady=(0, 20), sticky="ew")
        
        # Información adicional
        info_text = ("Este sistema compara los accesos actuales de un empleado\n"
                    "con los accesos que debería tener según su puesto.\n"
                    "Identifica accesos faltantes y excesivos.")
        ttk.Label(entrada_frame, text=info_text, style="Subsection.TLabel", 
                 justify="center").grid(row=4, column=0, pady=(20, 0), sticky="ew")
    
    def _crear_seccion_acciones(self, parent):
        """Crea la sección de acciones y resultados"""
        acciones_frame = ttk.LabelFrame(parent, text="⚡ Acciones y Resultados", padding="20")
        acciones_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        acciones_frame.columnconfigure(0, weight=1)
        acciones_frame.rowconfigure(1, weight=1)
        
        # Botones de acción
        botones_frame = ttk.Frame(acciones_frame)
        botones_frame.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)
        
        ttk.Button(botones_frame, text="📤 Exportar Excel", 
                  command=self._exportar_excel, style="Warning.TButton").grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        ttk.Button(botones_frame, text="🎫 Registrar Tickets", 
                  command=self._registrar_tickets, style="Danger.TButton").grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(acciones_frame, text="📊 Resultados de Conciliación", padding="15")
        resultados_frame.grid(row=1, column=0, sticky="nsew")
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar resultados
        columns = ('Acceso', 'Rol', 'Estado', 'Acción')
        self.tree_resultados = ttk.Treeview(resultados_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        for col in columns:
            self.tree_resultados.heading(col, text=col)
            self.tree_resultados.column(col, width=120, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree_resultados.yview)
        self.tree_resultados.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree_resultados.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Mensaje inicial
        self.tree_resultados.insert('', 'end', values=('', '', 'Sin datos', ''))
    
    def _conciliar_accesos(self):
        """Ejecuta la conciliación de accesos para un SID específico"""
        sid = self.sid_var.get().strip()
        if not sid:
            messagebox.showerror("Error", "Por favor ingrese un SID válido")
            return
        
        try:
            resultado = reconciliation_service.reconcile_person(sid)
            
            if "error" in resultado:
                messagebox.showerror("Error", resultado["error"])
                return
            
            self.resultado_conciliacion = resultado
            self._mostrar_resultados(resultado)
            messagebox.showinfo("Éxito", f"Conciliación completada para {sid}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la conciliación: {str(e)}")
    
    def _conciliar_todos(self):
        """Ejecuta la conciliación de accesos para todos los usuarios"""
        try:
            resultados = reconciliation_service.reconcile_all()
            
            if not resultados:
                messagebox.showwarning("Advertencia", "No se encontraron usuarios para conciliar")
                return
            
            self.resultado_conciliacion = resultados
            
            # Mostrar resumen
            total_to_grant = sum(len(r.get('to_grant', [])) for r in resultados if 'error' not in r)
            total_to_revoke = sum(len(r.get('to_revoke', [])) for r in resultados if 'error' not in r)
            
            mensaje = f"Conciliación masiva completada:\n"
            mensaje += f"Usuarios procesados: {len(resultados)}\n"
            mensaje += f"Accesos a otorgar: {total_to_grant}\n"
            mensaje += f"Accesos a revocar: {total_to_revoke}"
            
            messagebox.showinfo("Éxito", mensaje)
            
            # Limpiar treeview
            self.tree_resultados.delete(*self.tree_resultados.get_children())
            self.tree_resultados.insert('', 'end', values=('', '', 'Conciliación masiva completada', ''))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la conciliación masiva: {str(e)}")
    
    def _exportar_excel(self):
        """Exporta los resultados de conciliación a Excel"""
        if not self.resultado_conciliacion:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        try:
            output_path = export_service.export_reconciliation_tickets(
                [self.resultado_conciliacion] if isinstance(self.resultado_conciliacion, dict) 
                else self.resultado_conciliacion,
                "Sistema Integrado"
            )
            
            messagebox.showinfo("Éxito", f"Archivo exportado exitosamente a:\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def _registrar_tickets(self):
        """Registra los tickets de conciliación en el historial"""
        if not self.resultado_conciliacion:
            messagebox.showwarning("Advertencia", "No hay resultados para registrar")
            return
        
        try:
            resultado = history_service.register_reconciliation_tickets(
                self.resultado_conciliacion, "Sistema Integrado"
            )
            
            tickets_creados = resultado.get('tickets_created', 0)
            messagebox.showinfo("Éxito", f"Se registraron {tickets_creados} tickets exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar tickets: {str(e)}")
    
    def _mostrar_resultados(self, resultado):
        """Muestra los resultados de conciliación en el treeview"""
        # Limpiar treeview
        self.tree_resultados.delete(*self.tree_resultados.get_children())
        
        # Mostrar accesos actuales
        for acceso in resultado.get('current', []):
            self.tree_resultados.insert('', 'end', values=(
                acceso.get('app_name', ''),
                acceso.get('role_name', 'Sin rol'),
                '✅ Activo',
                'Mantener'
            ))
        
        # Mostrar accesos a otorgar
        for acceso in resultado.get('to_grant', []):
            self.tree_resultados.insert('', 'end', values=(
                acceso.get('app_name', ''),
                acceso.get('role_name', 'Sin rol'),
                '❌ Faltante',
                '🟢 Otorgar'
            ))
        
        # Mostrar accesos a revocar
        for acceso in resultado.get('to_revoke', []):
            self.tree_resultados.insert('', 'end', values=(
                acceso.get('app_name', ''),
                acceso.get('role_name', 'Sin rol'),
                '⚠️ Excesivo',
                '🔴 Revocar'
            ))


def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AppEmpleadosRefactorizada(root)
    root.mainloop()


if __name__ == "__main__":
    main()
