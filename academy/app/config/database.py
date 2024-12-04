from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from urllib.parse import quote

# Database configuration
DB_NAME = "dev_academy_db"
DB_USER = "academyforumdevdbuser"
PASSWORD = quote("YLBW7m-Z*!!!")  # Escaping special characters
HOST = "52.1.147.59"
PORT = 3306

# Database URLs
SYNC_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Synchronous setup
sync_engine = create_engine(SYNC_DATABASE_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Asynchronous setup
async_database = Database(ASYNC_DATABASE_URL)

# Base class for models
Base = declarative_base()

# Dependency for synchronous database session
def get_sync_db():
    """
    Dependency that provides a synchronous database session.
    It ensures proper cleanup after use.
    """
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
