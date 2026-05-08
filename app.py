import os
from flask import Flask
from config import Config
from models import db, Subject
from routes.statistics import stats_bp
from routes.ai import ai_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Надёжный путь к БД
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    db_path = os.path.join(instance_path, 'egemvp.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    db.init_app(app)
    
    # Blueprints
    from routes.main import main_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(ai_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not Subject.query.first():
            for name in ["Математика", "Русский язык", "Физика", "Химия", "Информатика"]:
                if not Subject.query.filter_by(name=name).first():
                    db.session.add(Subject(name=name))
            db.session.commit()
            print("✅ Предметы добавлены")
    
    print("🚀 Запущено на http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)