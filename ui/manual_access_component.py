"""
Componente para crear registros manuales de acceso
"""
import tkinter as tk
from tkinter import ttk, messagebox


class ManualAccessDialog:
    """Diálogo para crear registros manuales de acceso"""
    
    def __init__(self, parent, service=None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("➕ Crear Registro Manual de Acceso")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.service = service
        self.result = None
        
        # Variables
        self.variables = {
            'scotia_id': tk.StringVar(),
            'app_name': tk.StringVar(),
            'responsible': tk.StringVar(value="Manual"),
            'description': tk.StringVar()
        }
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="➕ Crear Registro Manual de Acceso", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Campos del formulario
        campos = [
            ("ID de Empleado (Scotia ID):", "scotia_id", "entry"),
            ("Aplicación:", "app_name", "combobox"),
            ("Responsable:", "responsible", "entry"),
            ("Descripción (opcional):", "description", "entry")
        ]
        
        for i, (label_text, var_name, widget_type) in enumerate(campos):
            # Label
            ttk.Label(main_frame, text=label_text, font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky="w", pady=5, padx=(0, 10))
            
            # Widget
            if widget_type == "entry":
                widget = ttk.Entry(main_frame, textvariable=self.variables[var_name], width=40)
            elif widget_type == "combobox":
                widget = ttk.Combobox(main_frame, textvariable=self.variables[var_name], width=37)
                # Cargar aplicaciones disponibles
                self._load_applications(widget)
            else:
                widget = ttk.Entry(main_frame, textvariable=self.variables[var_name], width=40)
            
            widget.grid(row=i, column=1, sticky="ew", pady=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(campos), column=0, columnspan=2, pady=20, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        ttk.Button(button_frame, text="Crear Registro", command=self._create_record, 
                  style="Success.TButton").grid(row=0, column=0, padx=(0, 10), sticky="ew")
        ttk.Button(button_frame, text="Cancelar", command=self._cancel, 
                  style="Danger.TButton").grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        # Información adicional
        info_text = """
ℹ️ Información:
• Este registro se creará como "manual_access" en el historial
• El empleado debe existir en el headcount
• La aplicación se puede seleccionar de la lista o escribir una nueva
• El registro quedará en estado "Pendiente" para su procesamiento
        """
        ttk.Label(main_frame, text=info_text, font=("Arial", 9), 
                 foreground="gray").grid(row=len(campos)+1, column=0, columnspan=2, 
                                       pady=(10, 0), sticky="w")
    
    def _load_applications(self, combobox):
        """Carga las aplicaciones disponibles en el combobox"""
        try:
            if self.service:
                applications = self.service.get_available_applications()
                app_names = [app['name'] for app in applications]
                combobox['values'] = app_names
        except Exception as e:
            print(f"Error cargando aplicaciones: {e}")
    
    def _create_record(self):
        """Crea el registro manual"""
        try:
            # Validar campos obligatorios
            scotia_id = self.variables['scotia_id'].get().strip()
            app_name = self.variables['app_name'].get().strip()
            responsible = self.variables['responsible'].get().strip()
            description = self.variables['description'].get().strip()
            
            if not scotia_id:
                messagebox.showerror("Error", "El ID de empleado es obligatorio")
                return
            
            if not app_name:
                messagebox.showerror("Error", "El nombre de la aplicación es obligatorio")
                return
            
            if not responsible:
                responsible = "Manual"
            
            if not description:
                description = None
            
            # Crear el registro
            if self.service:
                success, message = self.service.create_manual_access_record(
                    scotia_id, app_name, responsible, description
                )
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.result = {
                        'scotia_id': scotia_id,
                        'app_name': app_name,
                        'responsible': responsible,
                        'description': description
                    }
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Error", message)
            else:
                messagebox.showerror("Error", "Servicio no disponible")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error creando registro: {str(e)}")
    
    def _cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()
