import os
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query

from app.adapters import get_adapter

router = APIRouter()


@router.get("/debug/search")
def debug_search(
    q: str = Query(min_length=1), lang: Literal["en", "es"] = "en"
) -> dict:
    # Dev-only: hidden unless APP_ENV=dev (unset counts as dev; deploys set APP_ENV=prod).
    if os.getenv("APP_ENV", "dev") != "dev":
        raise HTTPException(status_code=404)
    results = get_adapter("search").search(q, lang)
    return {"request_id": str(uuid4()), "results": results}
