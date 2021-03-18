# Import flask and template operators
from flask import Flask, render_template, _app_ctx_stack
from sqlalchemy.orm import scoped_session

from .database import SessionLocal

# Define the application
app = Flask(__name__)

# Configurations
app.config.from_object('config')

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

#initial general page
@app.route('/')
def main():
    return render_template("index.html")

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()

# Import the modules using their blueprint handler variable
# from app.process.controllers import mod_process as process
from app.shopfloor.controllers import mod_shopfloor as sf
from app.products.controllers import mod_products as products
from app.demands.controllers import mod_demands as demands

# Register blueprint
# app.register_blueprint(process)
app.register_blueprint(sf)
app.register_blueprint(products)
app.register_blueprint(demands)