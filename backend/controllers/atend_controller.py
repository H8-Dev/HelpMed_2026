from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint #type: ignore

from models.database import db


atend_controller = Blueprint("atend_controller", __name__)

## @atend_controller.post('/atendimento')
## def gerarAtend(paciente, medico, av):
