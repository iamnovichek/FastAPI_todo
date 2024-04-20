from dataclasses import astuple

from fastapi import FastAPI, Depends, Query, Path, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_database
from schemas import TaskBase, TaskUpdate
from urls import UrlPatterns
from settings import origins
from models import Task
from crud import (
    create_task,
    get_all_tasks,
    get_task,
    update_task,
    delete_task,
    get_tasks_set,
    filter_tasks_by_title,
    filter_tasks_by_description,
    filter_tasks_by_status,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins)


def check_task_exists(task: Task = None, task_id: int = None):
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist",
        )


@app.get(UrlPatterns.root_url)
async def root():
    return {"all available endpoints": astuple(UrlPatterns())}


@app.get(UrlPatterns.all_tasks, description="Returns all tasks")
async def get_all_tasks_endpoint(db: Session = Depends(get_database)):
    all_tasks = get_all_tasks(db=db)

    return {"tasks": all_tasks}


@app.get(UrlPatterns.get_specific_task, description="Returns a specific task")
async def get_specific_task(
    task_id: int = Path(..., gt=0), db: Session = Depends(get_database)
):
    task = get_task(task_id=task_id, db=db)
    check_task_exists(task=task, task_id=task_id)

    return {"task": task}


@app.post(UrlPatterns.create_task, description="Creates a new task")
async def create_task_endpoint(
    task: TaskBase,
    db: Session = Depends(get_database),
):
    new_task = create_task(task=task, db=db)

    return {"task": new_task}


@app.patch(UrlPatterns.update_specific_task, description="Updates an existing task")
async def update_specific_task_endpoint(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_database),
    update_data: TaskUpdate = Body(None),
):
    task = update_task(task_id=task_id, db=db, new_data=update_data.dict())
    check_task_exists(task=task, task_id=task_id)

    return {"task": task, "message": f"Task with ID {task_id} was updated successfully"}


@app.delete(UrlPatterns.delete_specific_task, description="Deletes an existing task")
async def delete_specific_task_endpoint(
    task_id: int = Path(..., gt=0), db: Session = Depends(get_database)
):
    task = get_task(task_id=task_id, db=db)
    check_task_exists(task=task, task_id=task_id)
    delete_task(task_id=task_id, db=db)

    return {
        "message": f"Task with ID {task_id} was deleted successfully",
        "status": status.HTTP_204_NO_CONTENT,
    }


@app.get(UrlPatterns.tasks_set, description="Returns a set tasks")
async def tasks_set_endpoint(
    db: Session = Depends(get_database),
    skip: int = Query(..., ge=0),
    limit: int = Query(..., ge=0),
):
    tasks = get_tasks_set(db=db, skip=skip, limit=limit)

    return {"tasks": tasks}


@app.get(
    UrlPatterns.get_common_title_tasks,
    description="Returns a set of tasks filtered by title",
)
async def tasks_filtered_by_title_endpoint(
    db: Session = Depends(get_database), title: str = Path(..., min_length=1)
):
    tasks = filter_tasks_by_title(db=db, title=title)

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found"
        )

    return {"tasks": tasks}


@app.get(
    UrlPatterns.get_common_description_tasks,
    description="Returns a set of tasks filtered by description",
)
async def tasks_filtered_by_description_endpoint(
    db: Session = Depends(get_database), description: str = Path(..., min_length=1)
):
    tasks = filter_tasks_by_description(db=db, description=description)

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found"
        )

    return {"tasks": tasks}


@app.get(
    UrlPatterns.get_all_done_or_undone_tasks,
    description="Returns a set of tasks filtered by status",
)
async def tasks_filtered_by_status_endpoint(
    is_done: bool, db: Session = Depends(get_database)
):

    tasks = filter_tasks_by_status(db=db, status=is_done)

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found"
        )

    return {"tasks": tasks}
