from typing import Annotated

from fastapi import Depends

from repositories.tasks import TasksRepository
from services.tasks import TasksService
from utils.uow import InerfaceUnitofWork, UnitofWork

# def tasks_service():
#     return TasksService(TasksRepository)

UOWDep = Annotated[InerfaceUnitofWork, Depends(UnitofWork)]
