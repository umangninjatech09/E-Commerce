from fastapi.responses import JSONResponse

def error_response(status_code: int, message: str, details: dict = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "code": status_code,
            "message": message,
            "details": details,
        },
    )
