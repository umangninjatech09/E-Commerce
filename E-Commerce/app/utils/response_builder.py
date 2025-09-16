from fastapi.responses import JSONResponse

def error_response(status_code: int, error: str, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "code": status_code,
            "error": error,
            "message": message,
        },
    )