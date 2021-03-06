import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Loal
from web import util
util.load_env()

engine = create_engine(
    os.environ['DATABASE_URL'],
    echo=(os.environ['FLASK_ENV'] == 'development'),
    encoding='utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
