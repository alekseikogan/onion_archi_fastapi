from schemas.tasks import TaskSchemaAdd
from utils.repository import AbstractRepository


class TasksService:
    def __init__(self, tasks_repo: AbstractRepository):
        self.tasks_repo: AbstractRepository = tasks_repo()

    async def add_task(self, task: TaskSchemaAdd):
        tasks_dict = task.model_dump()
        task_id = await self.tasks_repo.add_one(tasks_dict)
        return task_id
