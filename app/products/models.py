# Import the database object (db)
from app import db

# Define a product model
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False, unique=True)

    #relationship with Demands
    #relationship with product family
    #relationship with process
    #db.relationship('Nome', backref='name_table' ...)

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def __str__(self):
        return self.name

#Define a product family model
class ProductFamily(db.Model):
    __tablename__ = 'product_families'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False, unique=True)

    #relationship with product
    #relationship with process
    #db.relationship('Nome', backref='name_table' ...)

    def __repr__(self):
        return '<Product Family %r>' % (self.name)

    def __str__(self):
        return self.name