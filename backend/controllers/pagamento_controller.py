from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint #type: ignore

from models.database import db


pag_controller = Blueprint("pag_controller", __name__)