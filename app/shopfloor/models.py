# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from app.database import Base

TYPES_OF_RESOURCES = ('EnvironmentSensor', 'Machine', 'Tool', 'CapacityResource',
                      'Worker', 'Cobot',
                      'ProductionObject')



   ###     ######    ######   ########  ########  ######      ###    ######## ######## 
  ## ##   ##    ##  ##    ##  ##     ## ##       ##    ##    ## ##      ##    ##       
 ##   ##  ##        ##        ##     ## ##       ##         ##   ##     ##    ##       
##     ## ##   #### ##   #### ########  ######   ##   #### ##     ##    ##    ######   
######### ##    ##  ##    ##  ##   ##   ##       ##    ##  #########    ##    ##       
##     ## ##    ##  ##    ##  ##    ##  ##       ##    ##  ##     ##    ##    ##       
##     ##  ######    ######   ##     ## ########  ######   ##     ##    ##    ######## 

# Define an aggregate resource 
class AggregateResource(Base):
    __tablename__ = 'aggregate_resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    # OneToMany
    resources = relationship("Resource", back_populates='aggregate_resource')
    # OneToMany with other aggregate resources
    parent_id = Column(Integer, ForeignKey('aggregate_resources.id'))
    parent = relationship('AggregateResource', remote_side=[id], back_populates='children')
    children = relationship('AggregateResource', back_populates='parent')
    

    def __repr__(self):
        return '< Aggregate Resource %r>' % (self.name)

    def __str__(self):
        return self.name    


########  ########  ######   #######  ##     ## ########   ######  ########  ######  
##     ## ##       ##    ## ##     ## ##     ## ##     ## ##    ## ##       ##    ## 
##     ## ##       ##       ##     ## ##     ## ##     ## ##       ##       ##       
########  ######    ######  ##     ## ##     ## ########  ##       ######    ######  
##   ##   ##             ## ##     ## ##     ## ##   ##   ##       ##             ## 
##    ##  ##       ##    ## ##     ## ##     ## ##    ##  ##    ## ##       ##    ## 
##     ## ########  ######   #######   #######  ##     ##  ######  ########  ######  

# Define a general resource model
class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)
    typeRes = Column(Enum(*TYPES_OF_RESOURCES))
    __mapper_args__ = {
        'polymorphic_identity':'resources',
        'polymorphic_on': typeRes
    }
    
    description = Column(String)
    capacity=Column(Integer)

    # PartOf relationship
    # ManyToOne
    aggregate_resource_id = Column(Integer, ForeignKey('aggregate_resources.id'))
    aggregate_resource = relationship("AggregateResource", back_populates='resources')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.typeRes = kwargs.get('typeRes')
        self.description = kwargs.get('description')
        self.capacity = kwargs.get('capacity') or 1
        self.aggregate_resource = kwargs.get('aggregate_resource')


    def __repr__(self):
        return '<Resource %r>' % (self.name)

    def __str__(self):
        return self.name

#Define the model of a resource of type environment sensor
class EnvironmentSensor(Resource):
    __tablename__ = 'environmentSensor'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    producingObservationOf = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'EnvironmentSensor',
    }

    def __init__(self, **kwargs):
        # self.producingObservationOf = kwargs.get('producingObservationOf')
        super(EnvironmentSensor, self).__init__(typeRes='EnvironmentSensor', **kwargs)

#Define the model of a resource of type machine
class Machine(Resource):
    __tablename__ = 'machine'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    #functions

    __mapper_args__ = {
        'polymorphic_identity':'Machine',
    }

    def __init__(self, **kwargs):
        super(Machine, self).__init__(typeRes='Machine', **kwargs)


#Define the model of a resource of type tool
class Tool(Resource):
    __tablename__ = 'tool'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Tool',
    }

    def __init__(self, **kwargs):
        super(Tool, self).__init__(typeRes='Tool', **kwargs)

#Define the model of a resource of type capacity resource
class CapacityResource(Resource):
    __tablename__ = 'capacityResource'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'CapacityResource',
    }

    def __init__(self, **kwargs):
        super(CapacityResource, self).__init__(typeRes='CapacityResource', **kwargs)

#Define the model of a resource of type production object
class ProductionObject(Resource):
    __tablename__ = 'productionObjects'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'ProductionObject',
    }

    def __init__(self, **kwargs):
        super(ProductionObject, self).__init__(typeRes='ProductionObject', **kwargs)


   ###     ######   ######     ########    ###    ########  ##       ########  ######  
  ## ##   ##    ## ##    ##       ##      ## ##   ##     ## ##       ##       ##    ## 
 ##   ##  ##       ##             ##     ##   ##  ##     ## ##       ##       ##       
##     ##  ######   ######        ##    ##     ## ########  ##       ######    ######  
#########       ##       ##       ##    ######### ##     ## ##       ##             ## 
##     ## ##    ## ##    ##       ##    ##     ## ##     ## ##       ##       ##    ## 
##     ##  ######   ######        ##    ##     ## ########  ######## ########  ######  

association_table = Table('agent_capabilities', Base.metadata,
    Column('agent_id', Integer, ForeignKey('agent.id')),
    Column('capabilities_id', Integer, ForeignKey('capabilities.id'))
)

   ###     ######  ######## #### ##    ##  ######      ######## ##    ## ######## #### ######## #### ########  ######  
  ## ##   ##    ##    ##     ##  ###   ## ##    ##     ##       ###   ##    ##     ##     ##     ##  ##       ##    ## 
 ##   ##  ##          ##     ##  ####  ## ##           ##       ####  ##    ##     ##     ##     ##  ##       ##       
##     ## ##          ##     ##  ## ## ## ##   ####    ######   ## ## ##    ##     ##     ##     ##  ######    ######  
######### ##          ##     ##  ##  #### ##    ##     ##       ##  ####    ##     ##     ##     ##  ##             ## 
##     ## ##    ##    ##     ##  ##   ### ##    ##     ##       ##   ###    ##     ##     ##     ##  ##       ##    ## 
##     ##  ######     ##    #### ##    ##  ######      ######## ##    ##    ##    ####    ##    #### ########  ######  

# Define the model of a resource of type agent
class _Agent(Resource):
    __tablename__ = 'agent'
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)

    # ManyToMany
    capabilities = relationship("Capability", secondary=association_table, back_populates='agent')

    def __init__(self, **kwargs):
        self.capabilities = kwargs.get('capabilities')
        super(_Agent, self).__init__(**kwargs)


class Worker(_Agent):
    """
    A class used to represent a human worker

    Attributes
    ----------
    name : str ----- the name of the worker
    description : str ----- a brief description (default None)
    capacity : int ----- capacity of the agent (default 1)
    aggregate resource : AggregateResource ----- the aggregate resource of which the agent is part of (default None)
    capabilities : list of Capability ----- the list of capabilities the agent can perform
    """

    __tablename__ = 'worker'
    id = Column(Integer, ForeignKey('agent.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Worker'
    }

    def __init__(self, **kwargs):
        super(Worker, self).__init__(typeRes='Worker', **kwargs)

class Cobot(_Agent):
    """
    A class used to represent a collaborative robot

    Attributes
    ----------
    name : str ----- the name of the worker
    description : str ----- a brief description (default None)
    capacity : int ----- capacity of the agent (default 1)
    aggregate resource : AggregateResource ----- the aggregate resource of which the agent is part of (default None)
    capabilities : list of Capability ----- the list of capabilities the agent can perform
    """

    __tablename__ = 'cobot'
    id = Column(Integer, ForeignKey('agent.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Cobot'
    }

    def __init__(self, **kwargs):
        super(Cobot, self).__init__(typeRes='Cobot', **kwargs)


 ######     ###    ########     ###    ########  #### ##       #### ######## #### ########  ######  
##    ##   ## ##   ##     ##   ## ##   ##     ##  ##  ##        ##     ##     ##  ##       ##    ## 
##        ##   ##  ##     ##  ##   ##  ##     ##  ##  ##        ##     ##     ##  ##       ##       
##       ##     ## ########  ##     ## ########   ##  ##        ##     ##     ##  ######    ######  
##       ######### ##        ######### ##     ##  ##  ##        ##     ##     ##  ##             ## 
##    ## ##     ## ##        ##     ## ##     ##  ##  ##        ##     ##     ##  ##       ##    ## 
 ######  ##     ## ##        ##     ## ########  #### ######## ####    ##    #### ########  ######  


class Capability(Base):
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)
    
    # ManyToMany
    agent = relationship("_Agent", secondary=association_table, back_populates='capabilities')

    def __repr__(self):
        return '< Capability %r>' %(self.name)

    def __str__(self):
        return self.name