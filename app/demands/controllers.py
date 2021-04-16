# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Demand
from app import app

from app.products import models as prod_mod

# Define the blueprint: 'demands', set its url prefix: app.url/demands
mod_demands = Blueprint('demands', __name__, url_prefix='/demands')

@mod_demands.route('/', methods=['GET'])
def hello():
    dem = app.session.query(Demand).all()
    return render_template("demands/indexDem.html", demands=dem)

@mod_demands.route('/', methods=['POST'])
def new():
    data = request.json
    # Add a new demand
    if(data[-1] == "new"):
        name = data[-2]['name']
        typeDem = data[-2]['type']
        product = data[-2]['product']
        quantity = data[-2]['quantity']
    
        # TODO cambiare il prodotto con la lista dei prodotti veri
        p1 = prod_mod.Product(name = 'AHHHHH')
        demand = Demand(name = name, quantity = quantity, product=p1, typeDem=typeDem)
        app.session.add(demand)

    if(data[-1] == "removeDem"):
        name = data[0]
        app.session.query(Demand).filter_by(name=name).delete()

    if(data[-1] == "editDem"):
        name = data[0]
        dem = app.session.query(Demand).filter_by(name=name).first()
        return redirect(url_for('demands.edit', demand = dem))

    app.session.commit()
    dem = app.session.query(Demand).all()
    return render_template("demands/indexDem.html", demands=dem)

@mod_demands.route('/editDem/')
def edit():
    dem = request.args.get('demand', None)
    return render_template("demands/modDem.html", demand=dem)