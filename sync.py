from sqlalchemy import create_engine, text

SYNC_DATABASE_URL = "mysql+mysqlconnector://academyforumdevdbuser:YLBW7m-Z*!!!@52.1.147.59:3306/dev_academy_db"
engine = create_engine(SYNC_DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Synchronous connection successful:", result.fetchone())
except Exception as e:
    print("Synchronous connection failed:", str(e))
