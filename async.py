import asyncio
from databases import Database

ASYNC_DATABASE_URL = "mysql+aiomysql://academyforumdevdbuser:YLBW7m-Z*!!!@52.1.147.59:3306/dev_academy_db"
database = Database(ASYNC_DATABASE_URL)

async def test_async_connection():
    try:
        await database.connect()
        result = await database.fetch_one("SELECT 1")
        print("Asynchronous connection successful:", result)
    except Exception as e:
        print("Asynchronous connection failed:", str(e))
    finally:
        await database.disconnect()

asyncio.run(test_async_connection())
