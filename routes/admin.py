from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Subject, Topic, Task

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/add_task', methods=['GET', 'POST'])
def add_task():
    subjects = Subject.query.all()
    
    if request.method == 'POST':
        try:
            subject_id = int(request.form.get('subject_id'))
            topic_name = request.form.get('topic_name', '').strip()
            task_text = request.form.get('task_text', '').strip()
            correct_answer = request.form.get('correct_answer', '').strip()
            explanation = request.form.get('explanation', '').strip()
            
            if not all([subject_id, topic_name, task_text, correct_answer]):
                flash('Заполните все обязательные поля!', 'danger')
                return redirect(url_for('admin.add_task'))
            
            topic = Topic.query.filter_by(subject_id=subject_id, name=topic_name).first()
            if not topic:
                topic = Topic(subject_id=subject_id, name=topic_name)
                db.session.add(topic)
                db.session.commit()
            
            task = Task(
                topic_id=topic.id,
                text=task_text,
                correct_answer=correct_answer,
                explanation=explanation or "Разбор решения будет добавлен позже."
            )
            db.session.add(task)
            db.session.commit()
            
            flash(f'✅ Задание по теме "{topic_name}" успешно добавлено!', 'success')
            return redirect(url_for('admin.add_task'))
            
        except Exception as e:
            flash(f'Ошибка при добавлении: {str(e)}', 'danger')
    
    return render_template('admin_add_task.html', subjects=subjects)