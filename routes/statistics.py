from flask import Blueprint, render_template
from models import db, Subject, Task, UserAnswer, Topic
from sqlalchemy import func
from datetime import datetime, timedelta

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/profile')
def profile():
    # Общая статистика
    total_answers = UserAnswer.query.count()
    correct_answers = UserAnswer.query.filter_by(is_correct=True).count()
    accuracy = round((correct_answers / total_answers * 100), 1) if total_answers > 0 else 0

    # Статистика по предметам
    subjects_stats = []
    for subject in Subject.query.all():
        total = UserAnswer.query.join(Task).join(Topic)\
                .filter(Topic.subject_id == subject.id).count()
        if total > 0:
            correct = UserAnswer.query.join(Task).join(Topic)\
                      .filter(Topic.subject_id == subject.id, UserAnswer.is_correct == True).count()
            percent = round(correct / total * 100, 1)
            subjects_stats.append({
                'subject': subject,
                'total': total,
                'correct': correct,
                'percent': percent
            })

    # Разбор по темам
    topics_stats = db.session.query(
        Topic.name,
        Subject.name.label('subject_name'),
        func.count(UserAnswer.id).label('total'),
        func.sum(UserAnswer.is_correct.cast(db.Integer)).label('correct')
    ).join(Task, Task.topic_id == Topic.id)\
     .join(Subject, Subject.id == Topic.subject_id)\
     .join(UserAnswer, UserAnswer.task_id == Task.id)\
     .group_by(Topic.id, Subject.name)\
     .all()

    # График прогресса
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    progress_raw = db.session.query(
        func.date(UserAnswer.answered_at).label('date'),
        func.count(UserAnswer.id).label('total'),
        func.sum(UserAnswer.is_correct.cast(db.Integer)).label('correct')
    ).filter(UserAnswer.answered_at >= thirty_days_ago)\
     .group_by(func.date(UserAnswer.answered_at))\
     .order_by('date').all()

    progress_data = []
    for p in progress_raw:
        progress_data.append({
            'date': p.date.strftime('%d.%m') if hasattr(p.date, 'strftime') else str(p.date),
            'accuracy': round((p.correct / p.total * 100), 1) if p.total > 0 else 0
        })

    return render_template('profile.html',
                         total_answers=total_answers,
                         accuracy=accuracy,
                         subjects_stats=subjects_stats,
                         topics_stats=topics_stats,
                         progress_data=progress_data)