from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Замени на свою строку подключения
# PostgreSQL: "postgresql://user:password@localhost/savi_db"
# SQLite (для теста): "sqlite:///./savi.db"
DATABASE_URL = "sqlite:///./savi.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # только для SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
