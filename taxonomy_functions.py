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

#capabilities
c1 = sf_mod.Capability(name = 'Pick Object')
c2 = sf_mod.Capability(name = 'Place Object')
c3 = sf_mod.Capability(name = 'PickAndPlace Object')
c4 = sf_mod.Capability(name = 'Screw')
c5 = sf_mod.Capability(name = 'Unscrew')
c6 = sf_mod.Capability(name = 'Assemble')
c7 = sf_mod.Capability(name = 'Disassemble')
c8 = sf_mod.Capability(name = 'Manual Guidance')
c9 = sf_mod.Capability(name = 'Motion')
c10 = sf_mod.Capability(name = 'Move/Navigate')
c11 = sf_mod.Capability(name = 'Weld')
c12 = sf_mod.Capability(name = 'Inspect')

#add all
db.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12])

#commit and close
db.commit()
db.close()
