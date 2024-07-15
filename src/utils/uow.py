from typing import Type

from db.db import get_async_session
from repositories.task_history import TaskHistoryRepository
from repositories.tasks import TasksRepository


class InerfaceUnitofWork:

    tasks: Type[TasksRepository]
    task_history: Type[TaskHistoryRepository]

    def __init__(self):
        pass

    async def __aenter__(self):
        pass

    async def __aexit(self, *args):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass


class UnitofWork:

    def __init__(self):
        self.session_factory = get_async_session

    async def __aenter__(self):
        self.session = self.session_factory()
        self.tasks = TasksRepository(self.session)
        self.task_history = TaskHistoryRepository(self.session)

    async def __aexit(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        """Завершение транзакции"""
        await self.session.rollback()
