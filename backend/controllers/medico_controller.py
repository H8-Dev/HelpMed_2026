from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.medico.cadastrar_medico_service import CriarMedicoService
from services.medico.buscar_crm_service import BuscarMedicoPorCRMService
from services.medico.buscar_formacao_service import BuscarMedicoPorFormacaoService
from services.medico.login_medico_service import LoginMedicoService
from services.medico.desativar_medico_service import DesativarMedicoService 
from services.medico.email_medico_service import EmailMedicoService
from services.medico.update_medico_service import UpdateMedicoService

med_controller = Blueprint("med_controller", __name__)

class MedicoController:
    
    @med_controller.post('/medicos/cadastrar')
    def cadastrar_medico():
        try:
            body = request.get_json(silent=True) or request.form.to_dict()

            dados = {
                "crm": str(body['crm']),
                "cpf": str(body['cpf']),
                "senha": str(body['senha']),
                "nome": str(body['nome']),
                "sobrenome": str(body['sobrenome']),
                "email": str(body['email']),
                "formacao": str(body['formacao'])
            }

            service = CriarMedicoService()
            medico = service.cadastrar(dados)
            return jsonify(medico), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao cadastrar médico."}), 500


    @med_controller.get('/medicos/buscar/formacao/<string:formacao>')
    def buscar_medico_formacao(formacao):

        service = BuscarMedicoPorFormacaoService()
        medicos = service.executar(formacao)

        if not medicos:
            return jsonify({"error": "Nenhum médico encontrado com essa formação."}), 404

        return jsonify(medicos), 200

    @med_controller.post('/medicos/login')
    def login_medico():
        try:
            body = request.get_json(silent=True) or request.form.to_dict()
        
            crm = str(body['crm']),
            senha = str(body['senha'])
            
            service = LoginMedicoService()
            validacao = service.login(crm, senha)

            if validacao['check1'] == 1:
                return jsonify("Logado com sucesso"), 200
            else:
                return jsonify("Usuário ou Senha inválidos!!"), 401
            
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao realizar o login do médico."}), 500

    @med_controller.post('/medicos/email')
    def email_medico():
        try:
            body = request.get_json(silent=True)
            id = str(body.get("id", ""))
    
            service = EmailMedicoService()
            service.executar(id)
            return jsonify("Email enviado com sucesso!"), 200
    
        except ValueError as error:
           if error.type == "GENERIC":
              return jsonify({"error": str(error.e)}), 500
           
           if error.type == "STMP":
              return jsonify({"error": str(error.e)}), 500
           
           return jsonify({"error": str(error.e)}), 400

    @med_controller.put('/medicos/desativar')
    def desativar_medico():
        try:
            body = request.get_json(silent=True)
            crm = body
            service = DesativarMedicoService()
            service.desativar(crm)
    
            return jsonify({"message": "Medico desativado"}), 200

        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao desativar o medico."}), 500

    @med_controller.get('/medicos/email/<int:crm>')
    def get_email(crm):
        try:
            service = BuscarMedicoPorCRMService()
            medico = service.executar(crm)

            return jsonify(medico['email']), 200

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    @med_controller.put('/medicos/atualizar')
    def atualizar_medico():
        try:
            body = request.get_json(silent=True) or request.form.to_dict()

            crm = str(body['crm'])
            dados = {
                    "senha": str(body['senha']),
                    "email": str(body['email']),
                    "formacao": str(body['formacao'])
                    }

            service = UpdateMedicoService()
            medico = service.executar(crm, dados)

            return jsonify({"message": "Médico atualizado com sucesso."}), 200
        
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao atualizar o médico."}), 500