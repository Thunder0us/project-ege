from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Subject, Task, UserAnswer
from services.adaptive_logic import get_adaptive_tasks

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    subjects = Subject.query.all()
    return render_template('dashboard.html', subjects=subjects)

@main_bp.route('/subject/<int:subject_id>')
def start_exam(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    tasks = get_adaptive_tasks(subject_id, count=6)
    
    if not tasks:
        flash('В этом предмете пока нет заданий. Добавьте их через админ-панель.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    return render_template('exam.html', subject=subject, tasks=tasks)

@main_bp.route('/ai/generate', methods=['POST'])
def generate_ai_tasks():
    from ai_helper import generate_tasks_by_topic
    # Берём первую тему для примера (можно улучшить — брать слабые темы)
    topic = Topic.query.first()
    if not topic:
        return {"message": "Нет тем в базе"}, 400
    
    success, message = generate_tasks_by_topic(topic.id, count=3)
    return {"message": message}

@main_bp.route('/check_exam/<int:subject_id>', methods=['POST'])
def check_exam(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    results = []
    score = 0
    total = 0

    for key, value in request.form.items():
        if key.startswith('answer_'):
            try:
                task_id = int(key.replace('answer_', ''))
                user_answer = value.strip()
                task = Task.query.get(task_id)
                if task:
                    is_correct = user_answer.lower() == task.correct_answer.lower()
                    if is_correct:
                        score += 1
                    total += 1

                    results.append({
                        'task': task,
                        'user_answer': user_answer,
                        'correct': task.correct_answer,
                        'is_correct': is_correct,
                        'explanation': task.explanation
                    })

                    db.session.add(UserAnswer(
                        user_id=1,
                        task_id=task.id,
                        user_answer=user_answer,
                        is_correct=is_correct
                    ))
            except:
                continue

    db.session.commit()
    return render_template('result.html', subject=subject, results=results, score=score, total=total)