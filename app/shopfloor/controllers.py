# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import *
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
    resId = int(data[0]['id'])
    typeR = data[0]['type']
    klass = globals()[typeR]

    app.session.query(klass).filter_by(id=resId).delete()    #OnCascade doesn't work
    app.session.query(Resource).filter_by(id=resId).delete()    
    app.session.commit()

    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

#add a new resource to the db. welcome page and request (post) after the user data input
@mod_shopfloor.route('/newRes/', methods=['GET'])
def new():
    ar = app.session.query(AggregateResource).all()
    c = app.session.query(Capability).all()
    return render_template("shopfloor/newRes.html", types=TYPES_OF_RESOURCES, aggregates=ar, capabilities=c)

@mod_shopfloor.route('/newRes/', methods=['POST'])
def newR():
    data = request.json
    # Add a new resource
    name = data[0]['name']
    descr = data[0]['description']
    typeR = data[0]['type']
    aggregateId = data[0]['aggregate']
    ar = app.session.query(AggregateResource).filter_by(id=aggregateId).first()
    f = []

    capabilities = data[0]['capabilities']
    for element in capabilities:
        if (element['type'] == 'new'):
            tmp = Capability(name=element['name'])
            app.session.add(tmp)
        else:
            tmp = app.session.query(Capability).filter_by(name=element['name']).first()
        f.append(tmp)
    app.session.commit()

    klass = globals()[typeR]
    resource = klass(name=name, description=descr, aggregate_resource=ar, capabilities=f)

    app.session.add(resource)
    app.session.commit()

    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

#edit a resource in the db. welcome page and request (post) after the user data input
@mod_shopfloor.route('/editRes/<resId>', methods=['GET'])
def edit(resId):
    res = app.session.query(Resource).filter_by(id=resId).first()
    ar = app.session.query(AggregateResource).all()
    f = app.session.query(Capability).all()
    return render_template("shopfloor/modRes.html", resource = res, types=TYPES_OF_RESOURCES, aggregates=ar, capabilities=f)
    
@mod_shopfloor.route('/editRes/<resId>', methods=['POST'])
def editR(resId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    descr = data[1]['description']
    # typeR = data[1]['type']
    aggregateId = data[1]['aggregate']
    resId = data[0]

    #get the database values and update them
    res = app.session.query(Resource).filter_by(id=resId).first()

    res.name = name
    res.description = descr
    ar = app.session.query(AggregateResource).filter_by(id=aggregateId).first()
    res.aggregate_resource = ar

    # if(res.typeRes != typeR):
        #TODO it doesn't work properly
        #The resource is still listed on the table of the old class
        # res.typeRes = typeR

    f = []
    capabilities = data[1]['capabilities']
    for element in capabilities:
        if (element['type'] == 'new'):
            tmp = Capability(name=element['name'])
            app.session.add(tmp)
        else:
            tmp = app.session.query(Capability).filter_by(name=element['name']).first()
        f.append(tmp)
    app.session.commit()

    res.capabilities = f

    app.session.commit()
    res = app.session.query(Resource).all()
    return render_template("shopfloor/indexSF.html", resources=res)

#manage the aggregate resources in the db. Display the list and a form from which add
#a new aggregate resource(post request), remove an aggregate resource(post request with id),
#modify the name, add or remove a resource of an aggregate resource(post request)
@mod_shopfloor.route('/manageAggr/', methods=['GET'])
def manage():
    ar = app.session.query(AggregateResource).all()
    return render_template("shopfloor/manageRes.html", aResources=ar)

@mod_shopfloor.route('/manageAggr/', methods=['POST'])
def newAR():
    data = request.json
    # Add a new aggregate resource
    if(data[-1] == "new"):
        name = data[-2]['name']
        parentId = data[-2]['ar']
        parent = app.session.query(AggregateResource).filter_by(id=parentId).first()
        #TODO list of resources

        ar = AggregateResource(name = name, parent=parent)
        app.session.add(ar)

    #remove an aggregate resource
    if(data[-1] == "remove"):
        arId = data[0]
        app.session.query(AggregateResource).filter_by(id=arId).delete()

    #modify a product family
    if(data[-1] == "edit"):
        #get data from input
        name = data[-2]['name']
        parentId = data[-2]['ar']
        parent = app.session.query(AggregateResource).filter_by(id=parentId).first()
        #get the database values and update them
        arId = data[0]
        ar = app.session.query(AggregateResource).filter_by(id=arId).first()

        ar.name = name
        ar.parent = parent

    #remove a resource from the aggregate resource
    if(data[-1] == 'removeRes'):
        #get data
        arId = data[0]['aggrRes']
        resId = data[0]['resId']

        res = app.session.query(Resource).filter_by(id=resId).first()
        ar = app.session.query(AggregateResource).filter_by(id=arId).first()
        ar.resources.remove(res)
    
    #remove an aggregate resource from the aggregate resource
    if(data[-1] == 'removeAggRes'):
        #get data
        arId = data[0]['aggrRes']
        resId = data[0]['aggResId']

        toRemove = app.session.query(AggregateResource).filter_by(id=resId).first()
        ar = app.session.query(AggregateResource).filter_by(id=arId).first()
        ar.children.remove(toRemove)

        
    app.session.commit()
    ars = app.session.query(AggregateResource).all()
    return render_template("shopfloor/manageRes.html", aResources=ars)