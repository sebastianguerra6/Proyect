#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asistente simple de estructuras de SQL Server (solo metadatos).

Funcionalidades:
1) Construir un catálogo de columnas recorriendo varias bases de datos.
   El resultado se almacena localmente en SQLite (schema_catalog.db) para evitar JSON masivos.
2) Iniciar un "chat" en consola para buscar tablas/columnas por descripción
   usando coincidencias léxicas y heurísticas (sin depender de IA ni catálogos manuales).

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
import sqlite3
import os
import difflib
import argparse
import re
import unicodedata
from typing import List, Dict, Any

# ==========================
# CONFIGURACIÓN
# ==========================

# Nombre del servidor SQL Server (puede ser nombre o IP)
# Ejemplos:
#   "MI-SQL-SRV"
#   "MI-SQL-SRV\\INSTANCIA"
#   "10.0.0.5"
#   "localhost\\SQLEXPRESS01"
SQL_SERVER = "localhost\\SQLEXPRESS01"

# Lista de bases de datos a catalogar (usa los nombres reales)
DATABASES = [
    "GAMLO_Empleados"
    # Agrega las que necesites
]

# Archivo local donde se guarda el catálogo (SQLite para evitar JSON masivo)
CATALOG_DB_FILE = "schema_catalog.db"
BATCH_SIZE = 500
CANDIDATE_LIMIT = 400


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


def init_catalog_store(reset: bool = False) -> sqlite3.Connection:
    """
    Inicializa la base SQLite que almacena el catálogo.
    """
    conn = sqlite3.connect(CATALOG_DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            database_name TEXT NOT NULL,
            schema_name TEXT NOT NULL,
            table_name TEXT NOT NULL,
            column_name TEXT NOT NULL,
            data_type TEXT,
            max_length INTEGER,
            is_nullable INTEGER,
            description TEXT
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_catalog_table ON catalog(table_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_catalog_column ON catalog(column_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_catalog_schema ON catalog(schema_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_catalog_desc ON catalog(description)")
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS catalog_fts 
        USING fts5(
            catalog_id UNINDEXED,
            content,
            tokenize = 'unicode61 remove_diacritics 2'
        )
    """)
    if reset:
        cursor.execute("DELETE FROM catalog")
        cursor.execute("DELETE FROM catalog_fts")
    conn.commit()
    return conn


# ==========================
# UTILIDADES DE NORMALIZACIÓN
# ==========================

WORD_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")
CAMEL_SPLIT_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


def normalize_token(value: str) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return without_marks.lower()


def split_identifier(value: str) -> List[str]:
    if not value:
        return []
    replaced = value.replace("_", " ").replace("-", " ").replace("/", " ")
    camel = CAMEL_SPLIT_PATTERN.sub(" ", replaced)
    tokens = WORD_PATTERN.findall(camel)
    return tokens


def generate_word_variants(token: str) -> List[str]:
    variants = {token}
    if token.endswith("es") and len(token) > 3:
        variants.add(token[:-2])
    if token.endswith("s") and len(token) > 3:
        variants.add(token[:-1])
    else:
        variants.add(f"{token}s")
    if token.startswith("num"):
        variants.add(token.replace("num", "numero"))
    if "numero" in token:
        variants.add(token.replace("numero", "num"))
    if token.endswith("cion"):
        variants.add(token[:-3] + "ción")
    consonants = re.sub(r"[aeiouáéíóúü]", "", token)
    if len(consonants) >= 3:
        variants.add(consonants)
    if len(token) > 4:
        variants.add(token[:4])
    variants = {v for v in variants if v}
    return list(variants)


def build_acronym(text: str) -> str:
    parts = split_identifier(text)
    acronym = "".join(part[0] for part in parts if part)
    acronym = normalize_token(acronym)
    return acronym if len(acronym) >= 2 else ""


def build_search_blob(entry: Dict[str, Any]) -> str:
    texts = []
    for field in ("database", "schema", "table", "column", "data_type", "description"):
        value = entry.get(field) or ""
        if not value:
            continue
        texts.append(value)
        texts.append(value.replace("_", " "))
    tokens = []
    for text in texts:
        for token in split_identifier(text):
            normalized = normalize_token(token)
            if normalized:
                tokens.extend(generate_word_variants(normalized))
    for field in ("table", "column"):
        acronym = build_acronym(entry.get(field, "") or "")
        if acronym:
            tokens.append(acronym)
    unique_tokens = sorted(set(tokens))
    return " ".join(unique_tokens)


def sanitize_for_fts(keyword: str) -> str:
    return re.sub(r"[^0-9a-z_]", "", keyword)


# ==========================
# CONSTRUCCIÓN DEL CATÁLOGO
# ==========================

def build_catalog() -> int:
    """
    Recorre las bases de datos configuradas y almacena un catálogo de columnas
    en SQLite (evita generar un JSON gigante).
    """
    catalog_conn = init_catalog_store(reset=True)
    insert_cursor = catalog_conn.cursor()
    total = 0

    for db_name in DATABASES:
        print(f"[INFO] Catalogando base de datos: {db_name} ...")
        sql_conn = get_connection(db_name)
        sql_cursor = sql_conn.cursor()

        sql_cursor.execute("""
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

        while True:
            rows = sql_cursor.fetchmany(BATCH_SIZE)
            if not rows:
                break

            for row in rows:
                entry = {
                    "database": row.database_name,
                    "schema": row.schema_name,
                    "table": row.table_name,
                    "column": row.column_name,
                    "data_type": row.data_type,
                    "max_length": int(row.max_length) if row.max_length is not None else None,
                    "is_nullable": int(bool(row.is_nullable)),
                    "description": str(row.column_description) if row.column_description is not None else ""
                }

                insert_cursor.execute("""
                    INSERT INTO catalog (
                        database_name, schema_name, table_name, column_name,
                        data_type, max_length, is_nullable, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry["database"],
                    entry["schema"],
                    entry["table"],
                    entry["column"],
                    entry["data_type"],
                    entry["max_length"],
                    entry["is_nullable"],
                    entry["description"]
                ))

                catalog_id = insert_cursor.lastrowid
                content_blob = build_search_blob(entry) or entry["column"]
                insert_cursor.execute("""
                    INSERT INTO catalog_fts (catalog_id, content)
                    VALUES (?, ?)
                """, (catalog_id, content_blob))

                total += 1

            catalog_conn.commit()

        sql_conn.close()

    catalog_conn.close()
    print(f"[INFO] Se catalogaron {total} columnas en total.")
    return total


# ==========================
# BÚSQUEDA "INTELIGENTE"
# ==========================

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
    Expande las palabras clave usando normalización y heurísticas básicas.
    """
    expanded = set()
    for w in words:
        normalized = normalize_token(w)
        if not normalized:
            continue
        for variant in generate_word_variants(normalized):
            expanded.add(variant)
    return list(expanded)


def _collect_candidates(conn: sqlite3.Connection, keywords: List[str]) -> List[Dict[str, Any]]:
    """
    Recupera candidatos desde SQLite usando coincidencias por LIKE para cada palabra clave.
    """
    candidates: Dict[str, Dict[str, Any]] = {}
    cursor = conn.cursor()
    for kw in keywords:
        like_kw = f"%{kw}%"
        cursor.execute("""
            SELECT 
                database_name, schema_name, table_name, column_name,
                data_type, max_length, is_nullable, description
            FROM catalog
            WHERE column_name LIKE ?
               OR table_name LIKE ?
               OR description LIKE ?
               OR schema_name LIKE ?
               OR database_name LIKE ?
            LIMIT ?
        """, (like_kw, like_kw, like_kw, like_kw, like_kw, CANDIDATE_LIMIT))

        for row in cursor.fetchall():
            key = f"{row['database_name']}|{row['schema_name']}|{row['table_name']}|{row['column_name']}"
            if key not in candidates:
                candidates[key] = {
                    "database": row["database_name"],
                    "schema": row["schema_name"],
                    "table": row["table_name"],
                    "column": row["column_name"],
                    "data_type": row["data_type"],
                    "max_length": row["max_length"],
                    "is_nullable": bool(row["is_nullable"]),
                    "description": row["description"] or ""
                }
    return list(candidates.values())


def search_catalog(question: str,
                   conn: sqlite3.Connection,
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

    candidates = _collect_candidates(conn, keywords)
    if not candidates:
        return []

    scored = []

    for item in candidates:
        # Crear texto de búsqueda más completo
        text = f"{item['database']} {item['schema']} {item['table']} {item['column']} {item['description']}".lower()
        score = 0

        for kw in keywords:
            # Match directo en columna (mayor peso)
            if kw in item['column'].lower():
                score += 6
            # Match directo en nombre de tabla
            elif kw in item['table'].lower():
                score += 5
            # Match directo en texto completo
            elif kw in text:
                score += 4
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


def run_chat():
    """
    Inicia un chat simple por consola.
    """
    if not os.path.exists(CATALOG_DB_FILE):
        print(f"[ERROR] No se encontró {CATALOG_DB_FILE}. Ejecuta primero el script con --build-catalog.")
        return

    conn = sqlite3.connect(CATALOG_DB_FILE)
    conn.row_factory = sqlite3.Row

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

        results = search_catalog(q, conn)

        if not results:
            print("Bot: No encontré columnas relacionadas con esa descripción.")
            continue

        print("Bot: Podría estar en alguno de estos campos:")
        for r in results:
            print("  - " + format_result(r))

    conn.close()


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
    parser.add_argument(
        "--export-synonyms",
        action="store_true",
        help="Genera un archivo CSV editable con ejemplos de sinónimos."
    )
    args = parser.parse_args()

    if args.export_synonyms:
        export_synonyms_template()
        return

    if args.build_catalog:
        total = build_catalog()
        print(f"[INFO] Catálogo guardado en {CATALOG_DB_FILE} ({total} columnas).")
    else:
        run_chat()


if __name__ == "__main__":
    main()
