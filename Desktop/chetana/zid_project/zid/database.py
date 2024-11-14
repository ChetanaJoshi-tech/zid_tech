# # app/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Set the database URL (using SQLite for simplicity, you can change to PostgreSQL or another)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Change this URL if you're using a different DB

# # Create the database engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# # Session local for interacting with the database
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for models
# Base = declarative_base()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (update with your database URI)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sales.db"  # Using SQLite here for local development

# Create engine, with check_same_thread=False for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models to inherit from
Base = declarative_base()


