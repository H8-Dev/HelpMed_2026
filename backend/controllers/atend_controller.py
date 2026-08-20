from flask import jsonify, request, Blueprint #type: ignore

from models.database import db


atend_controller = Blueprint("atend_controller", __name__)

class AtendimentoController:
    pass

## @atend_controller.post('/atendimento')
## def gerarAtend(paciente, medico, av):
