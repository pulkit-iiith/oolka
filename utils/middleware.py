from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from jose import jwt, JWTError
from utils.JWTManager import JWTManager
from fastapi.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, jwt_manager: JWTManager):
        super().__init__(app)
        self.jwt_manager = jwt_manager

    async def dispatch(self, request: Request, call_next):
        # Bypass authentication for GET /events
        if request.method == "GET" and request.url.path.startswith("/events"):
            response = await call_next(request)
            return response
        
        if request.url.path.startswith("/events") or request.url.path.startswith("/bookings"):
            try:
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    return self.error_response("Invalid token")
                    # raise HTTPException(status_code=401, detail="Authorization header missing")
                token = request.headers.get("Authorization").split(" ")[1]
                user_id = self.jwt_manager.verify_token(token)
                if user_id is None:
                    return self.error_response("Invalid token")
                request.state.user_id = user_id
            except (KeyError, IndexError, JWTError):
                return self.error_response("Invalid token")
                # raise HTTPException(status_code=401, detail="Invalid token")
        response = await call_next(request)
        return response
    def error_response(self, detail: str):
        return JSONResponse(status_code=401, content={"detail": detail})