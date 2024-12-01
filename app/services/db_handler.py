import os
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from app.models.master import MasterDatabase, Base
from app.utils.auth_utils import get_salt, get_hashed_password


logger = logging.getLogger("org_manager")
DATABASE_DIR = os.getenv("DATABASE_DIR", "./database")
DATABASE_URL = f"sqlite:///{DATABASE_DIR}/master.db"
os.makedirs(DATABASE_DIR, exist_ok=True)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def reset_db():
    """
    Helper function used to reset db for testing purpose.
    """
    global DATABASE_DIR, DATABASE_URL, engine, Session
    DATABASE_DIR = os.getenv("DATABASE_DIR", "./database")
    DATABASE_URL = f"sqlite:///{DATABASE_DIR}/master.db"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

def create_organization(payload):
    with Session() as session:
        try:
            dynamic_db_url = f"sqlite:///{DATABASE_DIR}/{payload.organization_name}.db"
            salt = get_salt()
            hashed_password = get_hashed_password(payload.password, salt)

            org_db_engine = create_engine(dynamic_db_url)
            with org_db_engine.connect() as connection:
                # NOTE: If any boiler plate tables like user have to be create
                # for the org then, it can be created here
                pass
            new_org = MasterDatabase(
                organization_name=payload.organization_name,
                admin_email=payload.email,
                dynamic_db_url=dynamic_db_url,
                salt=salt,
                hashed_password=hashed_password,
            )
            session.add(new_org)
            session.commit()
            return new_org.id
        except SQLAlchemyError as e:
            logger.warning(repr(e))
            session.rollback()
            return False

def get_organization_by_name(org_name):
    with Session() as session:
        org = session.query(MasterDatabase).filter_by(organization_name=org_name).first()
        return org

def get_organization_by_email(email):
    with Session() as session:
        org = session.query(MasterDatabase).filter_by(admin_email=email).first()
        return org
