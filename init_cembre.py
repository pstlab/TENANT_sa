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
                                                          
 ###### #    # #    #  ####  ##### #  ####  #    #  ####  
 #      #    # ##   # #    #   #   # #    # ##   # #      
 #####  #    # # #  # #        #   # #    # # #  #  ####  
 #      #    # #  # # #        #   # #    # #  # #      # 
 #      #    # #   ## #    #   #   # #    # #   ## #    # 
 #       ####  #    #  ####    #   #  ####  #    #  ####  
                                                          
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
f13 = sf_mod.Function(name = 'Block Pallet')
f14 = sf_mod.Function(name = 'Unblock Pallet')

all_functions = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]
#add all
db.add_all(all_functions)
                                                                
 #####  ######  ####   ####  #    # #####   ####  ######  ####  
 #    # #      #      #    # #    # #    # #    # #      #      
 #    # #####   ####  #    # #    # #    # #      #####   ####  
 #####  #           # #    # #    # #####  #      #           # 
 #   #  #      #    # #    # #    # #   #  #    # #      #    # 
 #    # ######  ####   ####   ####  #    #  ####  ######  ####  
                                                                
r1 = sf_mod.CapacityResource(name='Postazione1')
r2 = sf_mod.CapacityResource(name='Postazione2')
r3 = sf_mod.CapacityResource(name='Postazione3')

r4 = sf_mod.CapacityResource(name="Cassetta Pick")
r5 = sf_mod.CapacityResource(name="Cassetta Release")

r6 = sf_mod.ProductionObject(name="Ricambio1")
r7 = sf_mod.ProductionObject(name="Ricambio2")
r8 = sf_mod.ProductionObject(name="Ricambio3")

db.add_all([r1, r2, r3, r4, r5])
db.add_all([r6, r7, r8])
                                          
   ##    ####  ###### #    # #####  ####  
  #  #  #    # #      ##   #   #   #      
 #    # #      #####  # #  #   #    ####  
 ###### #  ### #      #  # #   #        # 
 #    # #    # #      #   ##   #   #    # 
 #    #  ####  ###### #    #   #    ####  
                                          
hw = sf_mod.Worker(name='Operatore', functions=all_functions)
ra = sf_mod.Cobot(name='Robotic Arm', functions=all_functions)

db.add_all([hw, ra])
                                                        
 #####  #####   ####  #####  #    #  ####  #####  ####  
 #    # #    # #    # #    # #    # #    #   #   #      
 #    # #    # #    # #    # #    # #        #    ####  
 #####  #####  #    # #    # #    # #        #        # 
 #      #   #  #    # #    # #    # #    #   #   #    # 
 #      #    #  ####  #####   ####   ####    #    ####  
                                                        
p1 = prod_mod.Product(name='pezzo1')
p2 = prod_mod.Product(name='pezzo2')
p3 = prod_mod.Product(name='pezzo3')

db.add_all([p1, p2, p3])
                                                  
 #####  #####   ####   ####  ######  ####   ####  
 #    # #    # #    # #    # #      #      #      
 #    # #    # #    # #      #####   ####   ####  
 #####  #####  #    # #      #           #      # 
 #      #   #  #    # #    # #      #    # #    # 
 #      #    #  ####   ####  ######  ####   ####  

c1 = proc_mod.ConjunctiveTask(name='Task di root')
db.add(c1)
db.commit()

c11 = proc_mod.ConjunctiveTask(name='Sposta in post 2', parent=c1)
db.add(c11)
db.commit()
s111 = proc_mod.SimpleTask(name='Sposta da 1 a 2', modality='Independent', parent=c11, f1=f3)

c12 = proc_mod.DisjunctiveTask(name='Main process', parent=c1)
db.add(c12)
db.commit()

c121 = proc_mod.ConjunctiveTask(name='Tutto in post 2', parent=c12)
db.add(c121)
db.commit()
s1211 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c121, f1=f13)
c1212 = proc_mod.ConjunctiveTask(name='Smontaggio', parent=c121)
db.add(c1212)
db.commit()
###
c12121 = proc_mod.DisjunctiveTask(name='Svita', parent=c1212)
db.add(c12121)
db.commit()
s121211 = proc_mod.SimpleTask(name='Svita uomo', modality='Independent', parent=c12121, f1=f5)
s121212 = proc_mod.SimpleTask(name='Svita robot', modality='Independent', parent=c12121, f1=f5)
c12122 = proc_mod.DisjunctiveTask(name='Estrazione', parent=c1212)
db.add(c12122)
db.commit()
s121221 = proc_mod.SimpleTask(name='Estrazione uomo', modality='Independent', parent=c12122, f1=f7)
s121222 = proc_mod.SimpleTask(name='Estrazione robot', modality='Independent', parent=c12122, f1=f7)
c12123 = proc_mod.DisjunctiveTask(name='Release', parent=c1212)
db.add(c12123)
db.commit()
s121231 = proc_mod.SimpleTask(name='Release uomo', modality='Independent', parent=c12123, f1=f3)
s121232 = proc_mod.SimpleTask(name='Release robot', modality='Independent', parent=c12123, f1=f3)
###
c1213 = proc_mod.ConjunctiveTask(name='Assemblaggio', parent=c121)
db.add(c1213)
db.commit()
###
c12131 = proc_mod.DisjunctiveTask(name='Picking', parent= c1213)
db.add(c12131)
db.commit()
s121311 = proc_mod.SimpleTask(name='Picking uomo', modality='Independent', parent= c12131, f1=f3)
s121312 = proc_mod.SimpleTask(name='Picking robot', modality='Independent', parent= c12131, f1=f3)
c12132 = proc_mod.DisjunctiveTask(name='Bloccaggio', parent= c1213)
db.add(c12132)
db.commit()
s121321 = proc_mod.SimpleTask(name='Bloccaggio uomo', modality='Independent', parent= c12132, f1=f6)
s121322 = proc_mod.SimpleTask(name='Bloccaggio robot', modality='Independent', parent= c12132, f1=f6)
c12133 = proc_mod.DisjunctiveTask(name='Avvita', parent= c1213)
db.add(c12133)
db.commit()
s121331 = proc_mod.SimpleTask(name='Avvita uomo', modality='Independent', parent= c12133, f1=f4)
s121332 = proc_mod.SimpleTask(name='Avvita robot', modality='Independent', parent= c12133, f1=f4)
###
s1214 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c121, f1=f14)

c122 = proc_mod.ConjunctiveTask(name='Tutto in post 3', parent=c12)
db.add(c122)
db.commit()
s1221 = proc_mod.SimpleTask(name='Sposta da 2 a 3', modality='Independent', parent=c122, f1=f3)
s1222 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c122, f1=f13)
c1223 = proc_mod.ConjunctiveTask(name='Smontaggio', parent=c122)
c1224 = proc_mod.ConjunctiveTask(name='Assemblaggio', parent=c122)
s1225 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c122, f1=f14)

c123 = proc_mod.ConjunctiveTask(name='Misto nelle post', parent=c12)
db.add(c123)
db.commit()
s1231 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c123, f1=f13)
c1232 = proc_mod.ConjunctiveTask(name='Smontaggio', parent=c123)
s1233 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c123, f1=f14)
s1224 = proc_mod.SimpleTask(name='Sposta da 2 a 3', modality='Independent', parent=c123, f1=f3)
s1235 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c123, f1=f13)
c1236 = proc_mod.ConjunctiveTask(name='Assemblaggio', parent=c123)
s1237 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c123, f1=f14)

s13 = proc_mod.SimpleTask(name='Sposta a 3', modality='Independent', parent=c1, f1=f3)

ct = [c1]
ct.extend([c11, c12])
ct.extend([c121, c122, c123])
ct.extend([c1212, c1213, c1223, c1224, c1232, c1236])
ct.extend([c12121, c12122, c12123, c12131, c12132, c12133])

ct.extend([s13])
ct.extend([s111])
ct.extend([s1211, s1214, s1221, s1222, s1224, s1225, s1231, s1233, s1235, s1237])
ct.extend([s121211, s121212, s121221, s121222, s121231, s121232])
ct.extend([s121311, s121312, s121321, s121322, s121331, s121332])

tc1 = proc_mod.Constraint(t1=c11, t2=c12)
tc2 = proc_mod.Constraint(t1=c11, t2=s13)
tc3 = proc_mod.Constraint(t1=c12, t2=s13)

tc = [tc1, tc2, tc3]

proc1 = proc_mod.Process(name="Processo 1", product=p1,
            tasks_list = ct, constraints=tc)

db.add(proc1)

#commit and close
db.commit()
db.close()