from flask import Blueprint, jsonify
from ai_helper import generate_and_save_tasks, explain_with_ai
from models import Topic, Task
from sqlalchemy import func

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/generate', methods=['POST'])
def generate_tasks():
    # Выбираем тему с наименьшим количеством заданий
    topic = Topic.query.outerjoin(Task)\
              .group_by(Topic.id)\
              .order_by(func.count(Task.id))\
              .first()
    
    if not topic:
        return jsonify({"message": "Нет тем в базе"}), 400

    success, message = generate_and_save_tasks(topic.id, count=2)
    return jsonify({"message": message, "success": success})


@ai_bp.route('/explain/<int:task_id>', methods=['POST'])
def explain_task(task_id):
    task = Task.query.get_or_404(task_id)
    explanation = explain_with_ai(task.text, task.correct_answer)
    return jsonify({"explanation": explanation})