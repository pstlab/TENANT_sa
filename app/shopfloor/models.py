# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base

# Define a general resource model
class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)
    typeRes = Column(Enum('Tool', 'Operator', 'AGV'))
    
    #capacity

    aggregate_resource_id = Column(Integer, ForeignKey('aggregate_resources.id'))
    aggregate_resource = relationship("AggregateResource", back_populates='resources')
    #TODO relationship with some functions

    def __repr__(self):
        return '<Resource %r>' % (self.name)

    def __str__(self):
        return self.name

# Define an aggregate resource 
class AggregateResource(Base):
    __tablename__ = 'aggregate_resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    resources = relationship("Resource", back_populates='aggregate_resource')

    def __repr__(self):
        return '< Aggregate Resource %r>' % (self.name)

    def __str__(self):
        return self.name
    
