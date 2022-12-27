from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///app.db")

def get_db():
    return Session(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    session_key = Column(String)


Base.metadata.create_all(bind=engine)


def create_todo(db: Session, content: str, session_key: str):
    todo = ToDo(content=content, session_key=session_key)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo(db: Session, item_id: int):
    return db.query(ToDo).filter(ToDo.id == item_id).first()


def update_todo(db: Session, item_id: int, content: str):
    todo = get_todo(db, item_id)
    todo.content = content  # type: ignore
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, session_key: str, skip: int = 0, limit: int = 100):
    return (
        db.query(ToDo)
        .filter(ToDo.session_key == session_key)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_todo(db: Session, item_id: int):
    todo = get_todo(db, item_id)
    db.delete(todo)
    db.commit()
