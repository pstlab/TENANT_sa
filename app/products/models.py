# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# Define a product model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    product_family_id = Column(Integer, ForeignKey('product_families.id'))
    product_family = relationship("ProductFamily", back_populates='products')

    demands = relationship("Demand", back_populates='product')
    #TODO relationship with process

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def __str__(self):
        return self.name

#Define a product family model
class ProductFamily(Base):
    __tablename__ = 'product_families'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    products = relationship("Product", back_populates='product_family')
    #TODO relationship with process

    def __repr__(self):
        return '<Product Family %r>' % (self.name)

    def __str__(self):
        return self.name