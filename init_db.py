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
r1 = sf_mod.Tool(name = 'Blue cube')
r2 = sf_mod.Tool(name = 'Orange cube')
r3 = sf_mod.Tool(name = 'White cube')

r4 = sf_mod.Worker(name = 'Human Operator', functions = [f1, f3])
r5 = sf_mod.Cobot(name = 'Cobot', functions = [f1, f2])

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
c1 = proc_mod.ConjunctiveTask(name='Do Row 1')
c2 = proc_mod.ConjunctiveTask(name='Do Row 2')
c3 = proc_mod.ConjunctiveTask(name='Do Row 3')
c4 = proc_mod.ConjunctiveTask(name='Do Row 4')
c5 = proc_mod.ConjunctiveTask(name='Do Row 5')

c10 = proc_mod.ConjunctiveTask(name='Do Cell A1', parent=c1)
c11 = proc_mod.ConjunctiveTask(name='Do Cell B1', parent=c1)
c12 = proc_mod.ConjunctiveTask(name='Do Cell C1', parent=c1)
c13 = proc_mod.DisjunctiveTask(name='Do Cell D1', parent=c1)
c14 = proc_mod.ConjunctiveTask(name='Do Cell E1', parent=c1)
c15 = proc_mod.DisjunctiveTask(name='Do Cell F1', parent=c1)
c16 = proc_mod.DisjunctiveTask(name='Do Cell G1', parent=c1)
c17 = proc_mod.DisjunctiveTask(name='Do Cell H1', parent=c1)
c18 = proc_mod.ConjunctiveTask(name='Do Cell I1', parent=c1)
c19 = proc_mod.DisjunctiveTask(name='Do Cell J1', parent=c1)

c20 = proc_mod.ConjunctiveTask(name='Do Cell A2', parent=c2)
c21 = proc_mod.DisjunctiveTask(name='Do Cell B2', parent=c2)
c22 = proc_mod.DisjunctiveTask(name='Do Cell C2', parent=c2)
c23 = proc_mod.DisjunctiveTask(name='Do Cell D2', parent=c2)
c24 = proc_mod.ConjunctiveTask(name='Do Cell E2', parent=c2)
c25 = proc_mod.DisjunctiveTask(name='Do Cell F2', parent=c2)
c26 = proc_mod.ConjunctiveTask(name='Do Cell G2', parent=c2)
c27 = proc_mod.DisjunctiveTask(name='Do Cell H2', parent=c2)
c28 = proc_mod.ConjunctiveTask(name='Do Cell I2', parent=c2)
c29 = proc_mod.DisjunctiveTask(name='Do Cell J2', parent=c2)

c30 = proc_mod.ConjunctiveTask(name='Do Cell A3', parent=c3)
c31 = proc_mod.ConjunctiveTask(name='Do Cell B3', parent=c3)
c32 = proc_mod.ConjunctiveTask(name='Do Cell C3', parent=c3)
c33 = proc_mod.DisjunctiveTask(name='Do Cell D3', parent=c3)
c34 = proc_mod.ConjunctiveTask(name='Do Cell E3', parent=c3)
c35 = proc_mod.DisjunctiveTask(name='Do Cell F3', parent=c3)
c36 = proc_mod.ConjunctiveTask(name='Do Cell G3', parent=c3)
c37 = proc_mod.DisjunctiveTask(name='Do Cell H3', parent=c3)
c38 = proc_mod.ConjunctiveTask(name='Do Cell I3', parent=c3)
c39 = proc_mod.DisjunctiveTask(name='Do Cell J3', parent=c3)

c40 = proc_mod.DisjunctiveTask(name='Do Cell A4', parent=c4)
c41 = proc_mod.DisjunctiveTask(name='Do Cell B4', parent=c4)
c42 = proc_mod.ConjunctiveTask(name='Do Cell C4', parent=c4)
c43 = proc_mod.DisjunctiveTask(name='Do Cell D4', parent=c4)
c44 = proc_mod.DisjunctiveTask(name='Do Cell E4', parent=c4)
c45 = proc_mod.ConjunctiveTask(name='Do Cell F4', parent=c4)
c46 = proc_mod.DisjunctiveTask(name='Do Cell G4', parent=c4)
c47 = proc_mod.ConjunctiveTask(name='Do Cell H4', parent=c4)
c48 = proc_mod.DisjunctiveTask(name='Do Cell I4', parent=c4)
c49 = proc_mod.DisjunctiveTask(name='Do Cell J4', parent=c4)

c50 = proc_mod.ConjunctiveTask(name='Do Cell A5', parent=c5)
c51 = proc_mod.ConjunctiveTask(name='Do Cell B5', parent=c5)
c52 = proc_mod.ConjunctiveTask(name='Do Cell C5', parent=c5)
c53 = proc_mod.DisjunctiveTask(name='Do Cell D5', parent=c5)
c54 = proc_mod.DisjunctiveTask(name='Do Cell E5', parent=c5)
c55 = proc_mod.ConjunctiveTask(name='Do Cell F5', parent=c5)
c56 = proc_mod.DisjunctiveTask(name='Do Cell G5', parent=c5)
c57 = proc_mod.ConjunctiveTask(name='Do Cell H5', parent=c5)
c58 = proc_mod.DisjunctiveTask(name='Do Cell I5', parent=c5)
c59 = proc_mod.DisjunctiveTask(name='Do Cell J5', parent=c5)

#simple tasks of cobot
s10 = proc_mod.SimpleTask(name='Do Cell A1', modality='Independent', parent=c10, f1=f2)
s11 = proc_mod.SimpleTask(name='Do Cell B1', modality='Independent', parent=c11, f1=f2)
s12 = proc_mod.SimpleTask(name='Do Cell C1', modality='Independent', parent=c12, f1=f2)
s20 = proc_mod.SimpleTask(name='Do Cell A2', modality='Independent', parent=c20, f1=f2)
s30 = proc_mod.SimpleTask(name='Do Cell A3', modality='Independent', parent=c30, f1=f2)
s31 = proc_mod.SimpleTask(name='Do Cell B3', modality='Independent', parent=c31, f1=f2)
s32 = proc_mod.SimpleTask(name='Do Cell C3', modality='Independent', parent=c32, f1=f2)
s42 = proc_mod.SimpleTask(name='Do Cell C4', modality='Independent', parent=c42, f1=f2)
s50 = proc_mod.SimpleTask(name='Do Cell A5', modality='Independent', parent=c50, f1=f2)
s51 = proc_mod.SimpleTask(name='Do Cell B5', modality='Independent', parent=c51, f1=f2)
s52 = proc_mod.SimpleTask(name='Do Cell C5', modality='Independent', parent=c52, f1=f2)

#simple tasks of both
s13 = proc_mod.SimpleTask(name='Do Cell D1', modality='Independent', parent=c13, f1=f1)
s15 = proc_mod.SimpleTask(name='Do Cell F1', modality='Independent', parent=c15, f1=f1)
s16 = proc_mod.SimpleTask(name='Do Cell G1', modality='Independent', parent=c16, f1=f1)
s17 = proc_mod.SimpleTask(name='Do Cell H1', modality='Independent', parent=c17, f1=f1)
s19 = proc_mod.SimpleTask(name='Do Cell J1', modality='Independent', parent=c19, f1=f1)
s21 = proc_mod.SimpleTask(name='Do Cell B2', modality='Independent', parent=c21, f1=f1)
s22 = proc_mod.SimpleTask(name='Do Cell C2', modality='Independent', parent=c22, f1=f1)
s23 = proc_mod.SimpleTask(name='Do Cell D2', modality='Independent', parent=c23, f1=f1)
s25 = proc_mod.SimpleTask(name='Do Cell F2', modality='Independent', parent=c25, f1=f1)
s27 = proc_mod.SimpleTask(name='Do Cell H2', modality='Independent', parent=c27, f1=f1)
s29 = proc_mod.SimpleTask(name='Do Cell J2', modality='Independent', parent=c29, f1=f1)
s33 = proc_mod.SimpleTask(name='Do Cell D3', modality='Independent', parent=c33, f1=f1)
s35 = proc_mod.SimpleTask(name='Do Cell F3', modality='Independent', parent=c35, f1=f1)
s37 = proc_mod.SimpleTask(name='Do Cell H3', modality='Independent', parent=c37, f1=f1)
s39 = proc_mod.SimpleTask(name='Do Cell J3', modality='Independent', parent=c39, f1=f1)
s40 = proc_mod.SimpleTask(name='Do Cell A4', modality='Independent', parent=c40, f1=f1)
s41 = proc_mod.SimpleTask(name='Do Cell B4', modality='Independent', parent=c41, f1=f1)
s43 = proc_mod.SimpleTask(name='Do Cell D4', modality='Independent', parent=c43, f1=f1)
s44 = proc_mod.SimpleTask(name='Do Cell E4', modality='Independent', parent=c44, f1=f1)
s46 = proc_mod.SimpleTask(name='Do Cell G4', modality='Independent', parent=c46, f1=f1)
s48 = proc_mod.SimpleTask(name='Do Cell I4', modality='Independent', parent=c48, f1=f1)
s49 = proc_mod.SimpleTask(name='Do Cell J4', modality='Independent', parent=c49, f1=f1)
s53 = proc_mod.SimpleTask(name='Do Cell D5', modality='Independent', parent=c53, f1=f1)
s54 = proc_mod.SimpleTask(name='Do Cell E5', modality='Independent', parent=c54, f1=f1)
s56 = proc_mod.SimpleTask(name='Do Cell G5', modality='Independent', parent=c56, f1=f1)
s58 = proc_mod.SimpleTask(name='Do Cell I5', modality='Independent', parent=c58, f1=f1)
s59 = proc_mod.SimpleTask(name='Do Cell J5', modality='Independent', parent=c59, f1=f1)

#simple tasks of operator
s14 = proc_mod.SimpleTask(name='Do Cell E1', modality='Independent', parent=c14, f1=f3)
s18 = proc_mod.SimpleTask(name='Do Cell I1', modality='Independent', parent=c18, f1=f3)
s24 = proc_mod.SimpleTask(name='Do Cell E2', modality='Independent', parent=c24, f1=f3)
s26 = proc_mod.SimpleTask(name='Do Cell G2', modality='Independent', parent=c26, f1=f3)
s28 = proc_mod.SimpleTask(name='Do Cell I2', modality='Independent', parent=c28, f1=f3)
s34 = proc_mod.SimpleTask(name='Do Cell E3', modality='Independent', parent=c34, f1=f3)
s36 = proc_mod.SimpleTask(name='Do Cell G3', modality='Independent', parent=c36, f1=f3)
s38 = proc_mod.SimpleTask(name='Do Cell I3', modality='Independent', parent=c38, f1=f3)
s45 = proc_mod.SimpleTask(name='Do Cell F4', modality='Independent', parent=c45, f1=f3)
s47 = proc_mod.SimpleTask(name='Do Cell H4', modality='Independent', parent=c47, f1=f3)
s55 = proc_mod.SimpleTask(name='Do Cell F5', modality='Independent', parent=c55, f1=f3)
s57 = proc_mod.SimpleTask(name='Do Cell H5', modality='Independent', parent=c57, f1=f3)

#constraints
con1 = proc_mod.Constraint(t1=c1, t2=c3)
con2 = proc_mod.Constraint(t1=c1, t2=c4)
con3 = proc_mod.Constraint(t1=c2, t2=c4)
con4 = proc_mod.Constraint(t1=c1, t2=c5)
con5 = proc_mod.Constraint(t1=c2, t2=c5)
con6 = proc_mod.Constraint(t1=c3, t2=c5)

tl = [c1, c2, c3, c4, c5]
tl.extend([c10,c11,c12,c13,c14,c15,c16,c17,c18,c19])
tl.extend([c20,c21,c22,c23,c24,c25,c26,c27,c28,c29])
tl.extend([c30,c31,c32,c33,c34,c35,c36,c37,c38,c39])
tl.extend([c40,c41,c42,c43,c44,c45,c46,c47,c48,c49])
tl.extend([c50,c51,c52,c53,c54,c55,c56,c57,c58,c59])
tl.extend([s10,s11,s12,s13,s14,s15,s16,s17,s18,s19])
tl.extend([s20,s21,s22,s23,s24,s25,s26,s27,s28,s29])
tl.extend([s30,s31,s32,s33,s34,s35,s36,s37,s38,s39])
tl.extend([s40,s41,s42,s43,s44,s45,s46,s47,s48,s49])
tl.extend([s50,s51,s52,s53,s54,s55,s56,s57,s58,s59])

#process
procM = proc_mod.Process(name='Do Mosaic', product=p1, tasks_list = tl,
            constraints = [con1, con2, con3, con4, con5, con6])


#demand
d1 = dem_mod.Demand(name = 'Mosaic', quantity = 1, product = p1, typeDem='StockOrder', process=procM)

#add all
db.add_all([r1, r2, r3, r4, r5, ar1, ar2])
db.add_all([p1, p2, p3, p4, p5, p6, pf1])
db.add(procM)
db.add(d1)

#commit and close
db.commit()
db.close()
