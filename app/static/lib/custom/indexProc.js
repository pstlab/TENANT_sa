// function to execute on page load
$(document).ready(function() {
    const IND = "Independent";
    const SYN = "Synchronous";
    const SIM = "Simultaneous";
    const SUPP = "Supportive";

    var tasks = [];

    var ComplexTask = class ComplexTask {
        constructor(id, name, list) {
            this.id = id;
            this.name = name;
            this.list = list;
            this.type = 'complex'
        }
    };

    $(".containComplex").hide();
    $("#containSimple").hide();

    /*******************************************
     *  Show the form for each complex task     
    ******************************************/
   $("#complex").click(function() {
    $(".containComplex").show();
    $("#containSimple").hide();
   });

   /*******************************************
     *  Show the form for each simple task     
    ******************************************/
    $("#simple").click(function() {
        $(".containComplex").hide();
        $("#containSimple").show();
    });

    /*******************************************
     *  Show the form for a complex task 
     * to be added from another complex task     
    ******************************************/
     $(document).on("click", ".complexST", function() {
        tmp = $(this).siblings(".ctaskid").html();
        specialID = Number(tmp)
        $(".containComplex").show();
        $("#containSimple").hide();
    });

    /*******************************************
     *  Add a complex task to the list     
    ******************************************/
   var generalID = 1  
   var specialID = 0
   $("#doneComplex").click(function() {
       //take the element
       var name = document.getElementById("new-taskname").value;
       document.getElementById("new-taskname").value = '';
       
       if(name === "") {
           window.alert("Enter all the information of the task!")
       }
       else {
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
           res += ("<div id=contain" + generalID + ">");
           res += ("<label class='ctaskid' hidden>"+ generalID +'</label>');
           if(specialID !== 0) {
               res += ('&nbsp;&nbsp;');
            }
           res += ("<label> Complex task name: " + name + "</label> &nbsp;");
           res += ("<button class='complexST'>Add a complex sub-task</button>");
           res += ("<button class='simpleST'>Add a simple sub-task</button></div></br>")
           if(specialID === 0) {
                $("#result").append(res);
           }
           else {
               var el = '#contain' + specialID;
               $(el).append(res);
           }

           //reset the variables for the next task
           generalID += 1;
           specialID = 0;
           $(".containComplex").hide();
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
        //TODO aggiungere i task probabilmente li tieni qui temporanei e poi mandi tutto

        if (processName === "" || processProduct === "") {
            window.alert("Enter all the information of the process!");
        }

        
        else if (tasks.length === 0) {
            window.alert("Enter at least one task!");
        }

        else {
            var data = [];
            data.push({'name':processName, 'product':processProduct, 'tasks':tasks});
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
    
});