##### factory.py










from fastapi import FastAPI, HTTPException
from api.endpoints.v1 import router as v1_router
from exception_handlers import (
    jwt_expired_handler,
    jwt_invalid_token_handler,
    global_exception_handler,
    not_authenticated_handler,
)
import jwt


def create_app(settings) -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    # Include routers
    print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    app.include_router(v1_router, prefix="/api")

    # Exception handlers
    app.add_exception_handler(jwt.ExpiredSignatureError, jwt_expired_handler)
    app.add_exception_handler(jwt.InvalidTokenError, jwt_invalid_token_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(HTTPException, not_authenticated_handler)

    return app
