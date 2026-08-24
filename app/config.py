"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings.

    Values are read from environment variables (or a local .env file during
    development). On Render these are set in the service's Environment tab.
    """

    # Supabase project URL, e.g. https://xxxxxxxx.supabase.co
    supabase_url: str

    # Supabase service_role key. Kept server-side only, never exposed to clients.
    supabase_service_key: str

    # Name of the table user records are written to.
    supabase_table: str = "users"

    # Comma-separated list of origins allowed to call the API via a browser.
    # Example: "https://synnovatify.com,https://www.synnovatify.com"
    cors_allow_origins: str = "https://synnovatify.com,https://www.synnovatify.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor so the .env is parsed only once."""
    return Settings()
