
from utils.repository import SQLAlchemyRepository
from models.tasks import Tasks


class TasksRepository(SQLAlchemyRepository):
    model = Tasks
