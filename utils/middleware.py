from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from jose import jwt, JWTError
from utils.JWTManager import JWTManager

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, jwt_manager: JWTManager):
        super().__init__(app)
        self.jwt_manager = jwt_manager

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/events") or request.url.path.startswith("/bookings"):
            try:
                token = request.headers.get("Authorization").split(" ")[1]
                user_id = self.jwt_manager.verify_token(token)
                if user_id is None:
                    raise HTTPException(status_code=401, detail="Invalid token")
                request.state.user_id = user_id
            except (KeyError, IndexError, JWTError):
                raise HTTPException(status_code=401, detail="Invalid token")
        response = await call_next(request)
        return response
