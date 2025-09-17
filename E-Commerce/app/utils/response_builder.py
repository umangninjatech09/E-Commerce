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
<<<<<<< HEAD
    )
=======
    )
>>>>>>> 91a3d0d74daa07f71f175cdfc49d5698377b8950
