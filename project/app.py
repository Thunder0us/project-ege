import os
from flask import Flask
from config import Config
from models import db, Subject

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Исправляем путь к базе данных
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Абсолютный путь к БД
    db_path = os.path.join(instance_path, 'egemvp.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    db.init_app(app)
    
    # Регистрация blueprint'ов
    from routes.main import main_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
                # Создаём начальные предметы
        if not Subject.query.first():
            subjects = ["Математика", "Русский язык", "Физика", "Химия", "Информатика"]
            for subj_name in subjects:
                subj = Subject(name=subj_name)
                db.session.add(subj)
            db.session.commit()
            print("✅ Начальные предметы добавлены!")
        print("✅ База данных создана успешно!")
    print("🚀 Сервер запущен! Открой в браузере: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)