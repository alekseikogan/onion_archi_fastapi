from schemas.tasks import TaskHistorySchemaAdd, TaskSchemaAdd, TaskSchemaEdit
from utils.uow import InerfaceUnitofWork


class TasksService:

    async def add_task(self, uow: InerfaceUnitofWork, task: TaskSchemaAdd):
        """Добавить задачу."""
        tasks_dict = task.model_dump()
        async with uow:
            task_id = await uow.tasks.add_one(tasks_dict)
            await uow.commit()
            return task_id

    async def get_tasks(self, uow: InerfaceUnitofWork):
        """Получить всё задачи."""
        async with uow:
            tasks = await uow.tasks.find_all()
            return tasks

    async def edit_task(self, uow: InerfaceUnitofWork, task_id: int, task: TaskSchemaEdit):
        """Изменить задачу."""
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

    async def get_task_history(self, uow: InerfaceUnitofWork):
        """Получить историю задач."""
        async with uow:
            history = await uow.task_history()
            return history
