from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession



SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")


sync_engine = create_engine(SYNC_DATABASE_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        raise Exception("Database connection failed") from e
    finally:
        db.close()




async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker( autoflush=False,  autocommit=False, bind=async_engine, class_=AsyncSession,)

async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except SQLAlchemyError as e:
            print(f"Database connection failed>>>>>>>>>>>>>>>>: {e}")
            raise Exception("Database connection failed") from e
