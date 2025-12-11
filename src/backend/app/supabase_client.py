# src/backend/app/supabase_client.py
# Reworked to use Render Postgres via DATABASE_URL (asyncpg)
import os
import asyncpg
from typing import Any, Dict, Optional, List

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set in environment")

# NOTE: this implementation opens & closes a connection per call for simplicity.
# It's fine for small apps; for production you should create a pool on startup.
# Make sure `asyncpg` is in requirements.txt.

def _parse_filters_sql(filters: Optional[str]) -> (str, List[Any]):
    """
    Support a basic supabase-style filter like: "id=eq.1" or "name=eq.foo&id=eq.2"
    Converts to SQL WHERE and parameter list.
    Currently supports only 'eq' operator.
    """
    if not filters:
        return "", []
    parts = filters.split("&")
    where_clauses = []
    params: List[Any] = []
    for part in parts:
        if "=" not in part:
            continue
        key, val = part.split("=", 1)
        # supabase format: eq.<value>
        if val.startswith("eq."):
            v = val[len("eq."):]
            where_clauses.append(f"{key} = ${len(params)+1}")
            params.append(v)
        else:
            # fallback: raw value
            where_clauses.append(f"{key} = ${len(params)+1}")
            params.append(val)
    if where_clauses:
        return " WHERE " + " AND ".join(where_clauses), params
    return "", []

async def table_select(
    table: str,
    columns: str = "*",
    filters: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
):
    """
    Select rows from Postgres table.
    - columns: comma-separated or '*' (same as previous API)
    - filters: supabase style "id=eq.1" or "name=eq.foo&id=eq.bar"
    - params: supports {'limit': int, 'order': 'col.asc' or 'col.desc'}
    Returns list[dict].
    """
    cols = columns if columns.strip() != "*" else "*"
    order_clause = ""
    limit_clause = ""

    if params:
        if "order" in params:
            # expect "col.asc" or "col.desc"
            coldir = params["order"]
            if "." in coldir:
                col, dir_ = coldir.split(".", 1)
                dir_ = dir_.upper() if dir_.lower() in ("asc", "desc") else "ASC"
                order_clause = f" ORDER BY {col} {dir_}"
        if "limit" in params:
            try:
                limit_clause = f" LIMIT {int(params['limit'])}"
            except Exception:
                pass

    where_sql, where_params = _parse_filters_sql(filters)
    sql = f"SELECT {cols} FROM {table}{where_sql}{order_clause}{limit_clause};"

    conn = await asyncpg.connect(DATABASE_URL, timeout=timeout)
    try:
        rows = await conn.fetch(sql, *where_params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def table_insert(table: str, payload: Any, returning: str = "representation"):
    """
    Insert a row or list of rows. payload: dict or list[dict]
    returning is ignored (we always return inserted rows)
    """
    if isinstance(payload, dict):
        rows = [payload]
    else:
        rows = list(payload)

    conn = await asyncpg.connect(DATABASE_URL, timeout=30.0)
    try:
        inserted = []
        async with conn.transaction():
            for row in rows:
                cols = ", ".join(row.keys())
                placeholders = ", ".join(f"${i}" for i in range(1, len(row) + 1))
                values = list(row.values())
                sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) RETURNING *;"
                rec = await conn.fetchrow(sql, *values)
                inserted.append(dict(rec))
        return inserted[0] if isinstance(payload, dict) else inserted
    finally:
        await conn.close()

async def table_update(table: str, payload: Dict[str, Any], filters: str, returning: str = "representation"):
    """
    Update rows matching filters. filters example: "id=eq.123"
    Returns updated rows (list).
    """
    set_clauses = []
    values = []
    i = 1
    for k, v in payload.items():
        set_clauses.append(f"{k} = ${i}")
        values.append(v)
        i += 1
    set_sql = ", ".join(set_clauses)
    where_sql, where_params = _parse_filters_sql(filters)
    sql = f"UPDATE {table} SET {set_sql}{where_sql} RETURNING *;"
    conn = await asyncpg.connect(DATABASE_URL, timeout=30.0)
    try:
        rows = await conn.fetch(sql, *(values + where_params))
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def table_delete(table: str, filters: str, returning: str = "representation"):
    """
    Delete rows matching filters.
    """
    where_sql, where_params = _parse_filters_sql(filters)
    sql = f"DELETE FROM {table}{where_sql} RETURNING *;"
    conn = await asyncpg.connect(DATABASE_URL, timeout=30.0)
    try:
        rows = await conn.fetch(sql, *where_params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def get_row_by_pk(table: str, pk_name: str, pk_value: Any, columns: str = "*"):
    filters = f"{pk_name}=eq.{pk_value}"
    data = await table_select(table, columns=columns, filters=filters)
    return data[0] if data else None
