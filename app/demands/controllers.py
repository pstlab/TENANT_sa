# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Demand
from app import app

from app.products.models import Product
from app.processes.models import Process

# Define the blueprint: 'demands', set its url prefix: app.url/demands
mod_demands = Blueprint('demands', __name__, url_prefix='/demands')

proc = []

#welcome page of the demands. Display the list and a form from which add a new demand(post request), 
#remove a demand(post request with id), modify a demand(new page)
@mod_demands.route('/', methods=['GET'])
def hello():
    global proc
    dem = app.session.query(Demand).all()
    prod = app.session.query(Product).all()
    return render_template("demands/indexDem.html", demands=dem, products=prod, processes=proc)

@mod_demands.route('/', methods=['POST'])
def new():
    global proc
    data = request.json
    # Add a new demand
    if(data[-1] == "new"):
        name = data[-2]['name']
        typeDem = data[-2]['type']
        productId = data[-2]['product']
        quantity = data[-2]['quantity']
        processId = data[-2]['process']
    
        p = app.session.query(Product).filter_by(id=productId).first()
        pr = app.session.query(Process).filter_by(id=processId).first()
        demand = Demand(name = name, quantity = quantity, product=p, typeDem=typeDem, process=pr)
        app.session.add(demand)
        # and empty the list of processes
        proc = []

    #remove a demand
    if(data[-1] == "removeDem"):
        demId = data[0]
        app.session.query(Demand).filter_by(id=demId).delete()

    #add the processes depending on the product
    if(data[-1] == "askForProcesses"):
        productId = data[0]
        p = app.session.query(Product).filter_by(id=productId).first()
        proc = p.processes
        
    app.session.commit()
    dem = app.session.query(Demand).all()
    prod = app.session.query(Product).all()
    return render_template("demands/indexDem.html", demands=dem, products=prod, processes=proc)

#edit a demand in the db. welcome page and request (post) after the user data input
@mod_demands.route('/editDem/<demId>', methods=['GET'])
def edit(demId):
    global proc
    dem = app.session.query(Demand).filter_by(id=demId).first()
    prod = app.session.query(Product).all()
    return render_template("demands/modDem.html", demand=dem, products=prod, processes=proc)

@mod_demands.route('/editDem/<demId>', methods=['POST'])
def editDem(demId):
    global proc
    #get the data from user input
    data = request.json

    demandId = data[0]
    dem = app.session.query(Demand).filter_by(id=demandId).first()
    
     #add the processes depending on the product
    if(data[-1] == "askForProcesses"):
        productId = data[1]
        p = app.session.query(Product).filter_by(id=productId).first()
        proc = p.processes

    else:
        # Get the new values
        name = data[1]['name']
        typeDem = data[1]['type']
        productId = data[1]['product']
        quantity = data[1]['quantity']
        processId = data[1]['process']

        #get the database values and update them
        dem.name = name
        dem.quantity = quantity
        p = app.session.query(Product).filter_by(id=productId).first()
        dem.product = p
        dem.typeDem = typeDem
        pr = app.session.query(Process).filter_by(id=processId).first()
        dem.process=pr

    app.session.commit()
    dems = app.session.query(Demand).all()
    prod = app.session.query(Product).all()
    return render_template("demands/indexDem.html", demands=dems, products=prod, processes=proc)