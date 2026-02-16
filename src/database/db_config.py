from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from src.database.models import Base
from src.core.config import ENV

DB_URL = os.getenv('DB_URL')
db_engine = create_engine(url=DB_URL)
db_session = sessionmaker(autoflush=False, bind=db_engine)

def init_db():
    Base.metadata.create_all(bind=db_engine)
