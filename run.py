# Run a test server.
from app import app
from app.database import engine

from app.shopfloor import models as sf_mod
from app.products import models as prod_mod

sf_mod.Base.metadata.create_all(bind=engine)
prod_mod.Base.metadata.create_all(bind=engine)

app.run()