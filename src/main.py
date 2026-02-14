from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from router.auth_router import router as auth_router

from src.core.config import setup_logging,limiter
from src.core.lifespan import lifespan
from src.core.exceptions import add_exception_handlers
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Gym Management API",lifespan=lifespan)
app.state.limiter = limiter
add_exception_handlers(app)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

@app.get('/',tags=['Health Check'])
@limiter.limit('10/minute')
def health_check(request: Request):
    logger.info('Application status ok')
    return {"status":"ok"}

app.include_router(auth_router,tags=["Authentication"])