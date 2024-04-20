from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = ""
    is_done: bool | None = False

    class Config:
        orm_mode = True


class TaskUpdate(TaskBase):
    title: str | None = None

    class Config:
        orm_mode = True
