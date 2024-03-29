// function to execute on page load
$(document).ready(function () {
    const IND = "Independent";
    const SIM = "Simultaneous";
    const SEQ = "Sequential";
    const SUPP = "Supportive";

    var tasks = [];
    var constraints = [];

    var ComplexTask = class ComplexTask {
        constructor(id, name, ct, list, description) {
            this.id = id;
            this.name = name;
            this.list = list;
            this.type = 'complex';
            this.complexType = ct;
            this.description = description;
        }
    };

    var SimpleTask = class SimpleTask {
        constructor(id, name, modality, f1, agent1, product1, resources1,
             f2, agent2, product2, resources2, description) {
            this.id = id;
            this.name = name;
            this.modality = modality;
            this.type = 'simple'
            this.f1 = f1;
            this.agent1 = agent1;
            this.product1 = product1;
            this.resources1 = resources1;
            this.f2 = f2;
            this.agent2 = agent2;
            this.product2 = product2;
            this.resources2 = resources2;
            this.description = description;
        }

    };

    var Constraint = class Constraint {
        constructor(id, t1, t2) {
            this.id = id;
            this.t1 = t1;
            this.t2 = t2;
        }
    };

    $('#new-res1').multiSelect();
    $('#new-res2').multiSelect();

    $(".containComplex").hide();
    $(".containSimple").hide();
    $(".constraintForm").hide();
    $(".mod").hide();
    $(".mod2").hide();
    $(".ms-container").hide();

    /*******************************************
     *  Show the form for each complex task     
    ******************************************/
    //TODO refactorize to have only a parametric function
    $("#complex").click(function () {
        $(".containComplex").show();
        $(".containSimple").hide();
        $(".constraintForm").hide();
    });

    /*******************************************
      *  Show the form for each simple task     
     ******************************************/
    $("#simple").click(function () {
        $(".containComplex").hide();
        $(".containSimple").show();
        $(".constraintForm").hide();
    });

    /*******************************************
     *  Show the form for a complex task 
     * to be added from another complex task     
    ******************************************/
    $(document).on("click", ".complexST", function () {
        tmp = $(this).siblings(".subtaskid").html();
        specialID = Number(tmp)
        $(".containComplex").show();
        $(".containSimple").hide();
        $(".constraintForm").hide();
    });

    /*******************************************
     *  Show the form for a simple task 
     * to be added from another (complex) task     
    ******************************************/
    $(document).on("click", ".simpleST", function () {
        tmp = $(this).siblings(".subtaskid").html();
        specialID = Number(tmp)
        $(".containComplex").hide();
        $(".containSimple").show();
        $(".constraintForm").hide();
    });

    /**************************************
    *  Show the form of the functions
    **************************************/
    $("#new-Staskmode").change(function () {
        mod = this.value;
        $(".mod").show();
        $("#ms-new-res1").show();
        if (mod !== IND) {
            $(".mod2").show();
            $("#ms-new-res2").show();
        }
        else {
            $(".mod2").hide();
            $("#ms-new-res2").hide();
        }
    });

    /**************************************
    *  Show the form to add a constraint
    **************************************/
    $("#constraint").click(function () {
        $(".containComplex").hide();
        $(".containSimple").hide();
        $(".constraintForm").show();
    });

    /*******************************************
     *  Add a complex task to the list     
    ******************************************/
    var generalID = 1
    var specialID = 0
    $("#doneComplex").click(function () {
        addTask('ComplexTask');
    });
    /*******************************************
      *  Add a simple task to the list     
     ******************************************/
    $("#doneSimple").click(function () {
        addTask('SimpleTask');
    });

    function addTask(typeOf) {
        var simple = 'SimpleTask'
        var complex = 'ComplexTask'
        //take the elements
        if (typeOf === complex) {
            var name = document.getElementById("new-Ctaskname").value;
            var ctype = document.getElementById("new-Ctype").value;
            var description = document.getElementById("new-Ctaskdescr").value;
        }
        if (typeOf === simple) {
            var name = document.getElementById("new-Staskname").value;
            var mod = document.getElementById("new-Staskmode").value;
            var f1 = document.getElementById("new-func1").value;
            var agent1 = document.getElementById("new-agent1").value;
            var product1 = document.getElementById("new-product1").value;
            var resources1 = document.getElementById("new-res1").selectedOptions;
                resources1 = Array.from(resources1, (x)=>(x.value));
            var f2 = document.getElementById("new-func2").value;
            var agent2 = document.getElementById("new-agent2").value;
            var product2 = document.getElementById("new-product2").value;
            var resources2 = document.getElementById("new-res2").selectedOptions;
                resources2 = Array.from(resources1, (x)=>(x.value));
            // Needed only to show the name of the task on the page
            var f1name = $("#new-func1 option:selected").text();
            var agent1name = $("#new-agent1 option:selected").text();
            var product1name = $("#new-product1 option:selected").text();
            var resources1name = $("#new-res1 option:selected").text();
            var f2name = $("#new-func2 option:selected").text();
            var agent2name = $("#new-agent2 option:selected").text();
            var product2name = $("#new-product2 option:selected").text();
            var resources2name = $("#new-res2 option:selected").text();
            var description = document.getElementById("new-Staskdescr").value;
        }

        if ((typeOf === complex && (name === "" || ctype === "")) ||
            (typeOf === simple && (name === "" || mod === "" || f1 === ""))) {
            window.alert("Enter all the information of the task!")
        }
        else {
            document.getElementById("new-Ctaskname").value = '';
            document.getElementById("new-Ctype").value = '';
            document.getElementById("new-Ctaskdescr").value = '';
            document.getElementById("new-Staskname").value = '';
            document.getElementById("new-Staskmode").value = '';
            document.getElementById("new-func1").value = '';
            document.getElementById("new-func2").value = '';
            document.getElementById("new-agent1").value = '';
            document.getElementById("new-agent2").value = '';
            document.getElementById("new-product1").value = '';
            document.getElementById("new-product2").value = '';
            document.getElementById("new-Staskdescr").value = '';
            $(".mod").hide();
            $("#ms-new-res1").hide();
            $(".mod2").hide();
            $("#ms-new-res2").hide();

            //build the task object
            if (typeOf === complex)
                var tmp = new ComplexTask(generalID, name, ctype, [], description);
            if (typeOf === simple)
                var tmp = new SimpleTask(generalID, name, mod, f1, agent1, product1, resources1, f2, agent2, product2, resources2, description);

            //higher level task
            if (specialID === 0) {
                tasks.push(tmp);
            }
            //from an existent task
            else {
                //TODO refactor in a more efficient way
                checkOthers(tmp, tasks);
            }

            //Built the string to append to display the task
            var res = '';
            res += ("<div class='subtask' id=contain" + generalID + ">");
            if (typeOf === complex) {
                res += ("<label class='subtaskid' hidden>" + generalID + '</label>');
                res += ("<label> Task name: " + name + "</label> &nbsp; &nbsp;");
                res += ("<label>" + ctype + " </label> &nbsp;");
                res += ("<button class='complexST'>Add a complex sub-task</button>");
                res += ("<button class='simpleST'>Add a simple sub-task</button> &nbsp; &nbsp;")
                res += ("<button class='removeST'>Remove</button>")
            }
            if (typeOf === simple) {
                res += ("<label class='subtaskid' hidden>" + generalID + '</label>');
                res += ("<label> Task name: " + name + "</label> &nbsp;");
                res += ("<label> Collaborative modality: " + mod + "</label> &nbsp; &nbsp;");
                res += ("<button class='removeST'>Remove</button>")
                res += ("<div><label>  Function1: " + f1name + '</label> &nbsp; &nbsp;');
                res += ("<label>  Agent1: " + agent1name + '</label> &nbsp; &nbsp;');
                res += ("<label> Target Product: " + product1name + '</label></div>');
                res += ("<div><label>  Required Resources: " + resources1name + '</label></div>');
                if (f2 !== '') {
                    res += ("<div><label>  Function2: " + f2name + '</label> &nbsp; &nbsp;');
                    res += ("<label>  Agent2: " + agent2name + '</label> &nbsp; &nbsp;');
                    res += ("<label> Target Product: " + product2name + '</label></div>');
                    res += ("<div><label>  Required Resources: " + resources2name + '</label></div>');

                }
                res += ("</div>");
            }
            res += ("</div>");

            if (specialID === 0) {
                $("#result").append(res);
            }
            else {
                var el = '#contain' + specialID;
                $(el).append(res);
            }

            //add the new task to the list for add a constraint
            $('#new-t1').append('<option value=' + generalID + '>' + name + '</option>');

            //reset the variables for the next task
            generalID += 1;
            specialID = 0;
            $(".containComplex").hide();
            $(".containSimple").hide();
        }
    }

    //AUXILIARY FUNCTION to push the sub-task in the right list
    function checkOthers(tmp, itemList) {
        var higher = itemList.find(x => x.id === specialID);
        if (higher !== undefined) {
            var tmpList = higher.list;
            tmpList.push(tmp);
        }
        else {
            for (var index in itemList) {
                checkOthers(tmp, itemList[index].list);
            }
        }
    }

    /*******************************************
      *  Remove a task from the list     
     ******************************************/
     $(document).on("click", ".removeST", function () {
        var tmp = $(this).siblings(".subtaskid").html();
        tmp = parseInt(tmp);
        var otherIds = removeFromList(tmp, tasks);
        $(this).parent().remove();

        //remove the task also from the list for add a constraint
        $("#new-t1 option[value="+ tmp +"]").remove();
        //and all the constraint with that task or its subtask
        otherIds.push(tmp)
        var constrainsToRemove = [];
        for( var i=constraints.length; i--;) {
            var t1 = parseInt(constraints[i].t1);
            var t2 = parseInt(constraints[i].t2);
            var tmp1 = otherIds.find(x => x === t1);
            var tmp2 = otherIds.find(x => x === t2);
            if( tmp1 !== undefined || tmp2 !== undefined ) {
                constrainsToRemove.push(constraints[i].id)
                constraints.splice(i, 1);
            }
        }
        $('.constraintid').each(function(){
            var id = $(this).html();
            id = parseInt(id);
            var tmp = constrainsToRemove.find(x => x === id);
            if(tmp !== undefined) {
                $(this).parent().remove();
            }
        })
    });

    //AUXILIARY FUNCTION to remove the sub-task from the right list
    function removeFromList(tmp, itemList) {
        var higher = itemList.find(x => x.id === tmp);
        if (higher !== undefined) {
            var ids = saveSubtaskId(higher.list, [])
            var index = itemList.map(x => { return x.id;}).indexOf(tmp);
            itemList.splice(index, 1);
            return ids;
        }
        else {
            for (var i in itemList) {
                removeFromList(tmp, itemList[i].list);
            }
        }
    }
    //and add all its subtask to a list
    function saveSubtaskId(itemList, ids) {
        for(var i in itemList) {
            ids.push(itemList[i].id);
            if(itemList[i].list !== []) {
                //ids.concat(saveSubtaskId(itemList[i].list, []));
                ids.push.apply(ids, saveSubtaskId(itemList[i].list, []))
            }
        }
        return ids;
    }

    /**************************************
    *   Submit a process
    ***************************************/
    $("#sub").click(function () {
        //take the elements
        var processName = document.getElementById('new-processname').value;
        var processProduct = document.getElementById('new-processproduct').value;

        if (processName === "" || processProduct === "") {
            window.alert("Enter all the information of the process!");
        }

        else if (tasks.length === 0) {
            window.alert("Enter at least one task!");
        }

        else {
            var data = [];
            data.push({ 'name': processName, 'product': processProduct, 'tasks': tasks, 'constraints': constraints });
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({
                url: '/process/newProc/',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                data: js_data
            }).always(function () {
                location.replace("/process/");
            });
        }
    });

    /**************************************
    *   Delete a process
    **************************************/
    $(".removeProc").click(function () {
        var procId = $(this).siblings(".id").html();

        //create the json data
        var js_data = JSON.stringify(procId);
        $.ajax({
            url: '/process/',
            type: 'post',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: js_data
        }).always(function () {
            location.replace("/process/");
        });
    });

    /**************************************
    *  Add all the siblings to the
    *  select input while choosing
    *  the tasks of a constraint
    **************************************/
    $("#new-t1").change(function () {
        var idToMatch = parseInt(this.value);

        var siblings = getSiblings(idToMatch, tasks);

        $("#new-t2").find("option:gt(0)").remove();

        for (var i = 0; i < siblings.length; i++) {
            var t = siblings[i];
            if (t.id !== idToMatch) {
                $('#new-t2').append('<option value=' + t.id + '>' + t.name + '</option>');
            }
        }
    });
    //AUXILIARY FUNCTION to get the siblings of a task
    function getSiblings(idToMatch, listToCheck) {
        var higher = listToCheck.find(x => x.id === idToMatch);
        if (higher !== undefined) {
            return listToCheck;
        }
        else {
            for (var index in listToCheck) {
                return getSiblings(idToMatch, listToCheck[index].list);
            }
        }
    }

    /**************************************
    *   Save a constrains
    **************************************/
    var constraintID = 0
    $("#doneConstraint").click(function () {
        //take the elements
        var t1 = document.getElementById("new-t1").value;
        var t2 = document.getElementById("new-t2").value;

        // Needed only to show the name of the task on the page
        var t1name = $("#new-t1 option:selected").text();
        var t2name = $("#new-t2 option:selected").text();


        if (t1 === "" || t2 === "") {
            window.alert("Enter all the information of the constraint!")
        }
        else {
            document.getElementById("new-t1").value = '';
            document.getElementById("new-t2").value = '';

            //build the constraint object
            var tmp = new Constraint(constraintID, t1, t2);

            constraints.push(tmp);

            //Built the string to append to display the task
            var res = '';
            res += ("<div>");
            res += ("<label class='constraintid' hidden>" + constraintID + '</label>');
            res += ("<label> Task: " + t1name + "</label> &nbsp;");
            res += ("<label> BEFORE </label> &nbsp; &nbsp;");
            res += ("<label> Task: " + t2name + "</label> &nbsp; &nbsp;");
            res += ("<button class='delConstraint'>Remove</button>");
            res += ("</div>");

            $("#constraintlist").append(res);

            //reset the variables for the next constraint
            constraintID += 1;
            $(".constraintForm").hide();
        }
    });

    /**************************************
    *  Remove a constraint
    **************************************/
    $(document).on("click", ".delConstraint", function () {
        tmp = $(this).siblings(".constraintid").html();
        var index = constraints.map(x => { return x.id;}).indexOf(tmp);
        constraints.splice(index, 1);
        $(this).parent().remove();
    });

});