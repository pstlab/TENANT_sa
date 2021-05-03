// function to execute on page load
$(document).ready(function() {
    const IND = "Independent";
    const SYN = "Synchronous";
    const SIM = "Simultaneous";
    const SUPP = "Supportive";

    var tasks = [];
    var constraints = [];

    var ComplexTask = class ComplexTask {
        constructor(id, name, list) {
            this.id = id;
            this.name = name;
            this.list = list;
            this.type = 'complex'
        }
    };

    var SimpleTask = class SimpleTask {
        constructor(id, name, modality) {
            this.id = id;
            this.name = name;
            this.modality = modality;
            this.type = 'simple'
        }

    };

    var Constraint = class Constraint {
        constructor(id, t1, t2) {
            this.id = id;
            this.t1 = t1;
            this.t2 = t2;
        }
    };

    $(".containComplex").hide();
    $(".containSimple").hide();
    $(".constraintForm").hide();

    /*******************************************
     *  Show the form for each complex task     
    ******************************************/
   //TODO refactorize to have only a parametric function
   $("#complex").click(function() {
    $(".containComplex").show();
    $(".containSimple").hide();
    $(".constraintForm").hide();
   });

   /*******************************************
     *  Show the form for each simple task     
    ******************************************/
    $("#simple").click(function() {
        $(".containComplex").hide();
        $(".containSimple").show();
        $(".constraintForm").hide();
    });

    /*******************************************
     *  Show the form for a complex task 
     * to be added from another complex task     
    ******************************************/
     $(document).on("click", ".complexST", function() {
        tmp = $(this).siblings(".ctaskid").html();
        specialID = Number(tmp)
        $(".containComplex").show();
        $(".containSimple").hide();
        $(".constraintForm").hide();
    });

    /*******************************************
     *  Show the form for a simple task 
     * to be added from another (complex) task     
    ******************************************/
     $(document).on("click", ".simpleST", function() {
        tmp = $(this).siblings(".ctaskid").html();
        specialID = Number(tmp)
        $(".containComplex").hide();
        $(".containSimple").show();
        $(".constraintForm").hide();
    });
    
    /**************************************
    *  Show the form to add a constraint
    **************************************/
     $("#constraint").click(function() {
        $(".containComplex").hide();
        $(".containSimple").hide();
        $(".constraintForm").show();
    });

    //TODO Refactor per unire i due metodi che cambiano di poche istruzioni
    /*******************************************
     *  Add a complex task to the list     
    ******************************************/
   var generalID = 1  
   var specialID = 0
   $("#doneComplex").click(function() {
       //take the element
       var name = document.getElementById("new-Ctaskname").value;
       
       if(name === "") {
           window.alert("Enter all the information of the task!")
       }
       else {
            document.getElementById("new-Ctaskname").value = '';
           //build the task object
           var tmp = new ComplexTask(generalID, name, []);

           //higher level task
           if(specialID === 0) {
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
           res += ("<label class='ctaskid' hidden>"+ generalID +'</label>');
           res += ("<label> Complex task name: " + name + "</label> &nbsp;");
           res += ("<button class='complexST'>Add a complex sub-task</button>");
           res += ("<button class='simpleST'>Add a simple sub-task</button></div>")
           if(specialID === 0) {
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
       }
   });  
   /*******************************************
     *  Add a simple task to the list     
    ******************************************/
    $("#doneSimple").click(function() {
        //take the element
        var name = document.getElementById("new-Staskname").value;
        var mod = document.getElementById("new-Staskmode").value;
        
        if(name === "" || mod === "") {
            window.alert("Enter all the information of the task!")
        }
        else {
            document.getElementById("new-Staskname").value = '';
            document.getElementById("new-Staskmode").value = '';
            //build the task object
            var tmp = new SimpleTask(generalID, name, mod);
 
            //higher level task
            if(specialID === 0) {
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
            res += ("<label class='staskid' hidden>"+ generalID +'</label>');
            res += ("<label> Simple task name: " + name + "</label> &nbsp;");
            res += ("<label> Collaborative modality: " + mod + "</label>");
            if(specialID === 0) {
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
            $(".containSimple").hide();
        }
    });

   //AUXILIARY FUNCTION to push the sub-task in the right list
   function checkOthers(tmp, itemList) {
    var higher = itemList.find(x => x.id === specialID);
    if(higher !== undefined) {
     var tmpList = higher.list;
     tmpList.push(tmp);
    }
    else {
         for (var index in itemList) {
             checkOthers(tmp, itemList[index].list);
         }
     }
   }
    /**************************************
    *   Submit a process
    ***************************************/
    $("#sub").click(function(){
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
            data.push({'name':processName, 'product':processProduct, 'tasks':tasks, 'constraints':constrains});
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/process/newProc/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/process/");
            });
        }
    });

    /**************************************
    *   Delete a process
    **************************************/
    $(".removeProc").click(function() {
        var procId = $(this).siblings(".id").html();

        //create the json data
        var js_data = JSON.stringify(procId);
        $.ajax({                        
            url: '/process/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/process/");
        });
    });

    /**************************************
    *  Add all the siblings to the
    *  select input while choosing
    *  the tasks of a constraint
    **************************************/
   $("#new-t1").change(function() {
        var idToMatch = parseInt(this.value);

        var siblings = getSiblings(idToMatch, tasks);

        $("#new-t2").find("option:gt(0)").remove();
        
        for(var i=0; i<siblings.length; i++) {
            var t = siblings[i];
            if(t.id !== idToMatch){
                $('#new-t2').append('<option value=' + t.id + '>' + t.name + '</option>');
            }
        }
   });
   //AUXILIARY FUNCTION to get the siblings of a task
   function getSiblings(idToMatch, listToCheck) {
        var higher = listToCheck.find(x => x.id === idToMatch);
        if(higher !== undefined) {
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
     $("#doneConstraint").click(function() {
        //take the elements
        var t1 = document.getElementById("new-t1").value;
        var t2 = document.getElementById("new-t2").value;

        // Needed only to show the name of the task on the page
        var t1name = document.getElementById("new-t1");
        t1name = t1name.options[t1name.selectedIndex].text;
        var t2name = document.getElementById("new-t2");
        t2name = t2name.options[t2name.selectedIndex].text;

        
        if(t1 === "" || t2 === "") {
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
            res += ("<label class='constraintid' hidden>"+ constraintID +'</label>');
            res += ("<label> Task: " + t1name + "</label> &nbsp;");
            res += ("<label> BEFORE </label> &nbsp; &nbsp;");
            res += ("<label> Task: " + t2name + "</label> &nbsp;");
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

    /**************************************
    *   Modify a constraint
    **************************************/
    
});