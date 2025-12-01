# src/backend/app/supabase_client.py
import os
import httpx
from typing import Any, Dict, Optional

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment")

DEFAULT_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Accept": "application/json",
}

async def table_select(
    table: str,
    columns: str = "*",
    filters: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
):
    """
    GET REST select from Supabase table.
    - table: table name
    - columns: columns string (e.g. "id,name") or "*" for all
    - filters: raw filter string appended to URL, e.g. "id=eq.1"
    - params: query params dict (limit, order, etc)
    Returns parsed JSON (list).
    """
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table}?select={columns}"
    if filters:
        url = f"{url}&{filters}"
    async with httpx.AsyncClient(timeout=timeout, headers=DEFAULT_HEADERS) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

async def table_insert(table: str, payload: Any, returning: str = "representation"):
    """
    Insert a row or list of rows.
    - payload: dict or list[dict]
    - returning: 'representation' to return inserted rows
    Returns first inserted item if single dict provided, otherwise list.
    """
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table}"
    headers = DEFAULT_HEADERS.copy()
    headers["Prefer"] = f"return={returning}"
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        return r.json()

async def table_update(table: str, payload: Dict[str, Any], filters: str, returning: str = "representation"):
    """
    Update rows matching filters. filters example: "id=eq.123"
    Returns updated rows (list).
    """
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table}?{filters}"
    headers = DEFAULT_HEADERS.copy()
    headers["Prefer"] = f"return={returning}"
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        r = await client.patch(url, json=payload)
        r.raise_for_status()
        return r.json()

async def table_delete(table: str, filters: str, returning: str = "representation"):
    """
    Delete rows matching filters.
    """
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{table}?{filters}"
    headers = DEFAULT_HEADERS.copy()
    headers["Prefer"] = f"return={returning}"
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        r = await client.delete(url)
        r.raise_for_status()
        return r.json()

async def get_row_by_pk(table: str, pk_name: str, pk_value: Any, columns: str = "*"):
    filters = f"{pk_name}=eq.{pk_value}"
    data = await table_select(table, columns=columns, filters=filters)
    return data[0] if data else None
