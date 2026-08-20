from flask import Flask #type: ignore
from flask_cors import CORS #type: ignore
from dotenv import load_dotenv #type: ignore
import os


from models.database import db
from controllers.medico_controller import med_controller
from controllers.paciente_controller import pac_controller
from controllers.atend_controller import atend_controller


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpmed.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(med_controller)
    app.register_blueprint(pac_controller)
    app.register_blueprint(atend_controller)

    return app

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'TRUE')== 'TRUE'
    app.run(debug=debug, host='0.0.0.0', port=5000)