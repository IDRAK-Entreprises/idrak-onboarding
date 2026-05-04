from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#this is how SQLAlchemy will know where our database is located at
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/idrak_db"

#so this is basically how we connect to the database
engine = create_engine(DATABASE_URL)

#this is self explanatory, it creates a session for us whenever we connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#all our models with inherit from this class
Base = declarative_base()


#yield is cool in this context because it basically pauses the code, allows the endpoints
#to do what they need to do with the database and then when its finished its close 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()