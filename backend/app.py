from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os


from models.database import db
from controllers.medico_controller import med_controller
from controllers.paciente_controller import pac_controller
from controllers.chat_controller import chat_controller


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpmed.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(med_controller)
    app.register_blueprint(pac_controller)
    app.register_blueprint(chat_controller)

    return app

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'TRUE')== 'TRUE'
    app.run(debug=debug, host='0.0.0.0', port=5000)