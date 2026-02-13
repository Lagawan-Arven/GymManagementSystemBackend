from fastapi import FastAPI,Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from src.router.auth import router as auth_router

from src.core.config import limiter

app = FastAPI(title="Gym Management API")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

'''app.state.limiter = limiter

@app.exception_handlers(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"message":"Too many request"})'''

app.include_router(auth_router)