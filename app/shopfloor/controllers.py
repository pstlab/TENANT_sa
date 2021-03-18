# Import flask dependencies
from flask import Blueprint, render_template

from .models import Resource
from app import app

# Define the blueprint: 'shopfloor', set its url prefix: app.url/sf
mod_shopfloor = Blueprint('sf', __name__, url_prefix='/sf')

@mod_shopfloor.route('/')
def hello():
    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

@mod_shopfloor.route('/newRes/')
def new():
    return render_template("shopfloor/newRes.html")

@mod_shopfloor.route('/newAggr/')
def newAggr():
    return render_template("shopfloor/newAggr.html")