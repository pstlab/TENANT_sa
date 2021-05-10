from app.database import SessionLocal, engine

from app.shopfloor import models as sf_mod
from app.products import models as prod_mod
from app.demands import models as dem_mod
from app.processes import models as proc_mod

db = SessionLocal()

#drop and recreate all the tables
sf_mod.Base.metadata.drop_all(bind=engine)
prod_mod.Base.metadata.drop_all(bind=engine)
dem_mod.Base.metadata.drop_all(bind=engine)
proc_mod.Base.metadata.drop_all(bind=engine)

sf_mod.Base.metadata.create_all(bind=engine)
prod_mod.Base.metadata.create_all(bind=engine)
dem_mod.Base.metadata.create_all(bind=engine)
proc_mod.Base.metadata.create_all(bind=engine)


#functions
f1 = sf_mod.Function(name = 'PickAndPlace Blue')
f2 = sf_mod.Function(name = 'PickAndPlace Orange')
f3 = sf_mod.Function(name = 'PickAndPlace White')

#resources
r1 = sf_mod.Resource(name = 'Blue cube', typeRes='Tool')
r2 = sf_mod.Resource(name = 'Orange cube', typeRes='Tool')
r3 = sf_mod.Resource(name = 'White cube', typeRes='Tool')

r4 = sf_mod.Resource(name = 'Human Operator', typeRes='Operator', functions = [f1, f3])
r5 = sf_mod.Resource(name = 'Cobot', typeRes='Operator', functions = [f1, f2])

#aggregate resources
ar1 = sf_mod.AggregateResource(name = 'Station 1', resources = [r2, r5])
ar2 = sf_mod.AggregateResource(name = 'Station 2', resources = [r3, r4])

#products
p1 = prod_mod.Product(name = 'Mosaico')

p2 = prod_mod.Product(name = 'Row 1')
p3 = prod_mod.Product(name = 'Row 2')
p4 = prod_mod.Product(name = 'Row 3')
p5 = prod_mod.Product(name = 'Row 4')
p6 = prod_mod.Product(name = 'Row 5')

#product families
pf1 = prod_mod.ProductFamily(name = 'Rows', products = [p2, p3, p4, p5, p6])

#complex tasks
c1 = proc_mod.ComplexTask(name='Do Row 1', typeTask='Conjunctive')
c2 = proc_mod.ComplexTask(name='Do Row 2', typeTask='Conjunctive')
c3 = proc_mod.ComplexTask(name='Do Row 3', typeTask='Conjunctive')
c4 = proc_mod.ComplexTask(name='Do Row 4', typeTask='Conjunctive')
c5 = proc_mod.ComplexTask(name='Do Row 5', typeTask='Conjunctive')
#c12 = proc_mod.ComplexTask(name='two', parent=c1)

# c11 = proc_mod.ComplexTask(name='Do Cell A1')
# c21 = proc_mod.ComplexTask(name='Do Cell A2')
# c31 = proc_mod.ComplexTask(name='Do Cell A3')
# c41 = proc_mod.ComplexTask(name='Do Cell A4')
# c51 = proc_mod.ComplexTask(name='Do Cell A5')

#simple tasks
# s1 = proc_mod.SimpleTask(name='one', modality='Independent', parent=c2, f1=f1, f2=f2)
# s2 = proc_mod.SimpleTask(name='two', modality='Supportive', parent=c1)

s11 = proc_mod.SimpleTask(name='Do Cell A1', modality='Independent', parent=c1, f1=f2)
s12 = proc_mod.SimpleTask(name='Do Cell B1', modality='Independent', parent=c1, f1=f2)
s13 = proc_mod.SimpleTask(name='Do Cell C1', modality='Independent', parent=c1, f1=f2)
s14 = proc_mod.SimpleTask(name='Do Cell D1', modality='Independent', parent=c1, f1=f1)
s15 = proc_mod.SimpleTask(name='Do Cell E1', modality='Independent', parent=c1, f1=f3)

#constraints
con1 = proc_mod.Constraint(tc1=c1, tc2=c3)
con2 = proc_mod.Constraint(tc1=c1, tc2=c4)
con3 = proc_mod.Constraint(tc1=c2, tc2=c4)
con4 = proc_mod.Constraint(tc1=c1, tc2=c5)
con5 = proc_mod.Constraint(tc1=c2, tc2=c5)
con6 = proc_mod.Constraint(tc1=c3, tc2=c5)

#process
procM = proc_mod.Process(name='Do Mosaic', product=p1,
            complex_tasks = [c1, c2, c3, c4, c5], simple_tasks = [s11, s12, s13, s14],
            constraints = [con1, con2, con3, con4, con5, con6])
procR = proc_mod.Process(name='Do Row', product=p2)
#procR1 = proc_mod.Process(name='Do Row 1', product=p2, simple_tasks = [s11, s12, s13, s14, s15])

#demand
d1 = dem_mod.Demand(name = 'Mosaic', quantity = 1, product = p1, typeDem='StockOrder', process=procM)

#add all
db.add_all([r1, r2, r3, r4, r5, ar1, ar2])
db.add_all([p1, p2, p3, p4, p5, p6, pf1])
db.add_all([procM, procR])
db.add(d1)

#commit and close
db.commit()
db.close()
