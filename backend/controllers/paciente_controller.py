from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint #type: ignore

from models.database import db

pac_controller = Blueprint("pac_controller", __name__)

@pac_controller.route('/cadastrar', methods=['POST'])
def cadastrar_paciente():
        dados = {
            "cpf": str(request.form['cpf']),
            "senha": str(request.form['senha']),
            "nome": str(request.form['nome']),
            "sobrenome": str(request.form['sobrenome']),
            "email": str(request.form['email'])
        }
        return jsonify(dados), 200