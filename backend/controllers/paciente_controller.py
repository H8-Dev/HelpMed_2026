from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.paciente.buscar_cpf_service import BuscarPacCpfService
from services.paciente.cadastrar_paciente_service import CriarPacienteService
from services.paciente.login_paciente_service import LoginPacienteService
from services.paciente.desativar_paciente_service import DesativarPacienteService
from services.paciente.email_paciente_service import EmailPacienteService
from services.paciente.update_paciente_service import UpdatePacienteService

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
                "email": str(body['email']),
            }

            service = CriarPacienteService()
            paciente = service.cadastrar(dados)
            return jsonify(paciente), 201
        
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao cadastrar paciente."}), 500

    #@pac_controller.get('/pacientes/buscar/<int:paciente_cpf>')
    #def buscar_paciente_por_cpf(paciente_cpf):
    #
    #    cpf_limpo = f"{paciente_cpf}"
    #    cpf_limpo = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    #
    #    service = BuscarPacCpfService()
    #    paciente = service.executar(cpf_limpo)
    #
    #    if paciente is None:
    #        return jsonify({"error": "Paciente não encontrado."}), 404
    #
    #    return jsonify(paciente), 200

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

    #@pac_controller.post('/pacientes/email') - Unfinished
    #def email_paciente():
    #    try:
    #        body = request.get_json(silent=True)
    #        id = str(body.get("id", ""))
    #
    #        service = EmailPacienteService()
    #        result = service.executar(id)
    #        return jsonify("Email enviado com sucesso!"), 200
    #
    #    except ValueError as error:
    #       return jsonify({"error": str(error)}), 400
    
        

    @pac_controller.put('/pacientes/desativar')
    def desativar_paciente():
        try:
            body = request.get_json(silent=True)
            cpf = body
            service = DesativarPacienteService()
            execute = service.desativar(cpf)

            if execute == False:
                return jsonify({"error": "Paciente não encontrado."}), 404
    
            return jsonify({"message": "Paciente desativado"}), 200
        
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao desativar o paciente."}), 500

    @pac_controller.get('/pacientes/email/<int:cpf>')
    def get_email(cpf):
        try:
            service = EmailPacienteService()
            paciente = service.executar(cpf)
            
            return jsonify(paciente.email), 200

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    @pac_controller.put('/pacientes/atualizar')
    def atualizar_paciente():
        try:
            body = request.get_json(silent=True)
            if body is None:
                body = request.form.to_dict()

            cpf = str(body.get("cpf", ""))
            dados = {
                    "senha": str(body.get("senha", "")),
                    "email": str(body.get("email", ""))
                    }

            service = UpdatePacienteService()
            paciente = service.executar(cpf, dados)

            return jsonify({"message": "Paciente atualizado com sucesso."}), 200
        
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao atualizar o médico."}), 500