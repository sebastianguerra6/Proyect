import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import pyodbc
from PIL import Image, ImageTk

from services import export_service, history_service, access_service, search_service
from ui import (CamposGeneralesFrame, OnboardingFrame, OffboardingFrame, 
                LateralMovementFrame, EdicionBusquedaFrame, CreacionPersonaFrame)
from ui.styles import aplicar_estilos_personalizados


class AppEmpleadosRefactorizada:
    """Aplicación principal integrada con sistema de conciliación"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("GAMLO - Sistema Integrado de Gestión de Empleados y Conciliación de Accesos")
        
        # Configuración responsive
        self.configurar_ventana_responsive()
        
        aplicar_estilos_personalizados()
        
        # Inicializar servicios (ya no se usa EmpleadoService)
        
        # Variables de control
        self.tipo_proceso_var = tk.StringVar()
        self.componentes = {}
        

        
        self.crear_interfaz()
    
    def configurar_ventana_responsive(self):
        """Configura la ventana para ser responsive"""
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Configurar dimensiones estándar
        window_width = min(int(screen_width * 0.8), 1400)
        window_height = min(int(screen_height * 0.8), 800)
        
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
        self.main_frame.rowconfigure(2, weight=0)
        
        # Frame para el header con título
        header_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 35), sticky="ew")
        header_frame.columnconfigure(0, weight=1)
        
        # Título con GAMLO
        titulo_label = ttk.Label(header_frame, text="GAMLO - Sistema Integrado de Gestión", 
                                style="Title.TLabel")
        titulo_label.grid(row=0, column=0, pady=(0, 0), sticky="ew")
        
        self.crear_botones_laterales(self.main_frame)
        self.crear_contenido_principal(self.main_frame)
        
        # Footer con logo GAMLO (abajo a la izquierda)
        self.crear_footer_con_logo(self.main_frame)
    
    def crear_logo_gamlo(self, parent):
        """Crea el logo de GAMLO en la esquina izquierda"""
        try:
            # Intentar cargar imagen del logo
            logo_path = os.path.join("images", "gamlo_logo.png")
            if os.path.exists(logo_path):
                # Cargar imagen real
                image = Image.open(logo_path)
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(image)
                logo_label = ttk.Label(parent, image=self.logo_photo)
            else:
                # Crear logo de texto si no hay imagen
                logo_label = ttk.Label(parent, text="GAMLO", 
                                     font=("Arial", 16, "bold"),
                                     foreground="#2E86AB",
                                     background="#F8F9FA")
                # Crear un frame con borde para simular un logo
                logo_frame = ttk.Frame(parent, style="Logo.TFrame")
                logo_frame.grid(row=0, column=0, padx=(0, 10), pady=5)
                logo_label = ttk.Label(logo_frame, text="GAMLO", 
                                     font=("Arial", 14, "bold"),
                                     foreground="#2E86AB")
                logo_label.pack(padx=10, pady=10)
                return
            
            logo_label.grid(row=0, column=0, padx=(0, 10), pady=5)
            
        except Exception as e:
            # Fallback: crear logo de texto si hay error
            logo_label = ttk.Label(parent, text="GAMLO", 
                                 font=("Arial", 14, "bold"),
                                 foreground="#2E86AB")
            logo_label.grid(row=0, column=0, padx=(0, 10), pady=5)
    
    def crear_footer_con_logo(self, parent):
        """Crea el footer con el logo GAMLO en la parte inferior izquierda"""
        # Frame para el footer
        footer_frame = ttk.Frame(parent, style="Main.TFrame")
        footer_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        footer_frame.columnconfigure(0, weight=0)
        footer_frame.columnconfigure(1, weight=1)
        
        # Logo GAMLO (abajo a la izquierda)
        self.crear_logo_gamlo_footer(footer_frame)
        
        # Espacio en blanco para empujar el logo a la izquierda
        ttk.Frame(footer_frame).grid(row=0, column=1, sticky="ew")
    
    def crear_logo_gamlo_footer(self, parent):
        """Crea el logo de GAMLO para el footer"""
        try:
            # Intentar cargar imagen del logo
            logo_path = os.path.join("images", "gamlo_logo.png")
            if os.path.exists(logo_path):
                # Cargar imagen real
                image = Image.open(logo_path)
                image = image.resize((48, 48), Image.Resampling.LANCZOS)  # Más pequeño para el footer
                self.logo_photo_footer = ImageTk.PhotoImage(image)
                logo_label = ttk.Label(parent, image=self.logo_photo_footer)
            else:
                # Crear logo de texto si no hay imagen
                logo_label = ttk.Label(parent, text="GAMLO", 
                                     font=("Arial", 12, "bold"),
                                     foreground="#2E86AB",
                                     background="#F8F9FA")
                # Crear un frame con borde para simular un logo
                logo_frame = ttk.Frame(parent, style="Logo.TFrame")
                logo_frame.grid(row=0, column=0, padx=(0, 10), pady=5)
                logo_label = ttk.Label(logo_frame, text="GAMLO", 
                                     font=("Arial", 10, "bold"),
                                     foreground="#2E86AB")
                logo_label.pack(padx=8, pady=8)
                return
            
            logo_label.grid(row=0, column=0, padx=(0, 10), pady=5)
            
        except Exception as e:
            # Fallback: crear logo de texto si hay error
            logo_label = ttk.Label(parent, text="GAMLO", 
                                 font=("Arial", 10, "bold"),
                                 foreground="#2E86AB")
            logo_label.grid(row=0, column=0, padx=(0, 10), pady=5)
    
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
            ("🔐 Conciliación de Accesos", "conciliacion"),
            ("📱 Gestión de Aplicaciones", "aplicaciones")
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
        self.crear_componente_aplicaciones()
        

    

        

    
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
            ("🔍 Probar Deduplicación", self.probar_deduplicacion, "Info.TButton"),
            ("🚪 Salir", self.root.quit, "Danger.TButton")
        ]
        
        for i, (texto, comando, estilo) in enumerate(botones_info):
            btn = ttk.Button(botones_frame, text=texto, command=comando, width=25, style=estilo)  # Aumentar ancho
            btn.grid(row=i, column=0, pady=12, sticky="ew")  # Aumentar espaciado
    
    def crear_componente_edicion(self):
        """Crea el componente de edición y búsqueda"""
        self.componentes['edicion_busqueda'] = EdicionBusquedaFrame(self.contenido_principal_frame, access_service)
        self.componentes['edicion_busqueda'].frame.grid(row=0, column=0, sticky="nsew")
        self.componentes['edicion_busqueda'].frame.grid_remove()
    
    def crear_componente_creacion(self):
        """Crea el componente de creación de persona"""
        try:
            print("Creando componente de creación...")
            self.componentes['creacion_persona'] = CreacionPersonaFrame(self.contenido_principal_frame, search_service)
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
    
    def crear_componente_aplicaciones(self):
        """Crea el componente de gestión de aplicaciones"""
        self.componentes['aplicaciones'] = AplicacionesFrame(self.contenido_principal_frame)
        self.componentes['aplicaciones'].frame.grid(row=0, column=0, sticky="nsew")
        self.componentes['aplicaciones'].frame.grid_remove()
    
    
    def cambiar_contenido(self, tipo_contenido):
        """Cambia el contenido mostrado según el botón seleccionado"""
        # Ocultar todos los componentes
        componentes_a_ocultar = ['gestion_frame', 'edicion_busqueda', 'creacion_persona', 'conciliacion', 'aplicaciones']
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
        elif tipo_contenido == "aplicaciones" and 'aplicaciones' in self.componentes:
            self.componentes['aplicaciones'].frame.grid()
        
        # Actualizar estado visual de los botones
        for valor, btn in self.botones_navegacion.items():
            btn.state(['pressed'] if valor == tipo_contenido else ['!pressed'])
    
    def guardar_datos(self):
        """Guarda los datos del formulario en la nueva estructura de base de datos"""
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
            
            # Obtener SID del empleado
            scotia_id = datos_generales.get('sid', '')
            if not scotia_id:
                messagebox.showerror("Error", "El SID es obligatorio")
                return
            
            # Procesar según el tipo de proceso usando la nueva estructura
            if tipo_proceso == 'onboarding':
                # Para onboarding, solo procesamos los accesos (el empleado debe existir previamente)
                # o se debe crear desde la sección "Crear Persona"
                
                # Verificar si el empleado existe
                empleado_existente = access_service.get_employee_by_id(scotia_id)
                if not empleado_existente:
                    messagebox.showerror("Error", 
                        f"El empleado {scotia_id} no existe en el headcount.\n"
                        "Por favor, cree primero el empleado en la sección 'Crear Persona'.")
                    return
                
                # Procesar onboarding
                success, message, records = access_service.process_employee_onboarding(
                    scotia_id, 
                    datos_generales.get('nuevo_cargo', ''), 
                    datos_generales.get('nueva_sub_unidad', '')
                )
                
                if success:
                    messagebox.showinfo("Éxito", f"Onboarding procesado exitosamente.\n{message}")
                    self.limpiar_campos()
                else:
                    messagebox.showerror("Error", message)
                    
            elif tipo_proceso == 'offboarding':
                # Procesar offboarding
                success, message, records = access_service.process_employee_offboarding(scotia_id)
                
                if success:
                    messagebox.showinfo("Éxito", f"Offboarding procesado exitosamente.\n{message}")
                    self.limpiar_campos()
                else:
                    messagebox.showerror("Error", message)
                    
            elif tipo_proceso == 'lateral':
                # Procesar movimiento lateral
                success, message, records = access_service.process_lateral_movement(
                    scotia_id,
                    datos_generales.get('nuevo_cargo', ''),
                    datos_generales.get('nueva_sub_unidad', '')
                )
                
                if success:
                    messagebox.showinfo("Éxito", f"Movimiento lateral procesado exitosamente.\n{message}")
                    self.limpiar_campos()
                else:
                    messagebox.showerror("Error", message)
            else:
                messagebox.showerror("Error", f"Tipo de proceso no soportado: {tipo_proceso}")
                
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
        """Muestra estadísticas de los datos almacenados usando la nueva estructura"""
        try:
            estadisticas = access_service.db_manager.get_database_stats()
            
            mensaje = "Estadísticas del Sistema (Nueva Estructura):\n\n"
            mensaje += f"Empleados en Headcount: {estadisticas.get('headcount', 0)}\n"
            mensaje += f"Empleados Activos: {estadisticas.get('empleados_activos', 0)}\n"
            mensaje += f"Aplicaciones Registradas: {estadisticas.get('applications', 0)}\n"
            mensaje += f"Aplicaciones Activas: {estadisticas.get('aplicaciones_activas', 0)}\n"
            mensaje += f"Registros en Histórico: {estadisticas.get('historico', 0)}\n"
            
            messagebox.showinfo("Estadísticas", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error obteniendo estadísticas: {str(e)}")
            print(f"Error en mostrar_estadisticas: {e}")

    def probar_deduplicacion(self):
        """Método de prueba para verificar la deduplicación de aplicaciones"""
        try:
            # Obtener un empleado de ejemplo para probar
            empleados = access_service.get_all_employees()
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados para probar")
                return
            
            empleado = empleados[0]
            position = empleado.get('position', '')
            unit = empleado.get('unit', '')
            
            if not position or not unit:
                messagebox.showwarning("Advertencia", f"Empleado {empleado.get('scotia_id')} no tiene posición o unidad válida")
                return
            
            # Probar deduplicación
            debug_info = access_service.debug_applications_by_position(position, unit)
            
            if "error" in debug_info:
                messagebox.showerror("Error", f"Error en debug: {debug_info['error']}")
                return
            
            mensaje = f"Prueba de Deduplicación para {empleado.get('scotia_id')}:\n\n"
            mensaje += f"Posición: {position}\n"
            mensaje += f"Unidad: {unit}\n\n"
            mensaje += f"Total sin deduplicación: {debug_info['total_without_dedup']}\n"
            mensaje += f"Total con deduplicación: {debug_info['total_with_dedup']}\n"
            mensaje += f"Duplicados encontrados: {debug_info['duplicates_found']}\n\n"
            
            if debug_info['duplicates_found'] > 0:
                mensaje += "Aplicaciones duplicadas encontradas:\n"
                for row in debug_info['all_rows']:
                    mensaje += f"- {row[0]} (Unit: {row[1]}, Subunit: {row[2]}, Position: {row[3]})\n"
            else:
                mensaje += "✅ No se encontraron duplicados"
            
            messagebox.showinfo("Prueba de Deduplicación", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en prueba de deduplicación: {str(e)}")
            print(f"Error en probar_deduplicacion: {e}")


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
        
        ttk.Button(entrada_frame, text="⚡ Asignar Accesos Automáticamente", 
                  command=self._asignar_accesos_automaticos, style="Warning.TButton").grid(row=3, column=0, pady=(0, 10), sticky="ew")
        
        
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
        
        # Treeview para mostrar resultados con campos de conciliación estricta
        columns = ('Acceso', 'Unidad', 'Subunidad', 'Posición', 'Rol', 'Estado', 'Acción')
        self.tree_resultados = ttk.Treeview(resultados_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas con anchos específicos
        column_widths = {
            'Acceso': 150,
            'Unidad': 100,
            'Subunidad': 100,
            'Posición': 120,
            'Rol': 100,
            'Estado': 80,
            'Acción': 80
        }
        
        for col in columns:
            self.tree_resultados.heading(col, text=col)
            self.tree_resultados.column(col, width=column_widths.get(col, 120), anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(resultados_frame, orient="vertical", command=self.tree_resultados.yview)
        self.tree_resultados.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree_resultados.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Mensaje inicial
        self.tree_resultados.insert('', 'end', values=('', '', '', '', '', 'Sin datos', ''))
    
    def _conciliar_accesos(self):
        """Ejecuta la conciliación de accesos para un SID específico usando la nueva estructura"""
        sid = self.sid_var.get().strip()
        if not sid:
            messagebox.showerror("Error", "Por favor ingrese un SID válido")
            return
        
        try:
            # Verificar si el empleado existe y tiene datos necesarios
            empleado = access_service.get_employee_by_id(sid)
            if not empleado:
                messagebox.showerror("Error", f"El empleado {sid} no existe en el headcount")
                return
            
            # Verificar si tiene posición y unidad
            if not empleado.get('position') or not empleado.get('unit'):
                respuesta = messagebox.askyesno(
                    "Datos Incompletos", 
                    f"El empleado {sid} no tiene posición o unidad definida.\n\n"
                    "¿Desea usar datos de ejemplo para probar la conciliación?\n"
                    "(Se asignará: ANALISTA SENIOR - TECNOLOGÍA)"
                )
                
                if respuesta:
                    # Actualizar con datos de ejemplo
                    conn = access_service.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE headcount 
                        SET position = 'ANALISTA SENIOR', unit = 'TECNOLOGÍA'
                        WHERE scotia_id = ?
                    """, (sid,))
                    conn.commit()
                    conn.close()
                    
                    # Crear aplicaciones de ejemplo si no existen
                    self._ensure_sample_applications()
                    
                    messagebox.showinfo("Datos Actualizados", 
                        "Se han asignado datos de ejemplo al empleado.\n"
                        "Ahora puede proceder con la conciliación.")
                else:
                    return
            
            # Usar el nuevo servicio de conciliación
            reporte = access_service.get_access_reconciliation_report(sid)
            
            if "error" in reporte:
                messagebox.showerror("Error", reporte["error"])
                return
            
            self.resultado_conciliacion = reporte
            self._mostrar_resultados_nuevos(reporte)
            messagebox.showinfo("Éxito", f"Conciliación completada para {sid}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la conciliación: {str(e)}")
    
    def _ensure_sample_applications(self):
        """Asegura que existan aplicaciones de ejemplo para la conciliación"""
        try:
            conn = access_service.get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existen aplicaciones para ANALISTA SENIOR en TECNOLOGÍA
            cursor.execute("""
                SELECT COUNT(*) FROM applications 
                WHERE unit = 'TECNOLOGÍA' AND position_role = 'ANALISTA SENIOR'
            """)
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Crear aplicaciones de ejemplo
                applications_data = [
                    ('Global', 'TECNOLOGÍA', 'DESARROLLO', 'JIRA', 'JIRA', 'ANALISTA SENIOR', 'USER', 'Aplicación', 'Desarrollo', 'Activo', 'Tecnología', 'Sistema de gestión de proyectos'),
                    ('Global', 'TECNOLOGÍA', 'DESARROLLO', 'CONFLUENCE', 'CONFLUENCE', 'ANALISTA SENIOR', 'USER', 'Aplicación', 'Desarrollo', 'Activo', 'Tecnología', 'Sistema de documentación'),
                    ('Global', 'TECNOLOGÍA', 'DESARROLLO', 'GITLAB', 'GITLAB', 'ANALISTA SENIOR', 'DEVELOPER', 'Aplicación', 'Desarrollo', 'Activo', 'Tecnología', 'Sistema de control de versiones'),
                    ('Global', 'TECNOLOGÍA', 'ANALISIS', 'POWER BI', 'POWER BI', 'ANALISTA SENIOR', 'ANALYST', 'Aplicación', 'Analytics', 'Activo', 'Tecnología', 'Herramienta de análisis de datos')
                ]
                
                for app in applications_data:
                    cursor.execute("""
                        INSERT OR IGNORE INTO applications 
                        (jurisdiction, unit, subunit, logical_access_name, alias, position_role, 
                         role_name, access_type, category, access_status, system_owner, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, app)
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            print(f"Error creando aplicaciones de ejemplo: {e}")
    
    def _asignar_accesos_automaticos(self):
        """Asigna accesos automáticamente según la unit y position del empleado"""
        sid = self.sid_var.get().strip()
        if not sid:
            messagebox.showerror("Error", "Por favor ingrese un SID válido")
            return
        
        try:
            # Confirmar la acción
            result = messagebox.askyesno(
                "Confirmar Asignación Automática",
                f"¿Está seguro de que desea asignar accesos automáticamente para {sid}?\n\n"
                "Esto creará tickets 'Pendiente' para los accesos que faltan y revocará los excesivos."
            )
            
            if not result:
                return
            
            # Llamar al método assign_accesses del servicio
            success, message, counts = access_service.assign_accesses(sid, "Sistema")
            
            if success:
                # Mostrar resultados
                resultado_texto = f"✅ {message}\n\n"
                resultado_texto += f"📊 Resumen:\n"
                resultado_texto += f"• Accesos otorgados: {counts['granted']}\n"
                resultado_texto += f"• Accesos revocados: {counts['revoked']}\n\n"
                resultado_texto += f"Los tickets han sido creados con estado 'Pendiente' en el historial."
                
                messagebox.showinfo("Asignación Completada", resultado_texto)
                
                # Actualizar la conciliación para mostrar los cambios
                self._conciliar_accesos()
                
            else:
                messagebox.showerror("Error", f"Error en la asignación automática: {message}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la asignación automática: {str(e)}")
    
    
    def _exportar_excel(self):
        """Exporta los resultados de conciliación a Excel"""
        if not self.resultado_conciliacion:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        try:
            # Adaptar la estructura de datos para el servicio de exportación
            adapted_data = self._adapt_data_for_export(self.resultado_conciliacion)
            
            output_path = export_service.export_reconciliation_tickets(
                [adapted_data],
                "Sistema Integrado"
            )
            
            messagebox.showinfo("Éxito", f"Archivo exportado exitosamente a:\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def _adapt_data_for_export(self, reconciliation_data):
        """Adapta los datos de conciliación para el formato esperado por el servicio de exportación"""
        try:
            employee = reconciliation_data.get('employee', {})
            
            # Adaptar estructura para el servicio de exportación
            adapted = {
                "person_info": {
                    "sid": employee.get('scotia_id', ''),
                    "area": employee.get('unit', ''),
                    "subunit": employee.get('subunit', ''),
                    "cargo": employee.get('position', '')
                },
                "current": reconciliation_data.get('current_access', []),
                "target": [],  # No tenemos datos de target en la nueva estructura
                "to_grant": self._adapt_access_list(reconciliation_data.get('to_grant', []), 'grant'),
                "to_revoke": self._adapt_access_list(reconciliation_data.get('to_revoke', []), 'revoke')
            }
            
            return adapted
            
        except Exception as e:
            return reconciliation_data
    
    def _adapt_access_list(self, access_list, action_type):
        """Adapta una lista de accesos para el formato de exportación"""
        adapted_list = []
        for access in access_list:
            adapted_item = {
                "sid": self.sid_var.get().strip(),
                "app_name": access.get('app_name', ''),
                "role_name": access.get('role_name', ''),
                "accion": "GRANT" if action_type == 'grant' else "REVOKE",
                "motivo": f"Acceso {'requerido' if action_type == 'grant' else 'excesivo'} para {access.get('app_name', '')}"
            }
            adapted_list.append(adapted_item)
        return adapted_list
    
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
    
    def _mostrar_resultados_nuevos(self, reporte):
        """Muestra los resultados de conciliación usando la nueva estructura con campos estrictos"""
        # Limpiar treeview
        self.tree_resultados.delete(*self.tree_resultados.get_children())
        
        # Mostrar accesos actuales
        current_access = reporte.get('current_access', [])
        for acceso in current_access:
            self.tree_resultados.insert('', 'end', values=(
                acceso.get('app_name', ''),
                acceso.get('unit', ''),
                acceso.get('subunit', ''),
                acceso.get('position_role', ''),
                acceso.get('role_name', 'Sin rol'),
                '✅ Activo',
                'Mantener'
            ))
        
        # Mostrar accesos a otorgar
        to_grant = reporte.get('to_grant', [])
        for acceso in to_grant:
            self.tree_resultados.insert('', 'end', values=(
                acceso.get('app_name', ''),
                acceso.get('unit', ''),
                acceso.get('subunit', ''),
                acceso.get('position_role', ''),
                acceso.get('role_name', 'Sin rol'),
                '❌ Faltante',
                '🟢 Otorgar'
            ))
        
        # Mostrar accesos a revocar
        to_revoke = reporte.get('to_revoke', [])
        for acceso in to_revoke:
            self.tree_resultados.insert('', 'end', values=(
                acceso.get('app_name', ''),
                acceso.get('unit', ''),
                acceso.get('subunit', ''),
                acceso.get('position_role', ''),
                acceso.get('role_name', 'Sin rol'),
                '⚠️ Excesivo',
                '🔴 Revocar'
            ))
        
        # Si no hay datos, mostrar mensaje
        if not current_access and not to_grant and not to_revoke:
            self.tree_resultados.insert('', 'end', values=('', '', '', '', '', 'Sin datos', ''))


class AplicacionesFrame:
    """Frame para la gestión de aplicaciones del sistema"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Usar el nuevo servicio de gestión de accesos
        # self.app_manager = ApplicationManager()  # Comentado para usar el nuevo servicio
        
        # Variables
        self.applications = []
        self.filtered_applications = []
        self.current_filter = ""
        
        # Variables para filtros múltiples
        self.filtros_activos = {}
        self.campos_filtro = {
            "Nombre Lógico": "logical_access_name",
            "Jurisdicción": "jurisdiction",
            "Unidad": "unit",
            "Subunidad": "subunit",
            "Alias": "alias",
            "Rol de Posición": "position_role",
            "Tipo de Acceso": "access_type",
            "Categoría": "category",
            "Propietario del Sistema": "system_owner",
            "Estado": "access_status",
            "Requiere Licencia": "require_licensing"
        }
        
        self._crear_interfaz()
        self._cargar_aplicaciones()
    
    def _crear_interfaz(self):
        """Crea la interfaz de gestión de aplicaciones"""
        # Título principal
        ttk.Label(self.frame, text="📱 Gestión de Aplicaciones del Sistema", 
                  style="Title.TLabel").grid(row=0, column=0, pady=(0, 25), sticky="ew")
        
        # Frame principal
        main_content = ttk.Frame(self.frame)
        main_content.grid(row=1, column=0, sticky="nsew", padx=20)
        main_content.columnconfigure(0, weight=1)
        main_content.rowconfigure(2, weight=1)  # Cambiar de row 1 a row 2 para la tabla
        
        # Barra de herramientas
        self._crear_barra_herramientas(main_content)
        
        # Panel de filtros múltiples
        self._crear_panel_filtros_aplicaciones(main_content)
        
        # Tabla de aplicaciones
        self._crear_tabla_aplicaciones(main_content)
        
        # Barra de estado
        self._crear_barra_estado(main_content)
    
    def _crear_barra_herramientas(self, parent):
        """Crea la barra de herramientas"""
        toolbar = ttk.Frame(parent)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Botones principales
        ttk.Button(toolbar, text="➕ Nueva Aplicación", command=self._agregar_aplicacion, 
                  style="Success.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text="✏️ Editar", command=self._editar_aplicacion, 
                  style="Info.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text="🗑️ Eliminar", command=self._eliminar_aplicacion, 
                  style="Danger.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Búsqueda
        ttk.Label(toolbar, text="🔍 Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_busqueda_change)
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de actualizar
        ttk.Button(toolbar, text="🔄 Actualizar", command=self._actualizar_datos).pack(side=tk.LEFT)
        
        # Botón de exportar
        ttk.Button(toolbar, text="📊 Exportar", command=self._exportar_datos).pack(side=tk.LEFT, padx=(10, 0))
    
    def _crear_panel_filtros_aplicaciones(self, parent):
        """Crea el panel de filtros múltiples para aplicaciones"""
        # Frame para filtros
        filtros_frame = ttk.LabelFrame(parent, text="Filtros Múltiples", padding="10")
        filtros_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0))
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
        
        ttk.Button(botones_filtros, text="Eliminar", command=self._eliminar_filtro_seleccionado_apps).pack(side=tk.TOP, pady=2)
        ttk.Button(botones_filtros, text="Limpiar", command=self._limpiar_todos_filtros_apps).pack(side=tk.TOP, pady=2)
        
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
        ttk.Button(nuevo_filtro_frame, text="Agregar Filtro", command=self._agregar_filtro_apps).grid(row=0, column=4, padx=(0, 5), pady=5)
        
        # Botones de acción
        botones_accion = ttk.Frame(filtros_frame)
        botones_accion.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(botones_accion, text="Aplicar Filtros", command=self._aplicar_filtros_multiples_apps).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botones_accion, text="Mostrar Todas", command=self._mostrar_todas_aplicaciones).pack(side=tk.LEFT)
        
        # Bind para Enter en el campo de texto
        self.entry_filtro.bind('<Return>', lambda e: self._agregar_filtro_apps())
    
    def _agregar_filtro_apps(self):
        """Agrega un nuevo filtro a la lista de aplicaciones"""
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
            self._actualizar_lista_filtros_apps()
            
            # Limpiar campos
            self.entry_filtro.delete(0, tk.END)
            self.combo_campo.set("")
    
    def _eliminar_filtro_seleccionado_apps(self):
        """Elimina el filtro seleccionado de la lista de aplicaciones"""
        seleccion = self.filtros_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            campo = list(self.filtros_activos.keys())[indice]
            del self.filtros_activos[campo]
            self._actualizar_lista_filtros_apps()
    
    def _limpiar_todos_filtros_apps(self):
        """Limpia todos los filtros activos de aplicaciones"""
        self.filtros_activos.clear()
        self._actualizar_lista_filtros_apps()
    
    def _actualizar_lista_filtros_apps(self):
        """Actualiza la lista visual de filtros activos de aplicaciones"""
        self.filtros_listbox.delete(0, tk.END)
        for campo, valor in self.filtros_activos.items():
            self.filtros_listbox.insert(tk.END, f"{campo}: {valor}")
    
    def _aplicar_filtros_multiples_apps(self):
        """Aplica todos los filtros activos para aplicaciones"""
        if not self.filtros_activos:
            messagebox.showwarning("Advertencia", "No hay filtros activos para aplicar")
            return
        
        try:
            # Aplicar filtros múltiples
            resultados_filtrados = self._aplicar_filtros_en_memoria_apps(self.applications)
            
            # Mostrar resultados
            if resultados_filtrados:
                self.filtered_applications = resultados_filtrados
                self._actualizar_tabla()
                self._actualizar_estado(f"🔍 Mostrando {len(resultados_filtrados)} de {len(self.applications)} aplicaciones con filtros aplicados")
            else:
                messagebox.showinfo("Filtros", "No se encontraron aplicaciones que coincidan con los filtros aplicados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error aplicando filtros: {str(e)}")
    
    def _aplicar_filtros_en_memoria_apps(self, aplicaciones):
        """Aplica los filtros activos a las aplicaciones en memoria"""
        if not aplicaciones:
            return aplicaciones
        
        resultados_filtrados = []
        for app in aplicaciones:
            cumple_filtros = True
            
            for campo_ui, valor_filtro in self.filtros_activos.items():
                campo_bd = self.campos_filtro.get(campo_ui)
                if campo_bd:
                    valor_campo = str(app.get(campo_bd, '')).lower()
                    if valor_filtro.lower() not in valor_campo:
                        cumple_filtros = False
                        break
            
            if cumple_filtros:
                resultados_filtrados.append(app)
        
        return resultados_filtrados
    
    def _mostrar_todas_aplicaciones(self):
        """Muestra todas las aplicaciones sin filtros"""
        self.filtros_activos.clear()
        self._actualizar_lista_filtros_apps()
        self.filtered_applications = self.applications.copy()
        self._actualizar_tabla()
        self._actualizar_estado(f"✅ Mostrando todas las {len(self.applications)} aplicaciones")
    
    def _crear_tabla_aplicaciones(self, parent):
        """Crea la tabla de aplicaciones"""
        # Frame para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Crear Treeview - Actualizado para coincidir con tabla applications
        columns = ('ID', 'Logical Access Name', 'Alias', 'Unit', 'Position Role', 'System Owner', 'Access Status', 'Category')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Logical Access Name', text='Logical Access Name')
        self.tree.heading('Alias', text='Alias')
        self.tree.heading('Unit', text='Unit')
        self.tree.heading('Position Role', text='Position Role')
        self.tree.heading('System Owner', text='System Owner')
        self.tree.heading('Access Status', text='Access Status')
        self.tree.heading('Category', text='Category')
        
        # Configurar anchos de columna
        self.tree.column('ID', width=50, minwidth=50)
        self.tree.column('Logical Access Name', width=180, minwidth=150)
        self.tree.column('Alias', width=120, minwidth=100)
        self.tree.column('Unit', width=120, minwidth=100)
        self.tree.column('Position Role', width=150, minwidth=120)
        self.tree.column('System Owner', width=120, minwidth=100)
        self.tree.column('Access Status', width=100, minwidth=80)
        self.tree.column('Category', width=120, minwidth=100)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid de la tabla
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Eventos
        self.tree.bind('<Double-1>', self._on_doble_clic)
        self.tree.bind('<Delete>', lambda e: self._eliminar_aplicacion())
    
    def _crear_barra_estado(self, parent):
        """Crea la barra de estado"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky="ew", pady=(15, 0))
        
        self.status_label = ttk.Label(status_frame, text="Listo", style="Success.TLabel")
        self.status_label.pack(side=tk.LEFT)
        
        # Información de la base de datos
        self.db_info_label = ttk.Label(status_frame, text="", style="Header.TLabel")
        self.db_info_label.pack(side=tk.RIGHT)
    
    def _cargar_aplicaciones(self):
        """Carga las aplicaciones desde la nueva estructura de base de datos"""
        try:
            self.applications = access_service.get_all_applications()
            self.filtered_applications = self.applications.copy()
            self._actualizar_tabla()
            self._actualizar_estado(f"✅ Cargadas {len(self.applications)} aplicaciones")
            self._actualizar_info_bd()
        except Exception as e:
            self._actualizar_estado(f"❌ Error al cargar aplicaciones: {str(e)}", error=True)
    
    def _actualizar_tabla(self):
        """Actualiza la tabla con los datos actuales"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar datos filtrados
        for app in self.filtered_applications:
            # Formatear fecha
            fecha = app.get('fecha_creacion', '')
            try:
                fecha_formatted = datetime.fromisoformat(fecha).strftime('%d/%m/%Y %H:%M') if fecha else 'N/A'
            except:
                fecha_formatted = fecha or 'N/A'
            
            # Determinar color del estado
            status = app.get('status', 'Activo')
            tags = ('active',) if status == 'Activo' else ('inactive',) if status == 'Inactivo' else ('maintenance',)
            
            self.tree.insert('', 'end', values=(
                app.get('id', ''),
                app.get('logical_access_name', ''),
                app.get('alias', ''),
                app.get('unit', ''),
                app.get('position_role', ''),
                app.get('system_owner', ''),
                app.get('access_status', ''),
                app.get('category', '')
            ), tags=tags)
        
        # Configurar colores de las filas
        self.tree.tag_configure('active', background='#d4edda')
        self.tree.tag_configure('inactive', background='#f8d7da')
        self.tree.tag_configure('maintenance', background='#fff3cd')
    
    def _on_busqueda_change(self, *args):
        """Maneja cambios en la búsqueda"""
        search_term = self.search_var.get().lower()
        self.current_filter = search_term
        
        if not search_term:
            self.filtered_applications = self.applications.copy()
        else:
            self.filtered_applications = [
                app for app in self.applications
                if (search_term in app.get('logical_access_name', '').lower() or
                    search_term in app.get('alias', '').lower() or
                    search_term in app.get('unit', '').lower() or
                    search_term in app.get('position_role', '').lower() or
                    search_term in app.get('system_owner', '').lower() or
                    search_term in app.get('category', '').lower())
            ]
        
        self._actualizar_tabla()
        self._actualizar_estado(f"🔍 Mostrando {len(self.filtered_applications)} de {len(self.applications)} aplicaciones")
    
    def _agregar_aplicacion(self):
        """Abre diálogo para agregar nueva aplicación usando la nueva estructura"""
        # Usar valores por defecto para categorías y propietarios
        categories = ["RRHH", "Tecnología", "Finanzas", "Operaciones", "Marketing", "Comunicaciones"]
        owners = ["Admin", "RRHH", "Tecnología", "Finanzas", "Operaciones", "Marketing", "Comunicaciones"]
        
        dialog = ApplicationDialog(self.frame, "Nueva Aplicación", categories=categories, owners=owners)
        self.frame.wait_window(dialog.dialog)
        
        if dialog.result:
            success, message = access_service.create_application(dialog.result)
            
            if success:
                self._actualizar_estado("✅ Aplicación agregada correctamente")
                self._cargar_aplicaciones()
            else:
                self._actualizar_estado(f"❌ Error al agregar aplicación: {message}", error=True)
    
    def _editar_aplicacion(self):
        """Edita la aplicación seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una aplicación para editar")
            return
        
        item = self.tree.item(selection[0])
        app_id = item['values'][0]
        
        # Buscar la aplicación en la lista
        app_data = None
        for app in self.applications:
            if app['id'] == app_id:
                app_data = app
                break
        
        if not app_data:
            messagebox.showerror("Error", "No se pudo encontrar la aplicación seleccionada")
            return
        
        # Usar valores por defecto para categorías y propietarios
        categories = ["RRHH", "Tecnología", "Finanzas", "Operaciones", "Marketing", "Comunicaciones"]
        owners = ["Admin", "RRHH", "Tecnología", "Finanzas", "Operaciones", "Marketing", "Comunicaciones"]
        
        dialog = ApplicationDialog(self.frame, "Editar Aplicación", app_data, categories, owners)
        self.frame.wait_window(dialog.dialog)
        
        if dialog.result:
            # Usar el access_service para actualizar la aplicación
            success, message = access_service.update_application(app_id, dialog.result)
            
            if success:
                self._actualizar_estado("✅ Aplicación actualizada correctamente")
                self._cargar_aplicaciones()
            else:
                self._actualizar_estado(f"❌ Error al actualizar aplicación: {message}", error=True)
    
    def _eliminar_aplicacion(self):
        """Elimina la aplicación seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una aplicación para eliminar")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        if len(values) < 2:
            messagebox.showerror("Error", "Datos de aplicación no válidos")
            return
            
        app_id = values[0]  # ID está en la posición 0
        app_name = values[1]  # Nombre está en la posición 1
        
        # Confirmar eliminación
        result = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la aplicación '{app_name}'?\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if result:
            # Usar el access_service para eliminar la aplicación
            success, message = access_service.delete_application(app_id)
            if success:
                self._actualizar_estado("✅ Aplicación eliminada correctamente")
                self._cargar_aplicaciones()
            else:
                self._actualizar_estado(f"❌ Error al eliminar aplicación: {message}", error=True)
    
    def _on_doble_clic(self, event):
        """Maneja doble clic en la tabla"""
        self._editar_aplicacion()
    
    def _actualizar_datos(self):
        """Actualiza los datos desde la base de datos"""
        self._cargar_aplicaciones()
        self._actualizar_estado("🔄 Datos actualizados")
    
    def _exportar_datos(self):
        """Exporta los datos a un archivo CSV"""
        try:
            import csv
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar como CSV"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['ID', 'Logical Access Name', 'Alias', 'Unit', 'Position Role', 'System Owner', 'Access Status', 'Category']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for app in self.filtered_applications:
                        writer.writerow({
                            'ID': app.get('id', ''),
                            'Logical Access Name': app.get('logical_access_name', ''),
                            'Alias': app.get('alias', ''),
                            'Unit': app.get('unit', ''),
                            'Position Role': app.get('position_role', ''),
                            'System Owner': app.get('system_owner', ''),
                            'Access Status': app.get('access_status', ''),
                            'Category': app.get('category', '')
                        })
                
                self._actualizar_estado(f"📊 Datos exportados a {filename}")
                messagebox.showinfo("Éxito", f"Los datos se exportaron correctamente a:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos: {str(e)}")
            self._actualizar_estado("❌ Error al exportar datos", error=True)
    
    def _actualizar_estado(self, message: str, error: bool = False):
        """Actualiza el mensaje de estado"""
        if error:
            self.status_label.config(text=message, style="Error.TLabel")
        else:
            self.status_label.config(text=message, style="Success.TLabel")
    
    def _actualizar_info_bd(self):
        """Actualiza la información de la base de datos usando la nueva estructura"""
        try:
            stats = access_service.db_manager.get_database_stats()
            total_apps = stats.get('applications', 0)
            self.db_info_label.config(text=f"Total aplicaciones: {total_apps}")
        except:
            self.db_info_label.config(text="Base de datos no disponible")


class ApplicationManager:
    """Clase para gestionar las aplicaciones en la base de datos"""
    
    def __init__(self, db_path: str = None):
        import os
        # Use the database file directly
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'database', 'empleados.db')
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Base de datos no encontrada: {self.db_path}")
        return sqlite3.connect(self.db_path)
    
    def get_all_applications(self) -> list:
        """Obtiene todas las aplicaciones de la base de datos"""
        try:    
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, app_name, description, category, owner, status, fecha_creacion
                FROM applications
                ORDER BY app_name
            """)
            
            columns = [description[0] for description in cursor.description]
            applications = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return applications
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener aplicaciones: {str(e)}")
            return []
    
    def add_application(self, app_name: str, description: str, category: str, owner: str) -> bool:
        """Agrega una nueva aplicación a la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO applications (app_name, description, category, owner, status, fecha_creacion)
                VALUES (?, ?, ?, ?, 'Activo', ?)
            """, (app_name, description, category, owner, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe una aplicación con ese nombre")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar aplicación: {str(e)}")
            return False
    
    def update_application(self, app_id: int, app_name: str, description: str, category: str, owner: str, status: str) -> bool:
        """Actualiza una aplicación existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE applications 
                SET app_name = ?, description = ?, category = ?, owner = ?, status = ?
                WHERE id = ?
            """, (app_name, description, category, owner, status, app_id))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe una aplicación con ese nombre")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar aplicación: {str(e)}")
            return False
    
    def delete_application(self, app_id: int) -> bool:
        """Elimina una aplicación de la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar dependencias
            cursor.execute("SELECT COUNT(*) FROM roles WHERE app_name = (SELECT app_name FROM applications WHERE id = ?)", (app_id,))
            roles_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM procesos WHERE app_name = (SELECT app_name FROM applications WHERE id = ?)", (app_id,))
            procesos_count = cursor.fetchone()[0]
            
            if roles_count > 0 or procesos_count > 0:
                messagebox.showwarning("Advertencia", 
                    f"No se puede eliminar la aplicación porque tiene {roles_count} roles y {procesos_count} procesos asociados.\n"
                    "Elimine las dependencias primero o cambie el estado a 'Inactivo'.")
                conn.close()
                return False
            
            cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar aplicación: {str(e)}")
            return False
    
    def get_categories(self) -> list:
        """Obtiene las categorías únicas de aplicaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM applications ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            conn.close()
            return categories
        except Exception:
            return ["RRHH", "Tecnología", "Finanzas", "Operaciones", "Marketing", "Comunicaciones"]
    
    def get_owners(self) -> list:
        """Obtiene los propietarios únicos de aplicaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT owner FROM applications ORDER BY owner")
            owners = [row[0] for row in cursor.fetchall()]
            conn.close()
            return owners
        except Exception:
            return ["Admin", "RRHH", "Tecnología", "Finanzas", "Operaciones", "Marketing", "Comunicaciones"]


class ApplicationDialog:
    """Diálogo para agregar/editar aplicaciones"""
    
    def __init__(self, parent, title: str, app_data: dict = None, categories: list = None, owners: list = None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar el diálogo
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.app_data = app_data
        self.categories = categories or []
        self.owners = owners or []
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
        title_label = ttk.Label(scrollable_frame, text="Información de la Aplicación", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos actualizados para coincidir con tabla applications
        campos = [
            ("Jurisdiction:", "jurisdiction", "entry"),
            ("Unit:", "unit", "combobox", ["Tecnología", "Recursos Humanos", "Finanzas", "Marketing", "Operaciones", "Ventas", "Legal"]),
            ("Subunit:", "subunit", "entry"),
            ("Logical Access Name:", "logical_access_name", "entry"),
            ("Alias:", "alias", "entry"),
            ("Path/Email/URL:", "path_email_url", "entry"),
            ("Position Role:", "position_role", "entry"),
            ("Exception Tracking:", "exception_tracking", "entry"),
            ("Fulfillment Action:", "fulfillment_action", "entry"),
            ("System Owner:", "system_owner", "entry"),
            ("Role Name:", "role_name", "entry"),
            ("Access Type:", "access_type", "combobox", ["Aplicación", "Sistema", "Base de Datos", "Red", "Hardware"]),
            ("Category:", "category", "combobox", ["Sistemas", "Desarrollo", "RRHH", "ERP", "Analytics", "DevOps", "Recursos"]),
            ("Additional Data:", "additional_data", "entry"),
            ("AD Code:", "ad_code", "entry"),
            ("Access Status:", "access_status", "combobox", ["Activo", "Inactivo", "Mantenimiento"]),
            ("Require Licensing:", "require_licensing", "entry"),
            ("Description:", "description", "text"),
            ("Authentication Method:", "authentication_method", "combobox", ["LDAP", "SSO", "Local", "OAuth", "SAML"])
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
        if 'logical_access_name' in self.widgets:
            self.widgets['logical_access_name'].focus()
        
        self.dialog.bind('<Return>', lambda e: self._save())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _load_data(self):
        """Carga los datos existentes si es una edición"""
        if self.app_data:
            for var_name, var in self.variables.items():
                if var_name in self.app_data:
                    if isinstance(var, tk.StringVar):
                        var.set(str(self.app_data[var_name]) if self.app_data[var_name] is not None else '')
                    elif isinstance(var, tk.Text):
                        var.delete('1.0', tk.END)
                        var.insert('1.0', str(self.app_data[var_name]) if self.app_data[var_name] is not None else '')
    
    def _save(self):
        """Guarda los datos del formulario"""
        # Validaciones básicas
        if not self.variables['logical_access_name'].get().strip():
            messagebox.showerror("Error", "El Logical Access Name es obligatorio")
            return
        
        if not self.variables['unit'].get().strip():
            messagebox.showerror("Error", "La Unit es obligatoria")
            return
        
        # Preparar datos
        self.result = {}
        for var_name, var in self.variables.items():
            if isinstance(var, tk.StringVar):
                self.result[var_name] = var.get().strip()
            elif isinstance(var, tk.Text):
                self.result[var_name] = var.get('1.0', tk.END).strip()
        
        # Establecer valores por defecto si están vacíos
        if not self.result.get('access_status'):
            self.result['access_status'] = 'Activo'
        if not self.result.get('jurisdiction'):
            self.result['jurisdiction'] = 'Global'
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AppEmpleadosRefactorizada(root)
    root.mainloop()


if __name__ == "__main__":
    main()