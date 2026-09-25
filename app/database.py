import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

from app.models import Base

load_dotenv()


database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)


engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()


def create_tables():
    Base.metadata.create_all(engine)