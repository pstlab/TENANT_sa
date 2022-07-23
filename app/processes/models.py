# Import the database object (db)
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table, null
from sqlalchemy.orm import relationship

from app.database import Base

#costants
MODALITIES = ("Independent", "Simultaneous", "Sequential", "Supportive")
TYPES_OF_TASKS = ('ConjunctiveTask', 'DisjunctiveTask', 'SimpleTask')

# Define a process model
class Process(Base):
    """
    A class used to represent a process

    Attributes
    ----------
    name : str ----- the name of the process
    product : Product ----- the product to which the process refers
    tasks_list : Task[] ----- the list of tasks involved in the process
    constraints : Constraint[] ----- the list of constraints involved in the process
    """
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)

    # ManyToOne
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates='processes')
    # OneToOne
    product_family = relationship("ProductFamily", uselist=False, back_populates='process')
    # OneToMany
    tasks_list = relationship("Task", back_populates='process', cascade="all, delete-orphan")
    # OneToMany
    constraints = relationship("Constraint", back_populates='process')

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Process %r>' % (self.name)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=False)

    # ManyToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='tasks_list')
    
    # ManyToOne
    parent_id = Column(Integer, ForeignKey('tasks.id'))
    parent = relationship('Task')

    # two OneToMany
    constraint1 = relationship("Constraint", back_populates='t1', foreign_keys='Constraint.t1_id')
    constraint2 = relationship("Constraint", back_populates='t2', foreign_keys='Constraint.t2_id')
    
    typeTask = Column(Enum(*TYPES_OF_TASKS))

    __mapper_args__ = {
        'polymorphic_identity':'tasks',
        'polymorphic_on': typeTask
    }

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.typeTask = kwargs.get('typeTask')
        if kwargs.get('parent'):
            self.parent_id = kwargs.get('parent').id

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Task %r>' % (self.name)

class ComplexTask(Task):
    __tablename__ = 'complex_tasks'
    id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    
    def __init__(self, **kwargs):
        super(ComplexTask, self).__init__(**kwargs)

class ConjunctiveTask(ComplexTask):
    """
    A class used to represent a (complex) conjunctive task

    Attributes
    ----------
    name : str ----- the name of the task
    parent : ComplexTask ----- the task from which this derives in the hierarchy
    """

    __tablename__ = 'conjunctive_tasks'

    id = Column(Integer, ForeignKey('complex_tasks.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'ConjunctiveTask',
    }

    def __init__(self, **kwargs):
        super(ConjunctiveTask, self).__init__(typeTask='ConjunctiveTask', **kwargs)

class DisjunctiveTask(ComplexTask):
    """
    A class used to represent a (complex) disjunctive task

    Attributes
    ----------
    name : str ----- the name of the task
    parent : ComplexTask ----- the task from which this derives in the hierarchy
    """

    __tablename__ = 'disjunctive_tasks'

    id = Column(Integer, ForeignKey('complex_tasks.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'DisjunctiveTask',
    }

    def __init__(self, **kwargs):
        super(DisjunctiveTask, self).__init__(typeTask='DisjunctiveTask', **kwargs)

class SimpleTask(Task):
    """
    A class used to represent a simple task

    Attributes
    ----------
    name : str ----- the name of the task
    parent : ComplexTask ----- the task from which this derives in the hierarchy
    modality : str ----- the collaborative modality of the task
    f1: Function ----- the first function needed to execute the task
    f2: Function ----- the second function needed to execute the task
    """

    __tablename__ = 'simple_tasks'

    id = Column(Integer, ForeignKey('tasks.id'), primary_key=True, index=True)
    modality = Column(Enum(*MODALITIES), nullable=False)
    # two relationship ManyToOne
    f1_id = Column(Integer, ForeignKey('functions.id'))
    f2_id = Column(Integer, ForeignKey('functions.id'))
    f1 = relationship("Function", back_populates='simple_tasks1', foreign_keys=[f1_id])
    f2 = relationship("Function", back_populates='simple_tasks2', foreign_keys=[f2_id])

    __mapper_args__ = {
        'polymorphic_identity':'SimpleTask',
    }

    def __init__(self, **kwargs):
        self.modality = kwargs.get('modality')
        self.f1 = kwargs.get('f1')
        self.f2 = kwargs.get('f2', None)
        super(SimpleTask, self).__init__(typeTask='SimpleTask', **kwargs)

class Constraint(Base):
    """
    A class used to represent a temporal constraint

    Attributes
    ----------
    t1: Task ----- the first task involved
    t2: Task ----- the second task involved
    """

    __tablename__ = "constraints"
    id = Column(Integer, primary_key=True, index=True)

    # ManyToOne
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship("Process", back_populates='constraints')
    # two relationship ManyToOne
    t1_id = Column(Integer, ForeignKey('tasks.id'))
    t2_id = Column(Integer, ForeignKey('tasks.id'))
    t1 = relationship("Task", back_populates='constraint1', foreign_keys=[t1_id])
    t2 = relationship("Task", back_populates='constraint2', foreign_keys=[t2_id])

    def __str__(self):
        return self.name
    def __repr__(self):
        return '<Constraint %r>' % (self.name)
