# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from app.database import Base

association_table = Table('resources_functions', Base.metadata,
    Column('resources_id', Integer, ForeignKey('resources.id')),
    Column('functions_id', Integer, ForeignKey('functions.id'))
)

# Define a general resource model
class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)
    typeRes = Column(Enum('Tool', 'Operator', 'AGV'))
    
    #capacity

    # ManyToOne
    aggregate_resource_id = Column(Integer, ForeignKey('aggregate_resources.id'))
    aggregate_resource = relationship("AggregateResource", back_populates='resources')

    # ManyToMany
    functions = relationship("Function", secondary=association_table, back_populates='resource')

    def __repr__(self):
        return '<Resource %r>' % (self.name)

    def __str__(self):
        return self.name

# Define an aggregate resource 
class AggregateResource(Base):
    __tablename__ = 'aggregate_resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    # OneToMany
    resources = relationship("Resource", back_populates='aggregate_resource')

    def __repr__(self):
        return '< Aggregate Resource %r>' % (self.name)

    def __str__(self):
        return self.name
    
class Function(Base):
    __tablename__ = 'functions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)
    
    # ManyToMany
    resource = relationship("Resource", secondary=association_table, back_populates='functions')
    # OneToMany
    simple_tasks1 = relationship("SimpleTask", back_populates='f1', foreign_keys='SimpleTask.f1_id')
    simple_tasks2 = relationship("SimpleTask", back_populates='f2', foreign_keys='SimpleTask.f2_id')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name