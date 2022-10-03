# Import flask dependencies
from flask import Blueprint, render_template, request
from .models import *
from app import app

from app.products.models import Product
from app.shopfloor.models import _Agent, Capability, Resource

# Define the blueprint: 'process', set its url prefix: app.url/process
mod_process = Blueprint('process', __name__, url_prefix='/process')

#welcome page of the processes. Display the list and a button from which add a new process(new page), 
#remove a process(post request with id), view in detail a process(new page) from which modify it (new page)
@mod_process.route('/', methods=['GET'])
def hello():
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#remove a process
@mod_process.route('/', methods=['POST'])
def remove():
    data = request.json
    procId = data[0]
    app.session.query(Process).filter_by(id=procId).delete()
        
    app.session.commit()
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#add a new process to the db. welcome page and request (post) after the user data input
@mod_process.route('/newProc/', methods=['GET'])
def new():
    prod = app.session.query(Product).all()
    capabilities = app.session.query(Capability).all()
    resources = app.session.query(Resource).filter(Resource.typeRes!="Cobot", Resource.typeRes!="Worker").all()
    return render_template("processes/newProc.html", products=prod, capabilities=capabilities, resources=resources)

@mod_process.route('/newProc/', methods=['POST'])
def newP():
    data = request.json
    # Add a new process
    name = data[0]['name']
    pId = data[0]['product']
    p = app.session.query(Product).filter_by(id=pId).first()

    tasks = data[0]['tasks']
    t_list, idPageidDb = addTask(tasks)

    c = data[0]['constraints']
    cons = []
    for element in c:
        id1 = int(element['t1'])
        id2 = int(element['t2'])
        id1 = idPageidDb.get(id1)
        id2 = idPageidDb.get(id2)
        t1 = app.session.query(Task).filter_by(id=id1).first()
        t2 = app.session.query(Task).filter_by(id=id2).first()
        tmp = Constraint(t1=t1, t2=t2)
        cons.append(tmp)

    process = Process(name=name, product=p, tasks_list=t_list, constraints=cons)

    app.session.add(process)
    app.session.commit()

    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#AUXILIARY FUNCTIONS to define the complex tasks objects
# and associate all to the process
def addTask(tasks):
    list_of_task = []
    idPageidDb = {}
    for i in range(len(tasks)):
        #take the values
        name = tasks[i]['name']
        ttype = tasks[i]['type']
        tdescr = tasks[i]['description']
        idPage = tasks[i]['id']
        #If the task it's at the higher level, simply add it to the list
        if(ttype == 'complex'):
            complexType = tasks[i]['complexType']
            klass = globals()[complexType]
            c = klass(name=name, description=tdescr)

            app.session.add(c)
            app.session.commit()
            idDb = c.id
            idPageidDb.update({idPage: idDb})
            list_of_task.append(c)

            subT = tasks[i]['list']
            #then iterate on its subtasks, but iff it's a complex one
            tmp_list, idPageidDb = addTaskAux(c, subT, [], idPageidDb)
            list_of_task.extend(tmp_list)

        elif(ttype == 'simple'):
            mode = tasks[i]['modality']

            capability1id = tasks[i]['f1']
            capability2id = tasks[i]['f2']

            capability1 = app.session.query(Capability).filter_by(id=capability1id).first()
            capability2 = app.session.query(Capability).filter_by(id=capability2id).first()
            
            agent1id = tasks[i]['agent1']
            agent2id = tasks[i]['agent2']

            product1id = tasks[i]['product1']
            product2id = tasks[i]['product2']

            resources1id = tasks[i]['resources1']
            resources2id = tasks[i]['resources2']
            
            agent1 = app.session.query(_Agent).filter_by(id=agent1id).first()
            product1 = app.session.query(Product).filter_by(id=product1id).first()
            resources1 = []
            for r_id in resources1id:
                r = app.session.query(Resource).filter_by(id=r_id).first()
                resources1.append(r)
            f1 = Function(f_type=capability1, agent=agent1, target_product=product1, required_resources=resources1)
            functions = [f1]

            if(capability2):
                agent2 = app.session.query(_Agent).filter_by(id=agent2id).first()
                product2 = app.session.query(Product).filter_by(id=product2id).first()
                resources2 = []
                for r_id in resources2id:
                    r = app.session.query(Resource).filter_by(id=r_id).first()
                    resources2.append(r)
                f2 = Function(f_type=capability2, agent=agent2, target_product=product2, required_resources=resources2)
                functions.append(f2)

            s = SimpleTask(name=name, modality=mode, f=functions, description=tdescr)
            list_of_task.append(s)
            app.session.add(s)
            app.session.commit()
            idDb = s.id
            idPageidDb.update({idPage: idDb})
    
    return list_of_task, idPageidDb

def addTaskAux(parent, subT, res, idPageidDb):
    if(not subT):
        return [], idPageidDb
    for i in range(len(subT)):
        name = subT[i]['name']
        ttype = subT[i]['type']
        tdescr = subT[i]['description']
        idPage = subT[i]['id']
        if(ttype == 'complex'):
            complexType = subT[i]['complexType']
            klass = globals()[complexType]
            c = klass(name=name, parent=parent,  description=tdescr)
            res.append(c)
            app.session.add(c)
            app.session.commit()
            idDb = c.id
            idPageidDb.update({idPage: idDb})

            tmp, idPageidDb = addTaskAux(c, subT[i]['list'], [], idPageidDb)
            if (tmp):
                res.extend(tmp)

        elif(ttype == 'simple'):
            mode = subT[i]['modality']

            capability1id = subT[i]['f1']
            capability2id = subT[i]['f2']

            capability1 = app.session.query(Capability).filter_by(id=capability1id).first()
            capability2 = app.session.query(Capability).filter_by(id=capability2id).first()
            
            agent1id = subT[i]['agent1']
            agent2id = subT[i]['agent2']

            product1id = subT[i]['product1']
            product2id = subT[i]['product2']

            resources1id = subT[i]['resources1']
            resources2id = subT[i]['resources2']
            
            agent1 = app.session.query(_Agent).filter_by(id=agent1id).first()
            product1 = app.session.query(Product).filter_by(id=product1id).first()
            resources1 = []
            for r_id in resources1id:
                r = app.session.query(Resource).filter_by(id=r_id).first()
                resources1.append(r)
            f1 = Function(f_type=capability1, agent=agent1, target_product=product1, required_resources=resources1)
            functions = [f1]

            if(capability2):
                agent2 = app.session.query(_Agent).filter_by(id=agent2id).first()
                product2 = app.session.query(Product).filter_by(id=product2id).first()
                resources2 = []
                for r_id in resources2id:
                    r = app.session.query(Resource).filter_by(id=r_id).first()
                    resources2.append(r)
                f2 = Function(f_type=capability2, agent=agent2, target_product=product2, required_resources=resources2)
                functions.append(f2)

            s = SimpleTask(name=name, modality=mode, parent=parent, f=functions, description=tdescr)
            
            res.append(s)
            app.session.add(s)
            app.session.commit()
            idDb = s.id
            idPageidDb.update({idPage: idDb})

    return res, idPageidDb

#edit a process in the db. welcome page to view it and request (post) after the user data input
@mod_process.route('/viewProc/<procId>', methods=['GET'])
def mod(procId):
    proc = app.session.query(Process).filter_by(id=procId).first()
    prod = app.session.query(Product).all()
    return render_template("processes/detailProc.html", process=proc, products=prod)

@mod_process.route('/viewProc/<procId>', methods=['POST'])
def modP(procId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    pId = data[1]['processProduct']
    processId = data[0]

    #get the database values and update them
    proc = app.session.query(Process).filter_by(id=processId).first()
    proc.name = name
    p = app.session.query(Product).filter_by(id=pId).first()
    proc.product = p

    app.session.commit()
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)