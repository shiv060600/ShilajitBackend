from typing import final
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
LOCAL_DB_URL=os.getenv("LOCAL_DB_URL")
PROD_DB_URL=os.getenv("PROD_DB_URL")
ENV=os.getenv("ENV")

db_url = LOCAL_DB_URL if ENV == "LOCAL" else PROD_DB_URL

engine = create_engine(db_url,
    pool_size=5,                    
    max_overflow=10,                
    pool_pre_ping=True,             
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,       # 10 second timeout
        "application_name": "shilajit_tea_api"
    })

SessionLocal = sessionmaker(
    bind = engine,
    autocommit=False,
    autoflush=False
)

#auto handle sessions and session closing.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
