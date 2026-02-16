from fastapi import FastAPI,Request,Response
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from src.core.config import ENV
from src.database.db_config import init_db

import logging,os

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    #===============================
        #INITIALIZE DATABASE
    #===============================
    if os.getenv("TESTING") == "1":
        logger.info("Running in TESTING mode")
    elif os.getenv("ENVIRONMENT") == "local" or "docker":
        init_db()

    logger.info('[SERVER] Application Startup Complete')
    yield
    logger.info('[SERVER] Application Shutdown Complete')