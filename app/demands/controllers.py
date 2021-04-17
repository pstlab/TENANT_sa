# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Demand
from app import app

from app.products import models as prod_mod

# Define the blueprint: 'demands', set its url prefix: app.url/demands
mod_demands = Blueprint('demands', __name__, url_prefix='/demands')

#welcome page of the demands. Display the list and a form from which add a new demand(post request), 
#remove a demand(post request with id), modify a demand(new page)
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

    #remove a demand
    if(data[-1] == "removeDem"):
        demId = data[0]
        app.session.query(Demand).filter_by(id=demId).delete()
        
    app.session.commit()
    dem = app.session.query(Demand).all()
    return render_template("demands/indexDem.html", demands=dem)

#edit a demand in the db. welcome page and request (post) after the user data input
@mod_demands.route('/editDem/<demId>', methods=['GET'])
def edit(demId):
    dem = app.session.query(Demand).filter_by(id=demId).first()
    return render_template("demands/modDem.html", demand=dem)

@mod_demands.route('/editDem/<demId>', methods=['POST'])
def editDem(demId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    typeDem = data[1]['type']
    product = data[1]['product']
    quantity = data[1]['quantity']
    demandId = data[0]

    #get the database values and update them
    dem = app.session.query(Demand).filter_by(id=demandId).first()
    dem.name = name
    dem.quantity = quantity
    #TODO il cazzo di prodotto
    #dem.product = product
    dem.typeDem = typeDem

    app.session.commit()
    dems = app.session.query(Demand).all()
    return render_template("demands/indexDem.html", demands=dems)