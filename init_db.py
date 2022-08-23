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



 ######     ###    ########     ###    ########  #### ##       #### ######## #### ########  ######  
##    ##   ## ##   ##     ##   ## ##   ##     ##  ##  ##        ##     ##     ##  ##       ##    ## 
##        ##   ##  ##     ##  ##   ##  ##     ##  ##  ##        ##     ##     ##  ##       ##       
##       ##     ## ########  ##     ## ########   ##  ##        ##     ##     ##  ######    ######  
##       ######### ##        ######### ##     ##  ##  ##        ##     ##     ##  ##             ## 
##    ## ##     ## ##        ##     ## ##     ##  ##  ##        ##     ##     ##  ##       ##    ## 
 ######  ##     ## ##        ##     ## ########  #### ######## ####    ##    #### ########  ######  

cap1 = sf_mod.Capability(name = 'PickAndPlace Blue')
cap2 = sf_mod.Capability(name = 'PickAndPlace Orange')
cap3 = sf_mod.Capability(name = 'PickAndPlace White')

db.add_all([cap1, cap2, cap3])

 #####  ######  ####   ####  #    # #####   ####  ######  ####  
 #    # #      #      #    # #    # #    # #    # #      #      
 #    # #####   ####  #    # #    # #    # #      #####   ####  
 #####  #           # #    # #    # #####  #      #           # 
 #   #  #      #    # #    # #    # #   #  #    # #      #    # 
 #    # ######  ####   ####   ####  #    #  ####  ######  ####  

r1 = sf_mod.Tool(name = 'Blue cube', description="")
r2 = sf_mod.Tool(name = 'Orange cube', description="")
r3 = sf_mod.Tool(name = 'White cube', description="")

r4 = sf_mod.Worker(name = 'Human Operator', capabilities = [cap1, cap3], description="")
r5 = sf_mod.Cobot(name = 'Cobot', capabilities = [cap1, cap2], description="")

db.add_all([r1, r2, r3, r4, r5])

#aggregate resources
ar1 = sf_mod.AggregateResource(name = 'Station 1', resources = [r2, r5])
ar2 = sf_mod.AggregateResource(name = 'Station 2', resources = [r3, r4])

db.add_all([ar1, ar2])

 #####  #####   ####  #####  #    #  ####  #####  ####  
 #    # #    # #    # #    # #    # #    #   #   #      
 #    # #    # #    # #    # #    # #        #    ####  
 #####  #####  #    # #    # #    # #        #        # 
 #      #   #  #    # #    # #    # #    #   #   #    # 
 #      #    #  ####  #####   ####   ####    #    #### 
 
p1 = prod_mod.Product(name = 'Mosaico')

p2 = prod_mod.Product(name = 'Row 1')
p3 = prod_mod.Product(name = 'Row 2')
p4 = prod_mod.Product(name = 'Row 3')
p5 = prod_mod.Product(name = 'Row 4')
p6 = prod_mod.Product(name = 'Row 5')

db.add_all([p1, p2, p3, p4, p5, p6])

#product families
pf1 = prod_mod.ProductFamily(name = 'Rows', products = [p2, p3, p4, p5, p6])

db.add(pf1)

 #####  #####   ####   ####  ######  ####   ####  
 #    # #    # #    # #    # #      #      #      
 #    # #    # #    # #      #####   ####   ####  
 #####  #####  #    # #      #           #      # 
 #      #   #  #    # #    # #      #    # #    # 
 #      #    #  ####   ####  ######  ####   ####  

#complex tasks
c1 = proc_mod.ConjunctiveTask(name='Do Row 1')
c2 = proc_mod.ConjunctiveTask(name='Do Row 2')
c3 = proc_mod.ConjunctiveTask(name='Do Row 3')
c4 = proc_mod.ConjunctiveTask(name='Do Row 4')
c5 = proc_mod.ConjunctiveTask(name='Do Row 5')

tl = [c1, c2, c3, c4, c5]
db.add_all(tl)
db.commit()

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

tl_1 = [c10,c11,c12,c13,c14,c15,c16,c17,c18,c19]
tl_1.extend([c20,c21,c22,c23,c24,c25,c26,c27,c28,c29])
tl_1.extend([c30,c31,c32,c33,c34,c35,c36,c37,c38,c39])
tl_1.extend([c40,c41,c42,c43,c44,c45,c46,c47,c48,c49])
tl_1.extend([c50,c51,c52,c53,c54,c55,c56,c57,c58,c59])
tl.extend(tl_1)

db.add_all(tl_1)
db.commit()

#functions of cobot
f_cobot_1 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_2 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_3 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_4 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_5 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_6 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_7 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_8 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_9 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_10 = proc_mod.Function(f_type=cap2, operator=r5)
f_cobot_11 = proc_mod.Function(f_type=cap2, operator=r5)

#simple tasks of cobot
s10 = proc_mod.SimpleTask(name='Do Cell A1', modality='Independent', parent=c10, f=[f_cobot_1])
s11 = proc_mod.SimpleTask(name='Do Cell B1', modality='Independent', parent=c11, f=[f_cobot_2])
s12 = proc_mod.SimpleTask(name='Do Cell C1', modality='Independent', parent=c12, f=[f_cobot_3])
s20 = proc_mod.SimpleTask(name='Do Cell A2', modality='Independent', parent=c20, f=[f_cobot_4])
s30 = proc_mod.SimpleTask(name='Do Cell A3', modality='Independent', parent=c30, f=[f_cobot_5])
s31 = proc_mod.SimpleTask(name='Do Cell B3', modality='Independent', parent=c31, f=[f_cobot_6])
s32 = proc_mod.SimpleTask(name='Do Cell C3', modality='Independent', parent=c32, f=[f_cobot_7])
s42 = proc_mod.SimpleTask(name='Do Cell C4', modality='Independent', parent=c42, f=[f_cobot_8])
s50 = proc_mod.SimpleTask(name='Do Cell A5', modality='Independent', parent=c50, f=[f_cobot_9])
s51 = proc_mod.SimpleTask(name='Do Cell B5', modality='Independent', parent=c51, f=[f_cobot_10])
s52 = proc_mod.SimpleTask(name='Do Cell C5', modality='Independent', parent=c52, f=[f_cobot_11])

#functions
f_worker_1 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_2 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_3 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_4 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_5 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_6 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_7 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_8 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_9 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_10 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_11 = proc_mod.Function(f_type=cap3, operator=r4)
f_worker_12 = proc_mod.Function(f_type=cap3, operator=r4)

#simple tasks of operator
s14 = proc_mod.SimpleTask(name='Do Cell E1', modality='Independent', parent=c14, f=[f_worker_1])
s18 = proc_mod.SimpleTask(name='Do Cell I1', modality='Independent', parent=c18, f=[f_worker_2])
s24 = proc_mod.SimpleTask(name='Do Cell E2', modality='Independent', parent=c24, f=[f_worker_3])
s26 = proc_mod.SimpleTask(name='Do Cell G2', modality='Independent', parent=c26, f=[f_worker_4])
s28 = proc_mod.SimpleTask(name='Do Cell I2', modality='Independent', parent=c28, f=[f_worker_5])
s34 = proc_mod.SimpleTask(name='Do Cell E3', modality='Independent', parent=c34, f=[f_worker_6])
s36 = proc_mod.SimpleTask(name='Do Cell G3', modality='Independent', parent=c36, f=[f_worker_7])
s38 = proc_mod.SimpleTask(name='Do Cell I3', modality='Independent', parent=c38, f=[f_worker_8])
s45 = proc_mod.SimpleTask(name='Do Cell F4', modality='Independent', parent=c45, f=[f_worker_9])
s47 = proc_mod.SimpleTask(name='Do Cell H4', modality='Independent', parent=c47, f=[f_worker_10])
s55 = proc_mod.SimpleTask(name='Do Cell F5', modality='Independent', parent=c55, f=[f_worker_11])
s57 = proc_mod.SimpleTask(name='Do Cell H5', modality='Independent', parent=c57, f=[f_worker_12])

#functions of both
f_worker_1 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_2 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_3 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_4 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_5 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_6 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_7 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_8 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_9 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_10 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_11 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_12 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_13 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_14 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_15 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_16 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_17 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_18 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_19 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_20 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_21 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_22 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_23 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_24 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_25 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_26 = proc_mod.Function(f_type=cap1, operator=r4)
f_worker_27 = proc_mod.Function(f_type=cap1, operator=r4)

f_cobot_1 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_2 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_3 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_4 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_5 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_6 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_7 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_8 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_9 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_10 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_11 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_12 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_13 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_14 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_15 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_16 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_17 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_18 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_19 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_20 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_21 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_22 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_23 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_24 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_25 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_26 = proc_mod.Function(f_type=cap1, operator=r5)
f_cobot_27 = proc_mod.Function(f_type=cap1, operator=r5)

#simple tasks of both - worker
s13_w = proc_mod.SimpleTask(name='Do Cell D1', modality='Independent', parent=c13, f=[f_worker_1])
s15_w = proc_mod.SimpleTask(name='Do Cell F1', modality='Independent', parent=c15, f=[f_worker_2])
s16_w = proc_mod.SimpleTask(name='Do Cell G1', modality='Independent', parent=c16, f=[f_worker_3])
s17_w = proc_mod.SimpleTask(name='Do Cell H1', modality='Independent', parent=c17, f=[f_worker_4])
s19_w = proc_mod.SimpleTask(name='Do Cell J1', modality='Independent', parent=c19, f=[f_worker_5])
s21_w = proc_mod.SimpleTask(name='Do Cell B2', modality='Independent', parent=c21, f=[f_worker_6])
s22_w = proc_mod.SimpleTask(name='Do Cell C2', modality='Independent', parent=c22, f=[f_worker_7])
s23_w = proc_mod.SimpleTask(name='Do Cell D2', modality='Independent', parent=c23, f=[f_worker_8])
s25_w = proc_mod.SimpleTask(name='Do Cell F2', modality='Independent', parent=c25, f=[f_worker_9])
s27_w = proc_mod.SimpleTask(name='Do Cell H2', modality='Independent', parent=c27, f=[f_worker_10])
s29_w = proc_mod.SimpleTask(name='Do Cell J2', modality='Independent', parent=c29, f=[f_worker_11])
s33_w = proc_mod.SimpleTask(name='Do Cell D3', modality='Independent', parent=c33, f=[f_worker_12])
s35_w = proc_mod.SimpleTask(name='Do Cell F3', modality='Independent', parent=c35, f=[f_worker_13])
s37_w = proc_mod.SimpleTask(name='Do Cell H3', modality='Independent', parent=c37, f=[f_worker_14])
s39_w = proc_mod.SimpleTask(name='Do Cell J3', modality='Independent', parent=c39, f=[f_worker_15])
s40_w = proc_mod.SimpleTask(name='Do Cell A4', modality='Independent', parent=c40, f=[f_worker_16])
s41_w = proc_mod.SimpleTask(name='Do Cell B4', modality='Independent', parent=c41, f=[f_worker_17])
s43_w = proc_mod.SimpleTask(name='Do Cell D4', modality='Independent', parent=c43, f=[f_worker_18])
s44_w = proc_mod.SimpleTask(name='Do Cell E4', modality='Independent', parent=c44, f=[f_worker_19])
s46_w = proc_mod.SimpleTask(name='Do Cell G4', modality='Independent', parent=c46, f=[f_worker_20])
s48_w = proc_mod.SimpleTask(name='Do Cell I4', modality='Independent', parent=c48, f=[f_worker_21])
s49_w = proc_mod.SimpleTask(name='Do Cell J4', modality='Independent', parent=c49, f=[f_worker_22])
s53_w = proc_mod.SimpleTask(name='Do Cell D5', modality='Independent', parent=c53, f=[f_worker_23])
s54_w = proc_mod.SimpleTask(name='Do Cell E5', modality='Independent', parent=c54, f=[f_worker_24])
s56_w = proc_mod.SimpleTask(name='Do Cell G5', modality='Independent', parent=c56, f=[f_worker_25])
s58_w = proc_mod.SimpleTask(name='Do Cell I5', modality='Independent', parent=c58, f=[f_worker_26])
s59_w = proc_mod.SimpleTask(name='Do Cell J5', modality='Independent', parent=c59, f=[f_worker_27])

#simple tasks of both - cobot
s13_c = proc_mod.SimpleTask(name='Do Cell D1', modality='Independent', parent=c13, f=[f_cobot_1])
s15_c = proc_mod.SimpleTask(name='Do Cell F1', modality='Independent', parent=c15, f=[f_cobot_2])
s16_c = proc_mod.SimpleTask(name='Do Cell G1', modality='Independent', parent=c16, f=[f_cobot_3])
s17_c = proc_mod.SimpleTask(name='Do Cell H1', modality='Independent', parent=c17, f=[f_cobot_4])
s19_c = proc_mod.SimpleTask(name='Do Cell J1', modality='Independent', parent=c19, f=[f_cobot_5])
s21_c = proc_mod.SimpleTask(name='Do Cell B2', modality='Independent', parent=c21, f=[f_cobot_6])
s22_c = proc_mod.SimpleTask(name='Do Cell C2', modality='Independent', parent=c22, f=[f_cobot_7])
s23_c = proc_mod.SimpleTask(name='Do Cell D2', modality='Independent', parent=c23, f=[f_cobot_8])
s25_c = proc_mod.SimpleTask(name='Do Cell F2', modality='Independent', parent=c25, f=[f_cobot_9])
s27_c = proc_mod.SimpleTask(name='Do Cell H2', modality='Independent', parent=c27, f=[f_cobot_10])
s29_c = proc_mod.SimpleTask(name='Do Cell J2', modality='Independent', parent=c29, f=[f_cobot_11])
s33_c = proc_mod.SimpleTask(name='Do Cell D3', modality='Independent', parent=c33, f=[f_cobot_12])
s35_c = proc_mod.SimpleTask(name='Do Cell F3', modality='Independent', parent=c35, f=[f_cobot_13])
s37_c = proc_mod.SimpleTask(name='Do Cell H3', modality='Independent', parent=c37, f=[f_cobot_14])
s39_c = proc_mod.SimpleTask(name='Do Cell J3', modality='Independent', parent=c39, f=[f_cobot_15])
s40_c = proc_mod.SimpleTask(name='Do Cell A4', modality='Independent', parent=c40, f=[f_cobot_16])
s41_c = proc_mod.SimpleTask(name='Do Cell B4', modality='Independent', parent=c41, f=[f_cobot_17])
s43_c = proc_mod.SimpleTask(name='Do Cell D4', modality='Independent', parent=c43, f=[f_cobot_18])
s44_c = proc_mod.SimpleTask(name='Do Cell E4', modality='Independent', parent=c44, f=[f_cobot_19])
s46_c = proc_mod.SimpleTask(name='Do Cell G4', modality='Independent', parent=c46, f=[f_cobot_20])
s48_c = proc_mod.SimpleTask(name='Do Cell I4', modality='Independent', parent=c48, f=[f_cobot_21])
s49_c = proc_mod.SimpleTask(name='Do Cell J4', modality='Independent', parent=c49, f=[f_cobot_22])
s53_c = proc_mod.SimpleTask(name='Do Cell D5', modality='Independent', parent=c53, f=[f_cobot_23])
s54_c = proc_mod.SimpleTask(name='Do Cell E5', modality='Independent', parent=c54, f=[f_cobot_24])
s56_c = proc_mod.SimpleTask(name='Do Cell G5', modality='Independent', parent=c56, f=[f_cobot_25])
s58_c = proc_mod.SimpleTask(name='Do Cell I5', modality='Independent', parent=c58, f=[f_cobot_26])
s59_c = proc_mod.SimpleTask(name='Do Cell J5', modality='Independent', parent=c59, f=[f_cobot_27])


#constraints
con1 = proc_mod.Constraint(t1=c1, t2=c3)
con2 = proc_mod.Constraint(t1=c1, t2=c4)
con3 = proc_mod.Constraint(t1=c2, t2=c4)
con4 = proc_mod.Constraint(t1=c1, t2=c5)
con5 = proc_mod.Constraint(t1=c2, t2=c5)
con6 = proc_mod.Constraint(t1=c3, t2=c5)

tl.extend([s10,s11,s12,s13_w,s13_c,s14,s15_w,s15_c,s16_w,s16_c,s17_w,s17_c,s18,s19_w,s19_c])
tl.extend([s20,s21_w,s21_c,s22_w,s22_c,s23_w,s23_c,s24,s25_w,s25_c,s26,s27_w,s27_c,s28,s29_w,s29_c])
tl.extend([s30,s31,s32,s33_w,s33_c,s34,s35_w,s35_c,s36,s37_w,s37_c,s38,s39_w,s39_c])
tl.extend([s40_w,s40_c,s41_w,s41_c,s42,s43_w,s43_c,s44_w,s44_c,s45,s46_w,s46_c,s47,s48_w,s48_c,s49_w,s49_c])
tl.extend([s50,s51,s52,s53_w,s53_c,s54_w,s54_c,s55,s56_w,s56_c,s57,s58_w,s58_c,s59_w,s59_c])

#process
procM = proc_mod.Process(name='Do Mosaic', product=p1, tasks_list = tl,
            constraints = [con1, con2, con3, con4, con5, con6])


#demand
d1 = dem_mod.Demand(name = 'Mosaic', quantity = 1, product = p1, typeDem='StockOrder', process=procM)


db.add(procM)
db.add(d1)

#commit and close
db.commit()
db.close()
