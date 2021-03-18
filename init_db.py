from app.database import SessionLocal, engine

from app.shopfloor import models as sf_mod
from app.products import models as prod_mod
from app.demands import models as dem_mod

db = SessionLocal()

#drop and recreate all the tables
sf_mod.Base.metadata.drop_all(bind=engine)
prod_mod.Base.metadata.drop_all(bind=engine)
dem_mod.Base.metadata.drop_all(bind=engine)

sf_mod.Base.metadata.create_all(bind=engine)
prod_mod.Base.metadata.create_all(bind=engine)
dem_mod.Base.metadata.create_all(bind=engine)

#resources
r1 = sf_mod.Resource(name = 'blueCube')
r2 = sf_mod.Resource(name = 'orangeCube')
r3 = sf_mod.Resource(name = 'whiteCube')

r4 = sf_mod.Resource(name = 'Human Operator')
r5 = sf_mod.Resource(name = 'Cobot')

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

#demand
d1 = dem_mod.Demand(name = 'Mosaic', quantity = 1, product = p1)

#add all
db.add_all([r1, r2, r3, r4, r5, ar1, ar2])
db.add_all([p1, p2, p3, p4, p5, p6, pf1])
db.add(d1)

#commit and close
db.commit()
db.close()
