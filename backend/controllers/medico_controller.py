from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint

from models.database import db

med_controller = Blueprint("med_controller", __name__)
