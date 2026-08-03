from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint #type: ignore

from models.database import db

from services.medico.cadastrar_medico_service import CriarMedicoService

med_controller = Blueprint("med_controller", __name__)

@med_controller.route('/cadastrar', methods=['POST'])
def cadastrar_medico():
    try:
        dados = {
            "crm": str(request.form['crm']),
            "cpf": str(request.form['cpf']),
            "senha": str(request.form['senha']),
            "nome": str(request.form['nome']),
            "sobrenome": str(request.form['sobrenome']),
            "email": str(request.form['email'])
        }

        service = CriarMedicoService()
        medico = service.cadastrar(dados)
        return jsonify(medico), 201

  
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Erro ao cadastrar médico."}), 500