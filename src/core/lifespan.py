from fastapi import FastAPI,Request,Response
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    
    logger.info('[SERVER] Application Startup Complete')
    yield
    logger.info('[SERVER] Application Shutdown Complete')