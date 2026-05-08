from models import Task, Topic
from sqlalchemy import func
import random

from models import Task, Topic
from sqlalchemy import func

def get_adaptive_tasks(subject_id: int, count: int = 6):
    """Выбираем задания только по предмету"""
    tasks = Task.query.join(Topic)\
              .filter(Topic.subject_id == subject_id)\
              .order_by(func.random())\
              .limit(count)\
              .all()
    
    return tasks
    
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