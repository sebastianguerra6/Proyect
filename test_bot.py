#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asistente simple de estructuras de SQL Server (solo metadatos).

Funcionalidades:
1) Construir un catálogo de columnas (JSON) recorriendo varias bases de datos.
2) Iniciar un "chat" en consola para buscar tablas/columnas por descripción.

Requisitos:
    pip install pyodbc

Uso:
    # 1. Construir catálogo
    python db_schema_assistant.py --build-catalog

    # 2. Iniciar chat
    python db_schema_assistant.py

IMPORTANTE:
- Se conecta usando Trusted Connection (Windows Authentication).
- Tu usuario de Windows debe tener como mínimo:
    GRANT VIEW DEFINITION
  en las bases de datos que quieras catalogar.
"""

import pyodbc
import json
import os
import difflib
import argparse
from typing import List, Dict, Any

# ==========================
# CONFIGURACIÓN
# ==========================

# Nombre del servidor SQL Server (puede ser nombre o IP)
# Ejemplos:
#   "MI-SQL-SRV"
#   "MI-SQL-SRV\\INSTANCIA"
#   "10.0.0.5"
SQL_SERVER = "TU_SERVIDOR_SQL"

# Lista de bases de datos a catalogar (usa los nombres reales)
DATABASES = [
    "BaseCoreBanking",
    "BaseTarjetas",
    "BaseClientes",
    # Agrega las que necesites
]

# Archivo donde se guarda el catálogo
CATALOG_FILE = "schema_catalog.json"


# ==========================
# CONEXIÓN A SQL SERVER
# ==========================

def get_connection(database: str):
    """
    Crea una conexión a una base de datos específica de SQL Server
    usando Trusted Connection (Windows Authentication).
    """
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


# ==========================
# CONSTRUCCIÓN DEL CATÁLOGO
# ==========================

def build_catalog() -> List[Dict[str, Any]]:
    """
    Recorre las bases de datos configuradas y arma un catálogo de columnas.

    SOLO lee metadatos (sys.tables, sys.columns, etc.).
    No se leen filas de datos.
    """
    catalog = []

    for db_name in DATABASES:
        print(f"[INFO] Catalogando base de datos: {db_name} ...")
        conn = get_connection(db_name)
        cursor = conn.cursor()

        # Consulta de metadatos (tablas, columnas, tipos)
        # Incluye descripción si se usa MS_Description en extended properties
        cursor.execute("""
            SELECT
                DB_NAME() AS database_name,
                s.name AS schema_name,
                t.name AS table_name,
                c.name AS column_name,
                ty.name AS data_type,
                c.max_length,
                c.is_nullable,
                ep.value AS column_description
            FROM sys.tables t
            INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
            INNER JOIN sys.columns c ON c.object_id = t.object_id
            INNER JOIN sys.types ty ON ty.user_type_id = c.user_type_id
            LEFT JOIN sys.extended_properties ep 
                ON ep.major_id = c.object_id
               AND ep.minor_id = c.column_id
               AND ep.name = 'MS_Description'
            ORDER BY s.name, t.name, c.column_id;
        """)

        rows = cursor.fetchall()
        for row in rows:
            catalog.append({
                "database": row.database_name,
                "schema": row.schema_name,
                "table": row.table_name,
                "column": row.column_name,
                "data_type": row.data_type,
                "max_length": int(row.max_length) if row.max_length is not None else None,
                "is_nullable": bool(row.is_nullable),
                "description": str(row.column_description) if row.column_description is not None else ""
            })

        conn.close()

    print(f"[INFO] Se catalogaron {len(catalog)} columnas en total.")
    return catalog


def save_catalog(catalog: List[Dict[str, Any]], filename: str = CATALOG_FILE):
    """
    Guarda el catálogo en un archivo JSON.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Catálogo guardado en: {filename}")


def load_catalog(filename: str = CATALOG_FILE) -> List[Dict[str, Any]]:
    """
    Carga el catálogo desde un archivo JSON.
    """
    if not os.path.exists(filename):
        print(f"[ERROR] No se encontró el archivo {filename}.")
        print("        Primero ejecuta el script con --build-catalog.")
        return []

    with open(filename, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    print(f"[INFO] Catálogo cargado. Columnas totales: {len(catalog)}")
    return catalog


# ==========================
# BÚSQUEDA "INTELIGENTE"
# ==========================

# Diccionario de sinónimos de negocio (adáptalo al contexto de tu banco)
BUSINESS_SYNONYMS = {
    # Español
    "cedula": ["cedula", "dni", "documento", "num_documento", "numero_documento", "id_cliente"],
    "documento": ["dni", "documento", "num_documento"],
    "tarjeta": ["tarjeta", "card", "num_tarjeta", "pan"],
    "cuenta": ["cuenta", "num_cuenta", "numero_cuenta", "acct", "account"],
    "cliente": ["cliente", "customer", "titular", "id_cliente"],
    "telefono": ["telefono", "celular", "phone", "mobile"],
    "correo": ["email", "correo", "correo_electronico", "mail"],

    # Inglés
    "id": ["id", "identifier", "id_customer", "id_client"],
    "customer": ["customer", "client", "cliente"],
    "balance": ["balance", "saldo", "monto"],
}


STOPWORDS = {
    # Español
    "donde", "dónde", "esta", "está", "el", "la", "los", "las",
    "de", "del", "en", "que", "qué", "cual", "cuál", "para",
    "es", "se", "guarda", "almacena", "información", "info",
    # Inglés
    "where", "is", "the", "of", "in", "on", "store", "stored", "information", "data"
}


def expand_keywords(words: List[str]) -> List[str]:
    """
    Expande las palabras clave usando el diccionario de sinónimos.
    """
    expanded = set(words)
    for w in words:
        base = w.lower()
        if base in BUSINESS_SYNONYMS:
            for syn in BUSINESS_SYNONYMS[base]:
                expanded.add(syn.lower())
    return list(expanded)


def search_catalog(question: str,
                   catalog: List[Dict[str, Any]],
                   max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Busca en el catálogo las columnas más relacionadas con la pregunta.
    Utiliza:
        - Coincidencias directas por substring
        - Similaridad aproximada (difflib)
    """
    # Tokenizar pregunta muy simple
    raw_tokens = [w.strip("¿?!.:,;()").lower() for w in question.split()]
    keywords = [w for w in raw_tokens if w and w not in STOPWORDS]
    keywords = expand_keywords(keywords)

    if not keywords:
        return []

    scored = []

    for item in catalog:
        text = f"{item['database']} {item['schema']} {item['table']} {item['column']} {item['description']}".lower()
        score = 0

        for kw in keywords:
            if kw in text:
                score += 4  # Match directo
            else:
                # Similaridad aproximada
                s = difflib.SequenceMatcher(None, kw, text).ratio()
                if s > 0.6:
                    score += int(s * 3)

        if score > 0:
            scored.append((score, item))

    # Ordenar por score descendente
    scored.sort(key=lambda x: x[0], reverse=True)

    return [x[1] for x in scored[:max_results]]


# ==========================
# LOOP DE CHAT EN CONSOLA
# ==========================

def format_result(item: Dict[str, Any]) -> str:
    """
    Devuelve una línea de texto legible para un resultado.
    """
    desc = item.get("description") or ""
    if len(desc) > 60:
        desc = desc[:57] + "..."
    return (
        f"DB: {item['database']} | {item['schema']}.{item['table']} -> "
        f"{item['column']} ({item['data_type']})"
        + (f" | desc: {desc}" if desc else "")
    )


def run_chat(catalog: List[Dict[str, Any]]):
    """
    Inicia un chat simple por consola.
    """
    if not catalog:
        print("[ERROR] El catálogo está vacío. ¿Ya lo construiste?")
        return

    print("==============================================")
    print(" Asistente de estructura de BD (solo metadatos)")
    print(" Escribe 'salir' para terminar.")
    print(" Ejemplos de preguntas:")
    print("   - ¿Dónde está el número de cuenta del cliente?")
    print("   - columnas donde se guarda la cédula del cliente")
    print("==============================================")

    while True:
        try:
            q = input("\nTú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Saliendo...")
            break

        if not q:
            continue

        if q.lower() in ("salir", "exit", "quit"):
            print("[INFO] Saliendo...")
            break

        results = search_catalog(q, catalog)

        if not results:
            print("Bot: No encontré columnas relacionadas con esa descripción.")
            continue

        print("Bot: Podría estar en alguno de estos campos:")
        for r in results:
            print("  - " + format_result(r))


# ==========================
# MAIN
# ==========================

def main():
    parser = argparse.ArgumentParser(description="Asistente de metadatos SQL Server.")
    parser.add_argument(
        "--build-catalog",
        action="store_true",
        help="Reconstruye el catálogo de columnas a partir de las bases de datos configuradas."
    )
    args = parser.parse_args()

    if args.build_catalog:
        catalog = build_catalog()
        save_catalog(catalog, CATALOG_FILE)
    else:
        catalog = load_catalog(CATALOG_FILE)
        run_chat(catalog)


if __name__ == "__main__":
    main()
