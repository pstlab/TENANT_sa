# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Process
from app import app

from app.products.models import Product

# Define the blueprint: 'process', set its url prefix: app.url/process
mod_process = Blueprint('process', __name__, url_prefix='/process')

#welcome page of the processes. Display the list and a button from which add a new process(new page), 
#remove a process(post request with id), view in detail a process(new page) from which modify it (new page)
@mod_process.route('/', methods=['GET'])
def hello():
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#remove a process
@mod_process.route('/', methods=['POST'])
def remove():
    data = request.json
    procId = data[0]
    app.session.query(Process).filter_by(id=procId).delete()
        
    app.session.commit()
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#add a new process to the db. welcome page and request (post) after the user data input
@mod_process.route('/newProc/', methods=['GET'])
def new():
    prod = app.session.query(Product).all()
    return render_template("processes/newProc.html", products=prod)

@mod_process.route('/newProc/', methods=['POST'])
def newP():
    data = request.json
    # Add a new product
    name = data[0]['name']
    pId = data[0]['product']
    p = app.session.query(Product).filter_by(id=pId).first()
    process = Process(name=name, product=p)

    app.session.add(process)
    app.session.commit()

    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#edit a process in the db. welcome page to view it and request (post) after the user data input
@mod_process.route('/viewProc/<procId>', methods=['GET'])
def mod(procId):
    proc = app.session.query(Process).filter_by(id=procId).first()
    prod = app.session.query(Product).all()
    return render_template("processes/detailProc.html", process=proc, products=prod)

@mod_process.route('/viewProc/<procId>', methods=['POST'])
def modP(procId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    pId = data[1]['processProduct']
    processId = data[0]

    #get the database values and update them
    proc = app.session.query(Process).filter_by(id=processId).first()
    proc.name = name
    p = app.session.query(Product).filter_by(id=pId).first()
    proc.product = p

    app.session.commit()
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)