from sqlalchemy.orm import Session
from core.models import User
from core.database import Base, SessionLocal, engine


def init_db():
    Base.metadata.create_all(bind=engine)


def get_user_by_username(username: str):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user


def create_user(username: str, hashed_password: str):
    db: Session = SessionLocal()
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()
