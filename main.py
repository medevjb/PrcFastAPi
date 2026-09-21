from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional

app = FastAPI()

DATABASE_URL = "sqlite:///./testalchemy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# SQLAlchemy database model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


# Pydantic request model
class Todo(BaseModel):
    title: str
    description: Optional[str] = None


# Pydantic response model
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    model_config = {
        "from_attributes": True
    }


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/todos/", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos

@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: Todo, db: Session = Depends(get_db)):

    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=False
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return {"error": "Todo not found"}

    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not existing_todo:
        return {"error": "Todo not found"}

    existing_todo.title = todo.title
    existing_todo.description = todo.description
    db.commit()
    db.refresh(existing_todo)

    return existing_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not existing_todo:
        return {"error": "Todo not found"}

    db.delete(existing_todo)
    db.commit()

    return {"message": "Todo deleted successfully"} 