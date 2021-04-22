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

#resources
r1 = sf_mod.Resource(name = 'blueCube', typeRes='Tool')
r2 = sf_mod.Resource(name = 'orangeCube', typeRes='Tool')
r3 = sf_mod.Resource(name = 'whiteCube', typeRes='Tool')

r4 = sf_mod.Resource(name = 'Human Operator', typeRes='Operator')
r5 = sf_mod.Resource(name = 'Cobot', typeRes='Operator')

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
c1 = proc_mod.ComplexTask(name='DoRow1')
c2 = proc_mod.ComplexTask(name='DoRow2')
c3 = proc_mod.ComplexTask(name='DoRow3')
c4 = proc_mod.ComplexTask(name='DoRow4')
c5 = proc_mod.ComplexTask(name='DoRow5')
c12 = proc_mod.ComplexTask(name='two', parent=c1)

c11 = proc_mod.ComplexTask(name='DoCellA1')
c21 = proc_mod.ComplexTask(name='DoCellA2')
c31 = proc_mod.ComplexTask(name='DoCellA3')
c41 = proc_mod.ComplexTask(name='DoCellA4')
c51 = proc_mod.ComplexTask(name='DoCellA5')

#simple tasks
s1 = proc_mod.SimpleTask(name='one', modality='Independent', parent=c2)
s2 = proc_mod.SimpleTask(name='two', modality='Supportive', parent=c1)

#process
procM = proc_mod.Process(name='Do mosaic', product=p1, complex_tasks = [c1, c2, c3, c4, c5], simple_tasks = [s1, s2])
procR = proc_mod.Process(name='Do Row', product=p2, complex_tasks = [c11, c21, c31, c41, c51])

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
