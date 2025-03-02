from fastapi.responses import JSONResponse
from fastapi import HTTPException
from dtos.ResponseDto import ResponseDto

def custom_error(exception: Exception):
    if isinstance(exception, ValueError):
        status_code = 400
        message = str(exception)
    elif isinstance(exception, HTTPException):
        status_code = exception.status_code
        message = exception.detail
    else:
        status_code = 500
        message = "Internal Server Error"

    error_response = ResponseDto(
        message=message,
        status="false",
        statusCode=status_code,
        data=None
    )

    return JSONResponse(
        content=error_response.model_dump(),
        status_code=status_code
    )
