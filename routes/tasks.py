from fastapi import APIRouter, Depends, HTTPException
from tasks.jobs import notify_task_created
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token
from pydantic import BaseModel
from typing import Optional
from database import get_session
from models import Task, User

router = APIRouter(prefix="/tasks", tags=["tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_token(token)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


class TaskRequest(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


@router.post("/")
def create_task(
    body: TaskRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    task = Task(title=body.title, description=body.description, owner_id=user_id)
    session.add(task)
    user = session.get(User, user_id)
    session.commit()
    session.refresh(task)
    notify_task_created.delay(task.id, task.title, user.email)  # type: ignore
    return task


@router.get("/")
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    tasks = session.exec(
        select(Task).where(Task.owner_id == user_id).offset(skip).limit(limit)
    ).all()
    return tasks


@router.patch("/{task_id}")
def update_task(
    task_id: int,
    body: TaskUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    if body.title is not None:
        task.title = body.title
    if body.description is not None:
        task.description = body.description
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/{task_id}/complete")
def complete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"deleted": task_id}
