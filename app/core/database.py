from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL


# Engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency (FastAPI style)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()