import yaml
from flask import Flask
# Імпортуємо db та ma з нашого пакета
from my_project import db, ma

app = Flask(__name__)

# Завантаження конфігурації
with open('config/app.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

db_config = config['db']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Прив'язуємо базу до нашого додатка
db.init_app(app)
ma.init_app(app)

# Імпортуємо маршрути ТІЛЬКИ ПІСЛЯ ініціалізації бази
from my_project.auth.route.user_route import user_bp
app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)