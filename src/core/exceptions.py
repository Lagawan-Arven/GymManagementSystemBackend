from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

class NotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name

class PasswordIncorrectError(Exception):
    def __init__(self):
        pass

class UserUnauthorizeddError(Exception):
    def __init__(self, name: str):
        self.name = name

def add_exception_handlers(app: FastAPI):

    @app.exception_handler(RateLimitExceeded)
    def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"message":"Too many request"})
    
    @app.exception_handler(NotFoundError)
    def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={f"message":"{exc.name} not found"})
    
    @app.exception_handler(PasswordIncorrectError)
    def password_incorrect_handler(request: Request, exc: PasswordIncorrectError):
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"message":"Incorrect password"})