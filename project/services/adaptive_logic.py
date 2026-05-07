from models import Task, Topic
from sqlalchemy import func
import random

def get_adaptive_tasks(subject_id: int, user_id: int = 1, count: int = 5):
    """Адаптивный выбор заданий ТОЛЬКО по выбранному предмету"""
    
    # Основной запрос — только задания из нужного предмета
    tasks = Task.query.join(Topic)\
              .filter(Topic.subject_id == subject_id)\
              .order_by(func.random())\
              .limit(count)\
              .all()
    
    # Если заданий мало — дополняем только из этого предмета
    if len(tasks) < count:
        needed = count - len(tasks)
        extra = Task.query.join(Topic)\
                  .filter(Topic.subject_id == subject_id)\
                  .order_by(func.random())\
                  .limit(needed)\
                  .all()
        tasks.extend(extra)
    
    # Убираем возможные дубликаты
    seen = set()
    unique_tasks = []
    for task in tasks:
        if task.id not in seen:
            seen.add(task.id)
            unique_tasks.append(task)
    
    return unique_tasks[:count]