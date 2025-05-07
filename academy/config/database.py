# database.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from urllib.parse import quote
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Database configuration
DB_NAME = "dev_academy_db"
DB_USER = "academyforumdevdbuser"
PASSWORD = quote("YLBW7m-Z*!!!")  # Escaping special characters
HOST = "52.1.147.59"
PORT = 3306


# ASYNC_DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
# async_database = Database(ASYNC_DATABASE_URL)




SYNC_DATABASE_URL = "mysql+mysqlconnector://academyforumdevdbuser:YLBW7m-Z*!!!@52.1.147.59:3306/dev_academy_db"
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)





def get_sync_db():
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    db = SyncSessionLocal()
    try:
        # Test the database connection by performing a simple query
        db.execute(text("SELECT 1"))  # Wrap the SQL query in `text()`
        print("Database connection successfulZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZzz")
        yield db
    except SQLAlchemyError as e:
        print(f"Database connection failed>>>>>>>>>>>>>>>>: {e}")
        raise Exception("Database connection failed") from e
    finally:
        db.close()





ASYNC_DATABASE_URL = "mysql+asyncmy://academyforumdevdbuser:YLBW7m-Z*!!!@52.1.147.59:3306/dev_academy_db"

# Create an async engine
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Async sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)



async def get_async_db():
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    async with AsyncSessionLocal() as db:
        try:
            # Test the database connection by performing a simple query
            await db.execute(text("SELECT 1"))  # Use `await` for async execution
            print("Database connection successful async")
            yield db
        except SQLAlchemyError as e:
            print(f"Database connection failed>>>>>>>>>>>>>>>>: {e}")
            raise Exception("Database connection failed") from e
