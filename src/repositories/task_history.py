
from utils.repository import SQLAlchemyRepository
from models.tasks import TaskHistory


class TaskHistoryRepository(SQLAlchemyRepository):
    model = TaskHistory
