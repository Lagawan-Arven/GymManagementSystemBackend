from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from src.router import SystemRouter,AuthRouter,AdminRouter,MemberRouter,SessionRouter,PaymentRouter,LogsRouter

from src.core.config import setup_logging,limiter
from src.core.lifespan import lifespan
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Gym Management API",lifespan=lifespan)
app.state.limiter = limiter

origins = ["http://localhost:5173","http://127.0.0.1:5173"]

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

app.include_router(SystemRouter,tags=['System'])
app.include_router(AuthRouter,prefix='/auth',tags=["Authentication"])
app.include_router(AdminRouter,tags=["Admin Router"])
app.include_router(MemberRouter,tags=["Member Router"])
app.include_router(SessionRouter,tags=["Session Router"])
app.include_router(PaymentRouter,tags=["Payment Router"])
app.include_router(LogsRouter,tags=["Logs Router"])
                   