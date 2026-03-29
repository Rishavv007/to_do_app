import logging
from marshmallow import ValidationError
from app import db
from app.models.task import Task, Priority, Status
from app.schemas.task_schema import task_schema, tasks_schema

logger = logging.getLogger(__name__)


def _coerce_enums(data: dict) -> dict:
    """Convert string values to their corresponding Enum members for the Task model."""
    if "priority" in data and isinstance(data["priority"], str):
        data["priority"] = Priority(data["priority"])
    if "status" in data and isinstance(data["status"], str):
        data["status"] = Status(data["status"])
    return data


class TaskService:
    @staticmethod
    def create_task(data: dict) -> tuple:
        try:
            loaded = task_schema.load(data)
        except ValidationError as err:
            logger.warning(f"Validation failed on create: {err.messages}")
            return {"error": "Validation failed", "details": err.messages}, 400

        try:
            loaded = _coerce_enums(loaded)
            task = Task(**loaded)
            db.session.add(task)
            db.session.commit()
            return task_schema.dump(task), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating task: {e}")
            return {"error": "Internal Server Error", "message": "An unexpected error occurred."}, 500

    @staticmethod
    def get_all_tasks() -> tuple:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return tasks_schema.dump(tasks), 200

    @staticmethod
    def get_task(task_id: int) -> tuple:
        task = db.session.get(Task, task_id)
        if not task:
            return {"error": "Not Found", "message": "Task not found"}, 404
        return task_schema.dump(task), 200

    @staticmethod
    def update_task(task_id: int, data: dict) -> tuple:
        task = db.session.get(Task, task_id)
        if not task:
            return {"error": "Not Found", "message": "Task not found"}, 404

        try:
            loaded = task_schema.load(data, partial=True)
        except ValidationError as err:
            return {"error": "Validation failed", "details": err.messages}, 400

        try:
            loaded = _coerce_enums(loaded)
            for key, value in loaded.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.session.commit()
            return task_schema.dump(task), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating task: {e}")
            return {"error": "Internal Server Error", "message": "An unexpected error occurred."}, 500

    @staticmethod
    def delete_task(task_id: int) -> tuple:
        task = db.session.get(Task, task_id)
        if not task:
            return {"error": "Not Found", "message": "Task not found"}, 404

        try:
            db.session.delete(task)
            db.session.commit()
            return {"message": "Task deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting task: {e}")
            return {"error": "Internal Server Error", "message": "An unexpected error occurred."}, 500
