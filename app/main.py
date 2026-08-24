"""FastAPI application exposing a user-details API backed by Supabase."""

import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import get_supabase
from app.models import UserCreate, UserRead

logger = logging.getLogger("uvicorn.error")

settings = get_settings()

app = FastAPI(
    title="Synnovatify User API",
    description="Collects user details and stores them in Supabase.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def root() -> dict:
    """Simple liveness/info endpoint."""
    return {"service": "Synnovatify User API", "status": "ok"}


@app.get("/health", tags=["health"])
def health() -> dict:
    """Health check used by Render."""
    return {"status": "healthy"}


@app.post(
    "/api/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(payload: UserCreate) -> UserRead:
    """Validate incoming user details and persist them to Supabase."""
    supabase = get_supabase()
    record = {
        "name": payload.name,
        "email": str(payload.email),
        "phone": payload.phone,
        "message": payload.message,
    }

    try:
        result = supabase.table(settings.supabase_table).insert(record).execute()
    except Exception as exc:  # noqa: BLE001 - surface a clean 502 to the caller
        logger.exception("Supabase insert failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to save user to the database.",
        ) from exc

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Database returned no record after insert.",
        )

    return UserRead(**result.data[0])


@app.get("/api/users", response_model=list[UserRead], tags=["users"])
def list_users(limit: int = 50) -> list[UserRead]:
    """Return the most recent users (newest first)."""
    limit = max(1, min(limit, 200))
    supabase = get_supabase()

    try:
        result = (
            supabase.table(settings.supabase_table)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Supabase query failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to read users from the database.",
        ) from exc

    return [UserRead(**row) for row in (result.data or [])]
