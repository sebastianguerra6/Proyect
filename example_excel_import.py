#!/usr/bin/env python3
"""
Ejemplo de uso de las clases de importación de Excel
"""
import sys
import os
sys.path.append('services')
from excel_importer import ExcelToSQLiteImporter, ExcelToSQLServerImporter, import_excel_to_sqlite, import_excel_to_sqlserver

def example_sqlite_import():
    """Ejemplo de importación a SQLite"""
    print("=== EJEMPLO: IMPORTACIÓN A SQLITE ===")
    
    # Método 1: Usando la clase directamente
    importer = ExcelToSQLiteImporter()
    
    try:
        # Importar empleados
        success, message, count = importer.import_from_excel(
            excel_path="data/empleados.xlsx",
            sheet_name="headcount",
            table_name="headcount",
            skip_rows=1  # Saltar encabezados
        )
        print(f"Empleados: {success} - {message}")
        
        # Importar aplicaciones
        success, message, count = importer.import_from_excel(
            excel_path="data/aplicaciones.xlsx",
            sheet_name="applications",
            table_name="applications",
            skip_rows=1
        )
        print(f"Aplicaciones: {success} - {message}")
        
        # Importar histórico
        success, message, count = importer.import_from_excel(
            excel_path="data/historico.xlsx",
            sheet_name="historico",
            table_name="historico",
            skip_rows=1
        )
        print(f"Histórico: {success} - {message}")
        
    finally:
        importer.close()
    
    # Método 2: Usando función de conveniencia
    print("\n--- Usando función de conveniencia ---")
    success, message, count = import_excel_to_sqlite(
        excel_path="data/empleados.xlsx",
        sheet_name="headcount",
        table_name="headcount",
        skip_rows=1
    )
    print(f"Resultado: {success} - {message}")


def example_sqlserver_import():
    """Ejemplo de importación a SQL Server"""
    print("\n=== EJEMPLO: IMPORTACIÓN A SQL SERVER ===")
    
    # Configuración de SQL Server
    server = "localhost\\SQLEXPRESS"  # Cambiar por tu servidor
    database = "EmpleadosDB"  # Cambiar por tu base de datos
    username = "sa"  # Cambiar por tu usuario
    password = "tu_password"  # Cambiar por tu contraseña
    
    # Método 1: Usando la clase directamente
    importer = ExcelToSQLServerImporter(
        server=server,
        database=database,
        username=username,
        password=password,
        trusted_connection=False
    )
    
    try:
        # Crear tablas
        success, message = importer.create_tables()
        print(f"Crear tablas: {success} - {message}")
        
        if success:
            # Importar empleados
            success, message, count = importer.import_from_excel(
                excel_path="data/empleados.xlsx",
                sheet_name="headcount",
                table_name="headcount",
                skip_rows=1
            )
            print(f"Empleados: {success} - {message}")
            
            # Importar aplicaciones
            success, message, count = importer.import_from_excel(
                excel_path="data/aplicaciones.xlsx",
                sheet_name="applications",
                table_name="applications",
                skip_rows=1
            )
            print(f"Aplicaciones: {success} - {message}")
            
    finally:
        importer.close()
    
    # Método 2: Usando función de conveniencia
    print("\n--- Usando función de conveniencia ---")
    success, message, count = import_excel_to_sqlserver(
        excel_path="data/empleados.xlsx",
        sheet_name="headcount",
        table_name="headcount",
        server=server,
        database=database,
        username=username,
        password=password,
        trusted_connection=False,
        skip_rows=1
    )
    print(f"Resultado: {success} - {message}")


def example_with_trusted_connection():
    """Ejemplo con conexión de confianza (Windows Authentication)"""
    print("\n=== EJEMPLO: CONEXIÓN DE CONFIANZA ===")
    
    success, message, count = import_excel_to_sqlserver(
        excel_path="data/empleados.xlsx",
        sheet_name="headcount",
        table_name="headcount",
        server="localhost\\SQLEXPRESS",
        database="EmpleadosDB",
        trusted_connection=True,  # Usar Windows Authentication
        skip_rows=1
    )
    print(f"Resultado: {success} - {message}")


if __name__ == "__main__":
    print("Ejemplos de importación de Excel a bases de datos")
    print("=" * 50)
    
    # Ejecutar ejemplos (comentados para evitar errores sin archivos)
    # example_sqlite_import()
    # example_sqlserver_import()
    # example_with_trusted_connection()
    
    print("\nPara usar estos ejemplos:")
    print("1. Crea archivos Excel con las columnas correctas")
    print("2. Descomenta las líneas de ejemplo")
    print("3. Ajusta las rutas y configuraciones según tu entorno")
    print("\nEstructura de archivos Excel esperada:")
    print("- empleados.xlsx (hoja 'headcount')")
    print("- aplicaciones.xlsx (hoja 'applications')")
    print("- historico.xlsx (hoja 'historico')")
