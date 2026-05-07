from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Subject, Topic, Task

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/add_task', methods=['GET', 'POST'])
def add_task():
    subjects = Subject.query.all()
    
    if request.method == 'POST':
        try:
            subject_id = int(request.form['subject_id'])
            topic_name = request.form['topic_name'].strip()
            task_text = request.form['task_text'].strip()
            correct_answer = request.form['correct_answer'].strip()
            explanation = request.form.get('explanation', '').strip()
            
            # Создаём тему, если её нет
            topic = Topic.query.filter_by(subject_id=subject_id, name=topic_name).first()
            if not topic:
                topic = Topic(subject_id=subject_id, name=topic_name)
                db.session.add(topic)
                db.session.commit()
            
            task = Task(
                topic_id=topic.id,
                text=task_text,
                correct_answer=correct_answer,
                explanation=explanation or "Объяснение будет добавлено позже."
            )
            db.session.add(task)
            db.session.commit()
            
            flash('✅ Задание успешно добавлено!', 'success')
            return redirect(url_for('admin.add_task'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'danger')
    
    return render_template('admin_add_task.html', subjects=subjects)