from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Level = Literal["low", "medium", "high"]
PriorityCode = Literal["low", "medium", "high", "critical"]
CategoryCode = Literal[
    "security", "access", "network", "business_systems", "hardware", "software", "other"
]


class TicketRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "description": "La impresora de mi puesto no imprime.",
                    "impact": "low",
                    "urgency": "low",
                }
            ]
        },
    )

    description: Annotated[
        str, StringConstraints(strict=True, strip_whitespace=True, min_length=5, max_length=2000)
    ] = Field(description="Síntomas de la incidencia. La longitud se valida tras recortar espacios.")
    impact: Level = Field(description="Alcance de la incidencia según el catálogo.")
    urgency: Level = Field(description="Necesidad de atención según el catálogo.")


class Category(BaseModel):
    code: CategoryCode
    label: str


class CategoryDefinition(Category):
    description: str


class LevelDefinition(BaseModel):
    code: Level
    label: str
    description: str


class Priority(BaseModel):
    code: PriorityCode
    label: str


class PriorityDefinition(Priority):
    description: str


class MatrixEntry(BaseModel):
    impact: Level
    urgency: Level
    priority: PriorityCode


class SecurityException(BaseModel):
    category: CategoryCode
    minimum_priority: PriorityCode


class PriorityCatalog(BaseModel):
    impact_levels: list[LevelDefinition]
    urgency_levels: list[LevelDefinition]
    priority_levels: list[PriorityDefinition]
    matrix: list[MatrixEntry]
    security_exception: SecurityException


class TicketAnalysis(BaseModel):
    category: Category
    priority: Priority
    reason: str
    recommendations: list[str]
