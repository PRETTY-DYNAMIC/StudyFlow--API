from fastapi import FastAPI, HTTPException
from app.database import SessionLocal, engine
from app.models import Base, Task
from app.schemas import TaskCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

# HOME ROUTE
@app.get("/")
def home():
    return {"message": "Welcome to StudyFlow API"}

# CREATE TASK
@app.post("/tasks")
def create_task(task: TaskCreate):
    db = SessionLocal()

    new_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# GET ALL TASKS
@app.get("/tasks/{task_id}")
def get_tasks():
    db = SessionLocal()

    tasks = db.query(Task).all()

    return tasks

# GET ONE TASK
@app.get("/tasks/{task_id}")
def get_tasks(task_id: int):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404, detail="Task nott found"
        )
    return task

# UPDATE TASK STATUS
@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    db = SessionLocal()
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    task.status = "completed"

    db.commit()
    db.refresh(task)

    return task

# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

# FILTER TASKS BY STATUS
@app.get("/tasks/status/{status}")
def get_tasks_by_status(status: str):
    db = SessionLocal()

    tasks = db.query(Task).filter(
        Task.status == status
    ).all()

    return tasks