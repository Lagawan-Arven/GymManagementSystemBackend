from slowapi import Limiter
from slowapi.util import get_remote_address
from pathlib import Path
from dotenv import load_dotenv
import logging,sys,os

#=================================
        #LIMITER CONFIG
#=================================
limiter = Limiter(key_func=get_remote_address)

#=================================
        #LOGGING CONFIG
#=================================
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def setup_logging():
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)], format=LOG_FORMAT)

#=================================
        #ENVIRONMENT CONFIG
#=================================
load_dotenv()

ENV = os.getenv('ENVIRONMENT','local')
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env_file_map = {
    "local":".env.local",
    "docker":".env.docker"
}

env_file = env_file_map.get(ENV)

if env_file:
    env_path = BASE_DIR / env_file
    if env_path.exists():
        load_dotenv(env_path)

