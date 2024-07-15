from schemas.tasks import TaskHistorySchemaAdd, TaskSchemaAdd, TaskSchemaEdit
from utils.uow import InerfaceUnitofWork


class TasksService:

    async def add_task(self, task: TaskSchemaAdd):
        tasks_dict = task.model_dump()
        task_id = await self.tasks_repo.add_one(tasks_dict)
        return task_id

    async def get_tasks(self):
        tasks = await self.task_repo.find_all()
        return tasks

    async def edit_task(self, uow: InerfaceUnitofWork, task_id: int, task: TaskSchemaEdit):
        task_dict = task.model_dump()

        async with uow:
            await uow.tasks.edit_one(task_id, task_dict)
            current_task = await uow.tasks.find_one(id=task_id)
            task_history_log = TaskHistorySchemaAdd(
                task_id=task_id,
                # чел, который до этого был исполнителем
                previous_assignee_id=current_task.assignee_id,
                # новый исполнитель
                new_assignee_id=task.assignee_id
            )
            task_history_log = task_history_log.model_dump()
            await uow.task_history.add_one(task_history_log)
            await uow.commit()
