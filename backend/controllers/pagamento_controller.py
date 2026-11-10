from flask import jsonify, request, Blueprint #type: ignore

from models.database import db


pag_controller = Blueprint("pag_controller", __name__)

class PagamentoController:
    @pag_controller.get('/pagamentos')
    def historico():
        return

    @pag_controller.post('/pagamentos')
    def gerar_pagamento():
        return