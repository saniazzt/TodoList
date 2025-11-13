from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todolist.utils.env_loader import get_env

DATABASE_URL = get_env("DATABASE_URL", "postgresql+psycopg2://todolist:todolist@localhost:5432/todolist")

engine = create_engine(DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
