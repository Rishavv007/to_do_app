from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.services.ai_service import evaluate_task_with_ai
from marshmallow import ValidationError
from app.schemas.task_schema import AISuggestionSchema

task_blueprint = Blueprint('tasks', __name__)

@task_blueprint.route('', methods=['GET'])
def get_tasks():
    result, status = TaskService.get_all_tasks()
    return jsonify(result), status

@task_blueprint.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    result, status = TaskService.get_task(task_id)
    return jsonify(result), status

@task_blueprint.route('', methods=['POST'])
def create_task():
    data = request.get_json(silent=True) or {}
    result, status = TaskService.create_task(data)
    return jsonify(result), status

@task_blueprint.route('/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    result, status = TaskService.update_task(task_id, data)
    return jsonify(result), status

@task_blueprint.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result, status = TaskService.delete_task(task_id)
    return jsonify(result), status

@task_blueprint.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json(silent=True) or {}
    schema = AISuggestionSchema()
    try:
        validated = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "details": err.messages}), 400
        
    suggestion = evaluate_task_with_ai(validated.get('title'), validated.get('description', ''))
    return jsonify(suggestion), 200
