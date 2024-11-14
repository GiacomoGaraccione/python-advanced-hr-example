from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///hr.db'

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()