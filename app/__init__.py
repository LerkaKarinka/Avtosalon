from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate, login_menenger
from .config import DevelopmentConfig  # или ProductionConfig
from .models import Menenger
from flask_login import login_user, login_required, logout_user, current_user

# Загрузка .env должна происходить до создания приложения
load_dotenv(override=True)

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_menenger.init_app(app)

    #Настройка менеджера входа
    login_menenger.login_view = 'login'
    login_menenger.login_message_category = 'info'
    login_menenger.login_message = 'Пожалуйста, войдите в систему, чтобы получить доступ к этой странице'
    @login_menenger.user_loader
    def load_user(menenger_id):
        return Menenger.query.get(int(menenger_id))
   

    # Регистрация маршрутов
    from . import routes
    routes.init_routes(app)

    
    
    return app