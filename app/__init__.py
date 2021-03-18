# Import flask and template operators
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Define the application
app = Flask(__name__)

# Configurations
app.config.from_object('config')

#create db
db = SQLAlchemy(app)

#initial general page
@app.route('/')
def main():
    return render_template("index.html")

# Import the modules using their blueprint handler variable
# from app.mod_process.controllers import mod_process as process
from app.shopfloor.controllers import mod_shopfloor as sf
from app.products.controllers import mod_products as products
# from app.mod_demands.controllers import mod_demands as demands

# Register blueprint
# app.register_blueprint(process)
app.register_blueprint(sf)
app.register_blueprint(products)
# app.register_blueprint(demands)