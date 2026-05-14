from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: str
    priority: str

class TaskResponse(TaskCreate):
    id: int
    status: str

    class Config:
        from_attributes = True