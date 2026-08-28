from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.paciente.buscar_cpf_service import BuscarPacCpfService
from services.paciente.cadastrar_paciente_service import CriarPacienteService
from services.paciente.login_paciente_services import LoginPacienteService

pac_controller = Blueprint("pac_controller", __name__)


class PacienteController:

    @pac_controller.post('/pacientes/cadastrar')
    def cadastrar_paciente():
        try:
            body = request.get_json(silent=True) or request.form
            dados = {
                "cpf": str(body['cpf']),
                "senha": str(body['senha']),
                "nome": str(body['nome']),
                "sobrenome": str(body['sobrenome']),
                "email": str(body['email'])
            }

            service = CriarPacienteService()
            paciente = service.cadastrar(dados)
            return jsonify(paciente), 201
        
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao cadastrar paciente."}), 500

    @pac_controller.get('/pacientes/buscar/<string:paciente_cpf>')
    def buscar_paciente_por_cpf(paciente_cpf):

        service = BuscarPacCpfService()
        paciente = service.executar(paciente_cpf)

        if paciente is None:
            return jsonify({"error": "Paciente não encontrado."}), 404

        return jsonify(paciente), 200

    @pac_controller.post('/pacientes/login')
    def login_paciente():
        try:
            body = request.get_json(silent=True)
            if body is None:
                body = request.form.to_dict()

            cpf = str(body.get("cpf", "")),
            senha = str(body.get("senha", ""))
        
            service = LoginPacienteService()
            validacao = service.login(cpf, senha)
            
            if validacao['check1'] == 1:
                return jsonify("Logado com sucesso"), 200
            else:
                return jsonify("Usuário ou Senha inválidos!!"), 401
        
        
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao realizar o login do paciente."}), 500
        