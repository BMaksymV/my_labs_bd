import yaml
from flask import Flask
from my_project import db, ma
from my_project.auth.domain import user, rental, equipment

app = Flask(__name__)

with open('config/app.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

db_config = config['db']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
ma.init_app(app)

from my_project.auth.route.user_route import user_bp
from my_project.auth.route.rental_route import rental_bp
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(rental_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)