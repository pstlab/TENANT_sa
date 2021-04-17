# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base

#costanti
# IND = "Independent"
# SYN = "Synchronous"
# SIM = "Simultaneous"
# SUPP = "Supportive"

# Define a process model
class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)

    # ManyToOne
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates='processes')
    # OneToOne
    product_family = relationship("ProductFamily", uselist=False, back_populates='process')

    #TODO operazioni