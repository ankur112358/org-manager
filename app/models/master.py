from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MasterDatabase(Base):
    __tablename__ = "master_database"
    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String, unique=True, index=True)
    admin_email = Column(String, unique=True)
    dynamic_db_url = Column(String)
    salt = Column(String)
    hashed_password = Column(String)
