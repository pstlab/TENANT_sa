// function to execute on page load
$(document).ready(function() {   
    
    var AGENTS = ["Worker", "Cobot"]

    var Function = class Function {
        constructor(id, type, name) {
            this.id = id;
            this.type = type;
            this.name = name;
        }
    };

    var functions = [];

    //The already saved functions of the resource
    var functionID = 0
    var old = document.getElementsByClassName("oldFunId");
    Array.from(old).forEach(elem => {
        functions.push(new Function(functionID, 'old', elem.getAttribute('value')));
        //Add the local label id
        var res = document.createElement('label');
        res.className = 'functionId';
        res.innerHTML = functionID;
        res.hidden = true;
        elem.parentNode.appendChild(res)
        functionID += 1;
    });

    $(".functionForm").hide();
    $(".new-function").hide();
    $(".select-function").hide();

    /**************************************
     *  Show the form of function
     *************************************/
    $("#new-resourcetype").change(function() {
        if( AGENTS.includes(this.value) ) {
            $(".functionForm").show();
        }
        else {
            $(".functionForm").hide();
            $(".new-function").hide();
            $(".select-function").hide();
        }
    });

    /**************************************
     *  Show the form to add a
     *  NEW FUNCTION
     **************************************/
    $("#addNew").click(function() {
        $(".new-function").show();
        $(".select-function").hide();
    });

    /**************************************
     *  Show the form to add a
     *  PRE EXISTING FUNCTION
     **************************************/
     $("#selectOld").click(function() {
        $(".new-function").hide();
        $(".select-function").show();
    });

    /***************************************
     *  ADD A NEW FUNCTION
     * from the new resource
     * or the modified one
     **************************************/
    $("#new-doneNew").click(function() {
        addNew('new-functionname', '#result');
    });

    $("#doneNew").click(function() {
        addNew('functionname', '#resFunct');
    });

    function addNew(element, result) {
        var name = document.getElementById(element).value;
        if(name === "") {
            window.alert("Enter all the information of the function!")
        }
        else {
            document.getElementById(element).value = '';

            var tmp = new Function(functionID, 'new', name);
            functions.push(tmp);

            //Built the string to append to display the function
            var res = '';
            res += ("<div class='function'>");
            res += ("<label class='functionId' hidden>" + functionID + '</label>');
            res += ("<label>" + name + "</label> &nbsp;");
            res += ("<button class='delFunction'>Remove</button>");
            res += ("</div>")
            $(result).append(res);

            //reset the variables for the next function
            functionID += 1;
            $(".new-function").hide();
        }
    }


    /***************************************
     *  ADD A PRE EXISTING FUNCTION
     * from the new resource
     * or the modified one
     **************************************/
     $("#new-doneSelect").click(function() {
        addSelected('new-selected-f', "#result");
    });

    $("#doneSelect").click(function() {
        addSelected('selected-f', "#resFunct");
    });

    function addSelected(element, result) {
        var fid = document.getElementById(element).value;

        if(fid === "") {
            window.alert("Select one function!")
        }
        else {
            var tmp = new Function(functionID, 'old', fid);
            functions.push(tmp);

            //Built the string to append to display the function
            var fname = $("#" + element + " option:selected").text();
            var res = '';
            res += ("<div class='function'>");
            res += ("<label class='functionId' hidden>" + functionID + '</label>');
            res += ("<label>" + fname + "</label> &nbsp;");
            res += ("<button class='delFunction'>Remove</button>");
            res += ("</div>");
            $(result).append(res);

            //reset the variables for the next function
            functionID += 1;
            $(".select-function").hide();
        }
    }
        
    /**************************************
    *   Submit a resource
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var resourceName = document.getElementById('new-resourcename').value;
        var resourceDescription = document.getElementById('new-resourcedescr').value;
        var type = document.getElementById('new-resourcetype').value;
        var aggregate = document.getElementById('new-aggregate_resource').value;

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            if(!AGENTS.includes(type))
                functions = []
            data.push({'name':resourceName, 'description':resourceDescription, 'type':type, 'aggregate':aggregate, 'functions':functions});
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/sf/newRes/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/sf/");
            });
        }
    });

    /**************************************
    *   Delete a resource
    ***************************************/
    $(".removeRes").click(function() {
        var resId = $(this).siblings(".id").html();
        var resType = $(this).siblings(".type").html();

        var data = [{'id':resId, 'type':resType}, "removeRes"];

        //create the json data
        var js_data = JSON.stringify(data);
        $.ajax({                        
            url: '/sf/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/sf/");
        });
    });

    /**************************************
    *   Edit a resource
    ***************************************/
     $("#edit").click(function() {
        //take the elements
        var resourceId = document.getElementById('resourceid').value;

        var resourceName = document.getElementById('resourcename').value;
        var resourceDescription = document.getElementById('resourcedescription').value;
        var type = document.getElementById('resourcetype').value;
        var aggregate = document.getElementById('aggregate_resource').value;

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            data.push(resourceId)
            if(!AGENTS.includes(type))
                functions = []
            data.push({'name':resourceName, 'description':resourceDescription, 'type':type, 'aggregate':aggregate, 'functions':functions});

            var myurl = '/sf/editRes/' + resourceId;
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: myurl,
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/sf/");
            });
        }
    });

    // Manage the function form
    $("#resourcetype").change(function() {
        if( AGENTS.includes(this.value) ) {
            $("#mod-functionForm").show();
        }
        else {
            $("#mod-functionForm").hide();
        }
    });
    
    /**************************************
    *  Remove a function
    **************************************/
     $(document).on("click", ".delFunction", function () {
        tmp = $(this).siblings(".functionId").html();
        var index = functions.map(x => { return x.id;}).indexOf(tmp);
        functions.splice(index, 1);
        $(this).parent().remove();
    });
});