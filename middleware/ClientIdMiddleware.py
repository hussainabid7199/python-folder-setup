import os
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ClientIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.client_id = os.getenv('CLIENT_ID')

    async def dispatch(self, request: Request, call_next):
        header_client_id = request.headers.get("client-id")
        if not self.client_id or header_client_id != self.client_id:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid or missing client ID"}
            )
        response = await call_next(request)
        return response