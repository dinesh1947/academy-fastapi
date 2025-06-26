# exception_handlers.py
import traceback
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException




from fastapi.exceptions import RequestValidationError
import traceback



import jwt
from jose import JWTError, ExpiredSignatureError  # PyJWT compatibility

# ✅ Handle Expired JWT Token
async def jwt_expired_handler(request: Request, exc: jwt.ExpiredSignatureError):
    """Handles expired JWT tokens."""
    print(f"JWT Expired Error: {exc}")
    return JSONResponse(
        status_code=401,  # Unauthorized
        content={"message": "Token has expired. Please log in again.", "flag": 0}
    )

# ✅ Handle Invalid JWT Token
async def jwt_invalid_token_handler(request: Request, exc: jwt.InvalidTokenError):
    """Handles invalid JWT tokens."""
    print(f"JWT Invalid Token Error: {exc}")
    return JSONResponse(
        status_code=403,  # Forbidden
        content={"message": "Invalid token. Access denied.", "flag": 0}
    )

# ✅ Handle General Exceptions
async def global_exception_handler(request: Request, exc: Exception):
    """Handles unexpected errors globally."""
    print(f"Unhandled error: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error. Please try again later.", "flag": 0}
    )


# ✅ Handle Not Authenticated (HTTP 401)
async def not_authenticated_handler(request: Request, exc: HTTPException):
    """Handles not authenticated errors."""
    print(f"Not Authenticated Error: {exc}")
    return JSONResponse(
        status_code=401,  # Unauthorized
        content={"message": "Not authenticated. Please log in.", "flag": 0}
    )

async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"flag":0,"detail": "No page exists for the requested API endpoint.", "data":{}}
        )
    # For other HTTP exceptions, you can fallback to default handler or re-raise
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )






async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    # print("Validation Error:", exc)
    # traceback.print_exc()

    return JSONResponse(
        status_code=400,
        content={"message": "Invalid or missing request body.", "flag": 0}
    )
