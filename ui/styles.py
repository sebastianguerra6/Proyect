"""
Estilos personalizados para la aplicación de empleados
"""
from tkinter import ttk

def aplicar_estilos_personalizados():
    """Aplica estilos personalizados a toda la aplicación"""
    style = ttk.Style()
    
    # Configurar tema base
    try:
        style.theme_use('clam')
    except:
        pass
    
    # Estilos para botones de navegación
    style.configure('Nav.TButton', 
                   font=('Arial', 11, 'bold'),
                   padding=(15, 12),
                   relief='raised',
                   borderwidth=2)
    
    style.map('Nav.TButton',
              background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')],
              relief=[('pressed', 'sunken'), ('active', 'raised')])
    
    # Estilos para botón de salida
    style.configure('Salir.TButton', 
                   font=('Arial', 11, 'bold'),
                   padding=(15, 12),
                   relief='raised',
                   borderwidth=2,
                   foreground='#d32f2f')
    
    style.map('Salir.TButton',
              background=[('active', '#ffcdd2'), ('pressed', '#ef9a9a')],
              relief=[('pressed', 'sunken'), ('active', 'raised')])
    
    # Estilos para botones de acción
    estilos_botones = {
        'Success.TButton': {'background': '#e8f5e8', 'foreground': '#2e7d32'},
        'Info.TButton': {'background': '#e3f2fd', 'foreground': '#1565c0'},
        'Warning.TButton': {'background': '#fff3e0', 'foreground': '#ef6c00'},
        'Danger.TButton': {'background': '#ffebee', 'foreground': '#d32f2f'}
    }
    
    for nombre, colores in estilos_botones.items():
        style.configure(nombre, 
                       font=('Arial', 10, 'bold'),
                       padding=(12, 8),
                       relief='raised',
                       borderwidth=2,
                       **colores)
    
    # Estilos para labels
    estilos_labels = {
        'Title.TLabel': {'font': ('Arial', 20, 'bold'), 'foreground': '#1976d2'},
        'Section.TLabel': {'font': ('Arial', 18, 'bold'), 'foreground': '#388e3c'},
        'Subsection.TLabel': {'font': ('Arial', 14, 'bold'), 'foreground': '#1976d2'}
    }
    
    for nombre, config in estilos_labels.items():
        style.configure(nombre, **config)
    
    # Estilos para frames
    style.configure('Main.TFrame', relief='flat', borderwidth=0)
    style.configure('Nav.TLabelframe', relief='raised', borderwidth=2)
    
    # Estilos para pestañas
    style.configure('TNotebook.Tab',
                   font=('Arial', 10, 'bold'),
                   padding=(15, 8))
    
    style.map('TNotebook.Tab',
              background=[('selected', '#e3f2fd'), ('active', '#f5f5f5')],
              foreground=[('selected', '#1976d2'), ('active', '#333333')])
