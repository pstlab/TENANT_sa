# Import flask dependencies
from flask import Blueprint, render_template

from .models import Product
from app import app

# Define the blueprint: 'shopfloor', set its url prefix: app.url/process
mod_products = Blueprint('products', __name__, url_prefix='/products')

@mod_products.route('/')
def hello():
    prods = app.session.query(Product).all()
    return render_template("products/indexProd.html", products=prods)

@mod_products.route('/newProd/')
def new():
    return render_template("products/newProd.html")