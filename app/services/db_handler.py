from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.master import MasterDatabase, Base
import hashlib

DATABASE_URL = "sqlite:///./database/master.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def create_organization(payload):
    session = SessionLocal()
    try:
        # Example logic for dynamic DB creation
        dynamic_db_url = f"sqlite:///./{payload.organization_name}.db"
        hashed_password = hashlib.sha256(payload.password.encode()).hexdigest()

        session.add(MasterDatabase(
            organization_name=payload.organization_name,
            admin_email=payload.email,
            dynamic_db_url=dynamic_db_url
        ))
        session.commit()
        return True
    except Exception as e:
        print(e)
        session.rollback()
        return False
    finally:
        session.close()

def get_organization_by_name(org_name):
    session = SessionLocal()
    org = session.query(MasterDatabase).filter_by(organization_name=org_name).first()
    session.close()
    return org
