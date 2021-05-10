# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
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
    # OneToMany
    simple_tasks = relationship("SimpleTask", back_populates='process', cascade='all, delete-orphan')
    # OneToMany
    constraints = relationship("Constraint", back_populates='process')

    def __str__(self):
        return self.name

class ComplexTask(Base):
    __tablename__ = 'complex_tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=False)
    typeTask = Column(Enum('Conjunctive', 'Disjunctive'))

    # ManyToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='complex_tasks')
    # OneToMany with other complex tasks
    parent_id = Column(Integer, ForeignKey('complex_tasks.id'))
    parent = relationship('ComplexTask', remote_side=[id], back_populates='children')
    children = relationship('ComplexTask', back_populates='parent', cascade="all, delete-orphan")
    # OneToMany
    simple_tasks = relationship("SimpleTask", back_populates='parent', cascade="all, delete-orphan")
    # two OneToMany
    complex_constraint1 = relationship("Constraint", back_populates='tc1', foreign_keys='Constraint.tc1_id')
    complex_constraint2 = relationship("Constraint", back_populates='tc2', foreign_keys='Constraint.tc2_id')

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Complex Task %r>' % (self.name)

class SimpleTask(Base):
    __tablename__ = 'simple_task'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=False)
    modality = Column(Enum('Independent', 'Synchronous', 'Simultaneous', 'Supportive'), nullable=False)

    # ManyToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='simple_tasks')
    # ManyToOne
    parent_id = Column(Integer, ForeignKey('complex_tasks.id'))
    parent = relationship("ComplexTask", back_populates='simple_tasks')
    # two relationship ManyToOne
    f1_id = Column(Integer, ForeignKey('functions.id'))
    f2_id = Column(Integer, ForeignKey('functions.id'))
    f1 = relationship("Function", back_populates='simple_tasks1', foreign_keys=[f1_id])
    f2 = relationship("Function", back_populates='simple_tasks2', foreign_keys=[f2_id])
    # two OneToMany
    simple_constraint1 = relationship("Constraint", back_populates='ts1', foreign_keys='Constraint.ts1_id')
    simple_constraint2 = relationship("Constraint", back_populates='ts2', foreign_keys='Constraint.ts2_id')

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Simple Task %r>' % (self.name)

class Constraint(Base):
    __tablename__ = "constraints"
    id = Column(Integer, primary_key=True, index=True)

    # ManyToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='constraints')
    # two relationship ManyToOne for complexTasks
    tc1_id = Column(Integer, ForeignKey('complex_tasks.id'))
    tc2_id = Column(Integer, ForeignKey('complex_tasks.id'))
    tc1 = relationship("ComplexTask", back_populates='complex_constraint1', foreign_keys=[tc1_id])
    tc2 = relationship("ComplexTask", back_populates='complex_constraint2', foreign_keys=[tc2_id])
    # two relationship ManyToOne for simpleTasks
    ts1_id = Column(Integer, ForeignKey('simple_task.id'))
    ts2_id = Column(Integer, ForeignKey('simple_task.id'))
    ts1 = relationship("SimpleTask", back_populates='simple_constraint1', foreign_keys=[ts1_id])
    ts2 = relationship("SimpleTask", back_populates='simple_constraint2', foreign_keys=[ts2_id])

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Constraint %r>' % (self.name)
