# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Product, ProductFamily
from app import app

# Define the blueprint: 'products', set its url prefix: app.url/products
mod_products = Blueprint('products', __name__, url_prefix='/products')

#welcome page of the products. Display the list from which add a new product(new page), 
#a new product family(new page), remove a product(post request with id), modify a product(new page)
@mod_products.route('/', methods=['GET'])
def hello():
    prods = app.session.query(Product).all()
    return render_template("products/indexProd.html", products=prods)

#remove a product
@mod_products.route('/', methods=['POST'])
def remove():
    data = request.json
    prodId = data[0]
    app.session.query(Product).filter_by(id=prodId).delete()
        
    app.session.commit()
    prods = app.session.query(Product).all()
    return render_template("products/indexProd.html", products=prods)


#add a new product to the db. welcome page and request (post) after the user data input
@mod_products.route('/newProd/', methods=['GET'])
def new():
    pf = app.session.query(ProductFamily).all()
    return render_template("products/newProd.html", prodfamilies=pf)

@mod_products.route('/newProd/', methods=['POST'])
def newP():
    data = request.json
    # Add a new product
    name = data[0]['name']
    pfId = data[0]['productfamily']
    
    pf = app.session.query(ProductFamily).filter_by(id=pfId).first()
    product = Product(name = name, product_family = pf)
    app.session.add(product)
    
    app.session.commit()
    prods = app.session.query(Product).all()
    return render_template("products/indexProd.html", products=prods)


#edit a product in the db. welcome page and request (post) after the user data input
@mod_products.route('/editProd/<prodId>', methods=['GET'])
def edit(prodId):
    prod = app.session.query(Product).filter_by(id=prodId).first()
    pf = app.session.query(ProductFamily).all()
    return render_template("products/modProd.html", product = prod, prodfamilies=pf)

@mod_products.route('/editProd/<prodId>', methods=['POST'])
def editP(prodId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    pfId = data[1]['productfamily']
    productId = data[0]

    #get the database values and update them
    prod = app.session.query(Product).filter_by(id=productId).first()
    prod.name = name
    pf = app.session.query(ProductFamily).filter_by(id=pfId).first()
    prod.product_family = pf

    app.session.commit()
    prods = app.session.query(Product).all()
    return render_template("products/indexProd.html", products=prods)


#manage the product families in the db. Display the list and a form from which add
#a new product family(post request), remove a product family(post request with id),
#modify the name of a product family(post request)
@mod_products.route('/PF/', methods=['GET'])
def manage():
    prodFs = app.session.query(ProductFamily).all()
    return render_template("products/managePF.html", families = prodFs)

@mod_products.route('/PF/', methods=['POST'])
def managePF():
    data = request.json
    # Add a new product family
    if(data[-1] == "new"):
        name = data[-2]['name']

        family = ProductFamily(name = name)
        app.session.add(family)

    #remove a product family
    if(data[-1] == "remove"):
        pfId = data[0]
        app.session.query(ProductFamily).filter_by(id=pfId).delete()

    #modify a product family
    if(data[-1] == "edit"):
        #get data from input
        name = data[1]['name']
        #process = data[1]['process']
        #get the database values and update them
        pfId = data[0]
        pf = app.session.query(ProductFamily).filter_by(id=pfId).first()

        pf.name = name
        #pf.process = process
        
    app.session.commit()
    prodFs = app.session.query(ProductFamily).all()
    return render_template("products/managePF.html", families = prodFs)