# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base

# Define a demand model
class Demand(Base):
    __tablename__ = 'demands'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    quantity = Column(Integer)
    typeDem = Column(Enum('CustomerOrder', 'EngineeringWorkOrder', 'StockOrder'))
    
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates='demands')

    #TODO relationship col processo
