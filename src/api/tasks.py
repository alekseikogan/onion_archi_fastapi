from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import tasks_service
from db.db import get_async_session
from models.tasks import Tasks
from repositories.tasks import TasksRepository
from schemas.tasks import TaskSchemaAdd
from services.tasks import TasksService

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get('')
async def get_tasks(session: Annotated[AsyncSession, Depends(get_async_session)]):
    """Получение всех задач из БД."""
    stmt = select(Tasks)
    res = await session.execute(stmt)
    res = [row[0].to_read_model() for row in res.all()]
    return res


@router.post('')
async def add_task(
    task: TaskSchemaAdd,
    tasks_service: Annotated[TasksService, Depends(tasks_service)]):
    """Добавление задачи в базу данных."""
    task_id = await tasks_service.add_task(task)
    return {'task_id': task_id}
