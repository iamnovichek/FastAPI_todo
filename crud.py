from sqlalchemy.orm import Session

from schemas import TaskBase
from models import Task
from database import proceed_changes


def get_task(db: Session, task_id: int) -> Task:
    return db.query(Task).get(task_id)


def get_tasks_by_title(db: Session, title: str) -> list[Task]:
    return db.query(Task).filter(Task.title == title)


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_tasks_set(db: Session, skip: int = None, limit: int = None) -> list[Task]:
    return db.query(Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskBase) -> Task:
    new_task = Task(
        title=task.title, description=task.description, is_done=task.is_done
    )
    proceed_changes(db, new_task)

    return new_task


def update_task(db: Session, task_id: int, new_data: dict) -> Task:
    if task := db.query(Task).get(task_id):
        [
            new_data.setdefault(key, getattr(task, key))
            for key in new_data
            if new_data[key]
        ]
        db.query(Task).filter(Task.id == task_id).update(values=new_data)

        proceed_changes(db=db, obj=task)

        return task

    return


def delete_task(db: Session, task_id: int) -> None:
    if db.query(Task).get(task_id):
        db.query(Task).filter(Task.id == task_id).delete()
        db.commit()

    return


def filter_tasks_by_title(db: Session, title: str) -> list[Task]:
    return db.query(Task).filter(Task.title.like(f"%{title}%")).all()


def filter_tasks_by_description(db: Session, description: str) -> list[Task]:
    return db.query(Task).filter(Task.description.like(f"%{description}%")).all()


def filter_tasks_by_status(db: Session, status: bool) -> list[Task]:
    return db.query(Task).filter(Task.is_done == status).all()
