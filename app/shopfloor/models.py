# Import the database object (db)
from app import db

# Define a general resource model
class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False, unique=True)

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
