from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.master import MasterDatabase, Base
from app.utils.auth_utils import get_salt, get_hashed_password


DATABASE_URL = "sqlite:///./database/master.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def create_organization(payload):
    with Session() as session:
        try:
            dynamic_db_url = f"sqlite:///./database/{payload.organization_name}.db"
            salt = get_salt()
            hashed_password = get_hashed_password(payload.password, salt)

            org_db_engine = create_engine(dynamic_db_url)
            with org_db_engine.connect() as connection:
                # Create the organization tables here
                pass
            session.add(MasterDatabase(
                organization_name=payload.organization_name,
                admin_email=payload.email,
                dynamic_db_url=dynamic_db_url,
                salt=salt,
                hashed_password=hashed_password,
            ))
            session.commit()
            return True
        except Exception as e:
            print(e)
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
