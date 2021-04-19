# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Resource, AggregateResource
from app import app

# Define the blueprint: 'shopfloor', set its url prefix: app.url/sf
mod_shopfloor = Blueprint('sf', __name__, url_prefix='/sf')

#welcome page of the resources. Display the list and a button from which add a new resource(new page), 
#a new aggregate resource(new page), remove a resource(post request with id), modify a resource(new page)
@mod_shopfloor.route('/', methods=['GET'])
def hello():
    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

#remove a resource
@mod_shopfloor.route('/', methods=['POST'])
def remove():
    data = request.json
    resId = data[0]

    app.session.query(Resource).filter_by(id=resId).delete()    
    app.session.commit()

    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

#add a new resource to the db. welcome page and request (post) after the user data input
@mod_shopfloor.route('/newRes/', methods=['GET'])
def new():
    ar = app.session.query(AggregateResource).all()
    return render_template("shopfloor/newRes.html", aggregates=ar)

@mod_shopfloor.route('/newRes/', methods=['POST'])
def newR():
    data = request.json
    # Add a new resource
    name = data[0]['name']
    typeR = data[0]['type']
    aggregateId = data[0]['aggregate']
    ar = app.session.query(AggregateResource).filter_by(id=aggregateId).first()
    resource = Resource(name=name, typeRes=typeR, aggregate_resource=ar)

    app.session.add(resource)
    app.session.commit()

    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

#edit a resource in the db. welcome page and request (post) after the user data input
@mod_shopfloor.route('/editRes/<resId>', methods=['GET'])
def edit(resId):
    res = app.session.query(Resource).filter_by(id=resId).first()
    ar = app.session.query(AggregateResource).all()
    return render_template("shopfloor/modRes.html", resource = res, aggregates=ar)

@mod_shopfloor.route('/editRes/<resId>', methods=['POST'])
def editR(resId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    typeR = data[1]['type']
    aggregateId = data[1]['aggregate']
    resId = data[0]

    #get the database values and update them
    res = app.session.query(Resource).filter_by(id=resId).first()
    res.name = name
    res.typeRes = typeR
    ar = app.session.query(AggregateResource).filter_by(id=aggregateId).first()
    res.aggregate_resource = ar

    app.session.commit()
    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

@mod_shopfloor.route('/newAggr/')
def newAggr():
    return render_template("shopfloor/newAggr.html")