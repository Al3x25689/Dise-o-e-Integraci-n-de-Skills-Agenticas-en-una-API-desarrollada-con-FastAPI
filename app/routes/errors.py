from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException


class ErrorItem(BaseModel):
    type: str
    loc: list[str | int]
    msg: str


class ErrorResponse(BaseModel):
    detail: list[ErrorItem]


NOT_FOUND = {404: {"model": ErrorResponse, "description": "La ruta solicitada no existe."}}
ANALYSIS_ERRORS = {
    400: {"model": ErrorResponse, "description": "El cuerpo no contiene JSON válido en UTF-8."},
    422: {"model": ErrorResponse, "description": "El JSON es válido, pero no cumple el contrato."},
}


def error_response(status: int, *items: ErrorItem, headers=None) -> JSONResponse:
    body = ErrorResponse(detail=list(items))
    return JSONResponse(
        content=body.model_dump(mode="json"), status_code=status, headers=headers,
    )


async def handle_http_error(request: Request, exc: HTTPException):
    if exc.status_code == 400:
        item = ErrorItem(type="invalid_json", loc=["body"], msg="Envía un cuerpo JSON válido en UTF-8.")
    elif exc.status_code == 404:
        item = ErrorItem(type="not_found", loc=["path"], msg="La ruta solicitada no existe.")
    else:
        return await http_exception_handler(request, exc)
    return error_response(exc.status_code, item, headers=exc.headers)


async def handle_validation_error(_request: Request, exc: RequestValidationError):
    errors = exc.errors()
    for error in errors:
        if error["type"] == "json_invalid":
            return error_response(
                400, ErrorItem(type="invalid_json", loc=list(error["loc"]), msg="El JSON está mal formado."),
            )
    return error_response(
        422,
        *(ErrorItem(type=error["type"], loc=list(error["loc"]), msg=error["msg"]) for error in errors),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, handle_http_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
