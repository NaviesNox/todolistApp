from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .db import get_session
from .models import Task
from .schemas import TaskCreate, TaskRead, TaskUpdate


app = FastAPI(title="Todo List API")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def get_allowed_origins() -> List[str]:
    raw = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    return [o.strip() for o in raw.split(",") if o.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).order_by(Task.deadline.asc())).all()
    return tasks


@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    task = Task(
        description=payload.description.strip(),
        deadline=payload.deadline,
        created_at=now_utc(),
        updated_at=now_utc(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.description = payload.description.strip()
    task.deadline = payload.deadline
    task.updated_at = now_utc()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return Response(status_code=204)

