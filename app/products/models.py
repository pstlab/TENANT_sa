# Import the database object (db)
from sqlalchemy import Column, Integer, String

from app.database import Base

# Define a product model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    #relationship with Demands
    #relationship with product family
    #relationship with process
    #db.relationship('Nome', backref='name_table' ...)

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def __str__(self):
        return self.name

#Define a product family model
class ProductFamily(Base):
    __tablename__ = 'product_families'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    #relationship with product
    #relationship with process
    #db.relationship('Nome', backref='name_table' ...)

    def __repr__(self):
        return '<Product Family %r>' % (self.name)

    def __str__(self):
        return self.name