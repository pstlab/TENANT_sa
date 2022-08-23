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


                                                          
cap1 = sf_mod.Capability(name = 'Pick Object')
cap2 = sf_mod.Capability(name = 'Place Object')
cap3 = sf_mod.Capability(name = 'PickAndPlace Object')
cap4 = sf_mod.Capability(name = 'Screw')
cap5 = sf_mod.Capability(name = 'Unscrew')
cap6 = sf_mod.Capability(name = 'Assemble')
cap7 = sf_mod.Capability(name = 'Disassemble')
cap8 = sf_mod.Capability(name = 'Manual Guidance')
cap9 = sf_mod.Capability(name = 'Motion')
cap10 = sf_mod.Capability(name = 'Move/Navigate')
cap11 = sf_mod.Capability(name = 'Weld')
cap12 = sf_mod.Capability(name = 'Inspect')
cap13 = sf_mod.Capability(name = 'Block Pallet')
cap14 = sf_mod.Capability(name = 'Unblock Pallet')

hw_capabilities = [cap1, cap2, cap3, cap4, cap5, cap6, cap7, cap8, cap9, cap10, cap11, cap12, cap13, cap14]
ra_capabilities = [cap1, cap2, cap3, cap4, cap5, cap6, cap7, cap8, cap9, cap10, cap11, cap12]
                                                                
 #####  ######  ####   ####  #    # #####   ####  ######  ####  
 #    # #      #      #    # #    # #    # #    # #      #      
 #    # #####   ####  #    # #    # #    # #      #####   ####  
 #####  #           # #    # #    # #####  #      #           # 
 #   #  #      #    # #    # #    # #   #  #    # #      #    # 
 #    # ######  ####   ####   ####  #    #  ####  ######  ####  
                                                                
r1 = sf_mod.CapacityResource(name='Postazione1', description="")
r2 = sf_mod.CapacityResource(name='Postazione2', description="")
r3 = sf_mod.CapacityResource(name='Postazione3', description="")

r4 = sf_mod.CapacityResource(name="Cassetta Pick", description="")
r5 = sf_mod.CapacityResource(name="Cassetta Release", description="")

r6 = sf_mod.ProductionObject(name="Ricambio1", description="")
r7 = sf_mod.ProductionObject(name="Ricambio2", description="")
r8 = sf_mod.ProductionObject(name="Ricambio3",description="")

db.add_all([r1, r2, r3, r4, r5])
db.add_all([r6, r7, r8])
                                          
   ##    ####  ###### #    # #####  ####  
  #  #  #    # #      ##   #   #   #      
 #    # #      #####  # #  #   #    ####  
 ###### #  ### #      #  # #   #        # 
 #    # #    # #      #   ##   #   #    # 
 #    #  ####  ###### #    #   #    ####  
                                          
hw = sf_mod.Worker(name='Operatore', capabilities=hw_capabilities, description="")
ra = sf_mod.Cobot(name='Robotic Arm', capabilities=ra_capabilities, description="")

db.add_all([hw, ra])
                                                        
 #####  #####   ####  #####  #    #  ####  #####  ####  
 #    # #    # #    # #    # #    # #    #   #   #      
 #    # #    # #    # #    # #    # #        #    ####  
 #####  #####  #    # #    # #    # #        #        # 
 #      #   #  #    # #    # #    # #    #   #   #    # 
 #      #    #  ####  #####   ####   ####    #    ####  
                                                        
p1 = prod_mod.Product(name='Pezzo 1')
p2 = prod_mod.Product(name='Pezzo 2')
p3 = prod_mod.Product(name='Pezzo 3')

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
f111 = proc_mod.Function(f_type=cap3, operator=hw)
s111 = proc_mod.SimpleTask(name='Sposta da 1 a 2', modality='Independent', parent=c11, f=[f111])

c12 = proc_mod.DisjunctiveTask(name='Main process', parent=c1)
db.add(c12)
db.commit()

c121 = proc_mod.ConjunctiveTask(name='Tutto in post 2', parent=c12)
db.add(c121)
db.commit()
f1211 = proc_mod.Function(f_type=cap13, operator=hw)
s1211 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c121, f=[f1211])
c1212 = proc_mod.ConjunctiveTask(name='Smontaggio', parent=c121)
db.add(c1212)
db.commit()
###
c12121 = proc_mod.DisjunctiveTask(name='Svita', parent=c1212)
db.add(c12121)
db.commit()
f121211_hw = proc_mod.Function(f_type=cap5, operator=hw)
f121211_ra = proc_mod.Function(f_type=cap5, operator=ra)
s121211 = proc_mod.SimpleTask(name='Svita uomo', modality='Independent', parent=c12121, f=[f121211_hw])
s121212 = proc_mod.SimpleTask(name='Svita robot', modality='Independent', parent=c12121, f=[f121211_ra])
c12122 = proc_mod.DisjunctiveTask(name='Estrazione', parent=c1212)
db.add(c12122)
db.commit()
f121221_hw = proc_mod.Function(f_type=cap7, operator=hw)
f121221_ra = proc_mod.Function(f_type=cap7, operator=ra)
s121221 = proc_mod.SimpleTask(name='Estrazione uomo', modality='Independent', parent=c12122, f=[f121221_hw])
s121222 = proc_mod.SimpleTask(name='Estrazione robot', modality='Independent', parent=c12122, f=[f121221_ra])
c12123 = proc_mod.DisjunctiveTask(name='Release', parent=c1212)
db.add(c12123)
db.commit()
f121231_hw = proc_mod.Function(f_type=cap3, operator=hw)
f121231_ra = proc_mod.Function(f_type=cap3, operator=ra)
s121231 = proc_mod.SimpleTask(name='Release uomo', modality='Independent', parent=c12123, f=[f121231_hw])
s121232 = proc_mod.SimpleTask(name='Release robot', modality='Independent', parent=c12123, f=[f121231_ra])
###
c1213 = proc_mod.ConjunctiveTask(name='Assemblaggio', parent=c121)
db.add(c1213)
db.commit()
###
c12131 = proc_mod.DisjunctiveTask(name='Picking', parent= c1213)
db.add(c12131)
db.commit()
f121311_hw = proc_mod.Function(f_type=cap3, operator=hw)
f121311_ra = proc_mod.Function(f_type=cap3, operator=ra)
s121311 = proc_mod.SimpleTask(name='Picking uomo', modality='Independent', parent= c12131, f=[f121311_hw])
s121312 = proc_mod.SimpleTask(name='Picking robot', modality='Independent', parent= c12131, f=[f121311_ra])
c12132 = proc_mod.DisjunctiveTask(name='Bloccaggio', parent= c1213)
db.add(c12132)
db.commit()
f121321_hw = proc_mod.Function(f_type=cap6, operator=hw)
f121321_ra = proc_mod.Function(f_type=cap6, operator=ra)
s121321 = proc_mod.SimpleTask(name='Bloccaggio uomo', modality='Independent', parent= c12132, f=[f121321_hw])
s121322 = proc_mod.SimpleTask(name='Bloccaggio robot', modality='Independent', parent= c12132, f=[f121321_ra])
c12133 = proc_mod.DisjunctiveTask(name='Avvita', parent= c1213)
db.add(c12133)
db.commit()
f121331_hw = proc_mod.Function(f_type=cap4, operator=hw)
f121331_ra = proc_mod.Function(f_type=cap4, operator=ra)
s121331 = proc_mod.SimpleTask(name='Avvita uomo', modality='Independent', parent= c12133, f=[f121331_hw])
s121332 = proc_mod.SimpleTask(name='Avvita robot', modality='Independent', parent= c12133, f=[f121331_ra])
###
f1214 = proc_mod.Function(f_type=cap14, operator=hw)
s1214 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c121, f=[f1214])

c122 = proc_mod.ConjunctiveTask(name='Tutto in post 3', parent=c12)
db.add(c122)
db.commit()
f1221 = proc_mod.Function(f_type=cap3, operator=hw)
s1221 = proc_mod.SimpleTask(name='Sposta da 2 a 3', modality='Independent', parent=c122, f=[f1221])
f1222 = proc_mod.Function(f_type=cap13, operator=hw)
s1222 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c122, f=[f1222])
c1223 = proc_mod.ConjunctiveTask(name='Smontaggio', parent=c122)
c1224 = proc_mod.ConjunctiveTask(name='Assemblaggio', parent=c122)
f1225 = proc_mod.Function(f_type=cap14, operator=hw)
s1225 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c122, f=[f1225])

c123 = proc_mod.ConjunctiveTask(name='Misto nelle post', parent=c12)
db.add(c123)
db.commit()
f1231 = proc_mod.Function(f_type=cap13, operator=hw)
s1231 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c123, f=[f1231])
c1232 = proc_mod.ConjunctiveTask(name='Smontaggio', parent=c123)
f1233 = proc_mod.Function(f_type=cap14, operator=hw)
s1233 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c123, f=[f1233])
f1224 = proc_mod.Function(f_type=cap3, operator=hw)
s1224 = proc_mod.SimpleTask(name='Sposta da 2 a 3', modality='Independent', parent=c123, f=[f1224])
f1235 = proc_mod.Function(f_type=cap13, operator=hw)
s1235 = proc_mod.SimpleTask(name='Blocca', modality='Independent', parent=c123, f=[f1235])
c1236 = proc_mod.ConjunctiveTask(name='Assemblaggio', parent=c123)
f1237 = proc_mod.Function(f_type=cap14, operator=hw)
s1237 = proc_mod.SimpleTask(name='Sblocca', modality='Independent', parent=c123, f=[f1237])

f13 = proc_mod.Function(f_type=cap3, operator=hw)
s13 = proc_mod.SimpleTask(name='Sposta a 3', modality='Independent', parent=c1, f=[f13])

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