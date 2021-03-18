from app.database import SessionLocal, engine

from app.shopfloor import models as sf_mod
from app.products import models as prod_mod

db = SessionLocal()

#drop and recreate all the tables
sf_mod.Base.metadata.drop_all(bind=engine)
prod_mod.Base.metadata.drop_all(bind=engine)

sf_mod.Base.metadata.create_all(bind=engine)
prod_mod.Base.metadata.create_all(bind=engine)

#resources
r1 = sf_mod.Resource(name = 'blueCube')
r2 = sf_mod.Resource(name = 'orangeCube')
r3 = sf_mod.Resource(name = 'whiteCube')

r4 = sf_mod.Resource(name = 'Human Operator')
r5 = sf_mod.Resource(name = 'Cobot')

#aggregate resources

#products
p1 = prod_mod.Product(name = 'Mosaico')


#add all
db.add_all([r1, r2, r3, r4, r5])

db.add_all([p1])

#commit and close
db.commit()
db.close()
