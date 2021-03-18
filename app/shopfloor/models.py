# Import the database object (db)
from sqlalchemy import Column, Integer, String

from app.database import Base

# Define a general resource model
class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128),  nullable=False, unique=True)

    #isATool
    #isAnOperator
    
    #capacity

    #relationship with aggregate resources
    #relationship with some functions
    #db.relationship('Nome', backref='name_table' ...)

    def __repr__(self):
        return '<Resource %r>' % (self.name)

    def __str__(self):
        return self.name
