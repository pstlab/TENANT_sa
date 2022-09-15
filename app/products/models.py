# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# Define a product model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    # ManyToOne
    product_family_id = Column(Integer, ForeignKey('product_families.id', use_alter=True))
    product_family = relationship("ProductFamily", back_populates='products')
    # OneToMay
    demands = relationship("Demand", back_populates='product')
    # OneToMany
    processes = relationship("Process", back_populates='product')
    # OneToMany
    functions = relationship("Function", back_populates='target_product')

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def __str__(self):
        return self.name

#Define a product family model
class ProductFamily(Base):
    __tablename__ = 'product_families'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    # OneToMany
    products = relationship("Product", back_populates='product_family')
    # OneToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='product_family')

    def __repr__(self):
        return '<Product Family %r>' % (self.name)

    def __str__(self):
        return self.name