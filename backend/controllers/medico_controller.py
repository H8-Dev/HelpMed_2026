from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint #type: ignore

from models.database import db

med_controller = Blueprint("med_controller", __name__)

@med_controller.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_medico():
    if request.method == 'GET':
        return render_template(), 200