from flask import Flask #type: ignore
from flask_cors import CORS #type: ignore
from dotenv import load_dotenv #type: ignore
import os

load_dotenv()

from models.database import db
from models.mail import mail
from controllers.medico_controller import med_controller
from controllers.paciente_controller import pac_controller
from controllers.atend_controller import atend_controller
from controllers.arquivo_controller import arq_controller
from controllers.atend_previo_controller import prev_controller


def create_app():
    app = Flask(__name__)

    #Config Database
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", 'sqlite:///helpmed.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    #Blueprints
    app.register_blueprint(med_controller)
    app.register_blueprint(pac_controller)
    app.register_blueprint(atend_controller)
    app.register_blueprint(prev_controller)
    app.register_blueprint(arq_controller)

    #Porta Email
    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAILTRAP_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('MAILTRAP_PASS')
    app.config['MAIL_DEFAULT_SENDER'] = ('Sistema de Suporte - HelpMed', 'suporte@helpmed.com')

    mail.init_app(app)

    #Configurações do uso da API do Gemini
    app.config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
    app.config['GEMINI_API_PROMPT'] = os.getenv('GEMINI_API_PROMPT')
    app.config['GEMINI_API_MODELS'] = [
        "gemini-3.8-flash",       
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite"
    ]

    return app

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'TRUE')== 'TRUE'
    app.run(debug=debug, host='0.0.0.0', port=5000)