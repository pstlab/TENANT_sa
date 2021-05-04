// function to execute on page load
$(document).ready(function() {    

    var functions = [];

    var old = document.getElementsByClassName("functionId");
    Array.from(old).forEach(elem => functions.push({type:'old', name:elem.getAttribute('value')}));

    var Function = class Function {
        constructor(type, name) {
            this.type = type;
            this.name = name;
        }
    };

    $(".functionForm").hide();
    $(".new-function").hide();
    $(".select-function").hide();

    /**************************************
     *  Show the form of function
     *************************************/
    $("#new-resourcetype").change(function() {
        if( this.value === "Operator") {
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

            var tmp = new Function('new', name);
            functions.push(tmp);

            //Built the string to append to display the function
            var res = '';
            res += ("<div class='function'>");
            // TODO add an id to identify which function i have to remove
            //res += ("<label class='ctaskid' hidden>"+ generalID +'</label>');
            res += ("<label>" + name + "</label> &nbsp;");
            res += ("</div>")
            $(result).append(res);

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
            var tmp = new Function('old', fid);
            functions.push(tmp);

            //Built the string to append to display the function
            var fname = $("#" + element + " option:selected").text();
            var res = '';
            res += ("<div class='function'>");
            // TODO add an id to identify which function i have to remove
            //res += ("<label class='ctaskid' hidden>"+ generalID +'</label>');
            res += ("<label>" + fname + "</label> &nbsp;");
            res += ("</div>")
            $(result).append(res);

            $(".select-function").hide();
        }
    }
        
    /**************************************
    *   Submit a resource
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var resourceName = document.getElementById('new-resourcename').value;
        var type = document.getElementById('new-resourcetype').value;
        var aggregate = document.getElementById('new-aggregate_resource').value;

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            data.push({'name':resourceName, 'type':type, 'aggregate':aggregate, 'functions':functions});
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

        var tmp =[resId, "removeRes"];
        //create the json data
        var js_data = JSON.stringify(tmp);
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
        var type = document.getElementById('resourcetype').value;
        var aggregate = document.getElementById('aggregate_resource').value;

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            data.push(resourceId)
            data.push({'name':resourceName, 'type':type, 'aggregate':aggregate, 'functions':functions});

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

    
});