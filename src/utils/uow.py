from typing import Type
from abc import ABC, abstractmethod
from db.db import get_async_session
from repositories.task_history import TaskHistoryRepository
from repositories.tasks import TasksRepository


class InerfaceUnitofWork(ABC):

    tasks: Type[TasksRepository]
    task_history: Type[TaskHistoryRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitofWork:

    def __init__(self):
        self.session_factory = get_async_session

    async def __aenter__(self):
        self.session = await self.session_factory().__anext__()
        # self.session = self.session_factory()

        self.tasks = TasksRepository(self.session)
        self.task_history = TaskHistoryRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        """Завершение транзакции"""
        await self.session.rollback()
