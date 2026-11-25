from fastapi import FastAPI

from app.routes import health, tickets
from app.routes.errors import NOT_FOUND, register_error_handlers

app = FastAPI(
    title="IT Support API",
    description="API académica para clasificar y priorizar incidencias informáticas.",
    version="0.1.0",
    responses=NOT_FOUND,
)
register_error_handlers(app)
app.include_router(health.router)
app.include_router(tickets.router)
