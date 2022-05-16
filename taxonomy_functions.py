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
f1 = sf_mod.Function(name = 'Pick Object')
f2 = sf_mod.Function(name = 'Place Object')
f3 = sf_mod.Function(name = 'PickAndPlace Object')
f4 = sf_mod.Function(name = 'Screw')
f5 = sf_mod.Function(name = 'Unscrew')
f6 = sf_mod.Function(name = 'Assemble')
f7 = sf_mod.Function(name = 'Disassemble')
f8 = sf_mod.Function(name = 'Manual Guidance')
f9 = sf_mod.Function(name = 'Motion')
f10 = sf_mod.Function(name = 'Move/Navigate')
f11 = sf_mod.Function(name = 'Weld')
f12 = sf_mod.Function(name = 'Inspect')

#add all
db.add_all([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12])

#commit and close
db.commit()
db.close()
