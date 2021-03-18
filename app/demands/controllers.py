# Import flask dependencies
from flask import Blueprint, render_template

from .models import Demand
from app import app

# Define the blueprint: 'demands', set its url prefix: app.url/demands
mod_demands = Blueprint('demands', __name__, url_prefix='/demands')

@mod_demands.route('/')
def hello():
    dem = app.session.query(Demand).all()
    return render_template("demands/indexDem.html", demands=dem)

@mod_demands.route('/newDem/')
def new():
    return render_template("demands/newDem.html")

@mod_demands.route('/modDem/')
def mod():
    return render_template("demands/modDem.html")