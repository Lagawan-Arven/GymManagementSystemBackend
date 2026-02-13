from slowapi import Limiter
from slowapi.util import get_remote_address
import logging,sys

#LIMITER CONFIG 
limiter = Limiter(key_func=get_remote_address)

#LOGGING CONFIG 
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def setup_logging():
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)], format=LOG_FORMAT)
