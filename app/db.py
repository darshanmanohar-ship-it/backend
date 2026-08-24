"""Supabase client factory."""

from functools import lru_cache

from supabase import Client, create_client

from app.config import get_settings


@lru_cache
def get_supabase() -> Client:
    """Return a cached Supabase client.

    Uses the service_role key so the API can write rows regardless of the
    table's row-level-security policies. This client must only ever run on the
    server (never shipped to a browser).
    """
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)
