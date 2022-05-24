# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from app.database import Base

TYPES_OF_RESOURCES = ('EnvironmentSensor', 'Machine', 'Tool', 'CapacityResource',
                      'Worker', 'Cobot',
                      'ProductionObject', 'WorkPiece') #Those two are probably products



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
        self.capacity = kwargs.get('capacity')


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

#Define the model of a resource of type machine
class Machine(Resource):
    __tablename__ = 'machine'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    #functions

    __mapper_args__ = {
        'polymorphic_identity':'Machine',
    }

#Define the model of a resource of type tool
class Tool(Resource):
    __tablename__ = 'tool'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Tool',
    }

#Define the model of a resource of type capacity resource
class CapacityResource(Resource):
    __tablename__ = 'capacityResource'
    id = Column(Integer, ForeignKey('resources.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'CapacityResource',
    }


   ###     ######   ######     ########    ###    ########  ##       ########  ######  
  ## ##   ##    ## ##    ##       ##      ## ##   ##     ## ##       ##       ##    ## 
 ##   ##  ##       ##             ##     ##   ##  ##     ## ##       ##       ##       
##     ##  ######   ######        ##    ##     ## ########  ##       ######    ######  
#########       ##       ##       ##    ######### ##     ## ##       ##             ## 
##     ## ##    ## ##    ##       ##    ##     ## ##     ## ##       ##       ##    ## 
##     ##  ######   ######        ##    ##     ## ########  ######## ########  ######  

association_table = Table('agent_functions', Base.metadata,
    Column('agent_id', Integer, ForeignKey('agent.id')),
    Column('functions_id', Integer, ForeignKey('functions.id'))
)

   ###     ######  ######## #### ##    ##  ######      ######## ##    ## ######## #### ######## #### ########  ######  
  ## ##   ##    ##    ##     ##  ###   ## ##    ##     ##       ###   ##    ##     ##     ##     ##  ##       ##    ## 
 ##   ##  ##          ##     ##  ####  ## ##           ##       ####  ##    ##     ##     ##     ##  ##       ##       
##     ## ##          ##     ##  ## ## ## ##   ####    ######   ## ## ##    ##     ##     ##     ##  ######    ######  
######### ##          ##     ##  ##  #### ##    ##     ##       ##  ####    ##     ##     ##     ##  ##             ## 
##     ## ##    ##    ##     ##  ##   ### ##    ##     ##       ##   ###    ##     ##     ##     ##  ##       ##    ## 
##     ##  ######     ##    #### ##    ##  ######      ######## ##    ##    ##    ####    ##    #### ########  ######  

# Define the model of a resource of type agent
class Agent(Resource):
    __tablename__ = 'agent'
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)

    # ManyToMany
    functions = relationship("Function", secondary=association_table, back_populates='agent')

    def __init__(self, **kwargs):
        self.functions = kwargs.get('functions')
        super(Agent, self).__init__(**kwargs)


class Worker(Agent):
    __tablename__ = 'worker'
    id = Column(Integer, ForeignKey('agent.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Worker'
    }

class Cobot(Agent):
    __tablename__ = 'cobot'
    id = Column(Integer, ForeignKey('agent.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Cobot'
    }


######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######  
##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ## 
##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##       
######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######  
##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ## 
##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ## 
##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######  

class Function(Base):
    __tablename__ = 'functions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)
    
    # ManyToMany
    agent = relationship("Agent", secondary=association_table, back_populates='functions')
    # OneToMany
    simple_tasks1 = relationship("SimpleTask", back_populates='f1', foreign_keys='SimpleTask.f1_id')
    simple_tasks2 = relationship("SimpleTask", back_populates='f2', foreign_keys='SimpleTask.f2_id')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name