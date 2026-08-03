from flask import Flask, jsonify, render_template, request, url_for, redirect, Blueprint #type: ignore

from models.database import db


chat_controller = Blueprint("chat_controller", __name__)