from typing import Literal

from fastapi import APIRouter

router = APIRouter(tags=["Disponibilidad"])


@router.get("/health", summary="Verificar disponibilidad")
def health() -> dict[str, Literal["ok"]]:
    return {"status": "ok"}
