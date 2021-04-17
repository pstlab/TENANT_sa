# Import flask dependencies
from flask import Blueprint, render_template

from .models import Process
from app import app

# Define the blueprint: 'process', set its url prefix: app.url/process
mod_process = Blueprint('process', __name__, url_prefix='/process')

@mod_process.route('/')
def hello():
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

@mod_process.route('/newProc/')
def new():
    return render_template("processes/newProc.html")

@mod_process.route('/modProc/')
def mod():
    return render_template("processes/modProc.html")