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
    # OneToMany
    complex_tasks = relationship("ComplexTask", back_populates='process', cascade="all, delete-orphan")
    #TODO operazioni

    def __str__(self):
        return self.name

class ComplexTask(Base):
    __tablename__ = 'complex_tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=False)

    # ManyToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='complex_tasks')

    # OneToMany with other complex tasks
    parent_id = Column(Integer, ForeignKey('complex_tasks.id'))
    parent = relationship('ComplexTask', remote_side=[id], back_populates='children')
    children = relationship('ComplexTask', back_populates='parent', cascade="all, delete-orphan")

    # OneToMany
    #simpleTasks = relationship("SimpleTask", back_populates='complexTask')

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Complex Task %r>' % (self.name)