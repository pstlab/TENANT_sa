var AGENTS = ["Worker", "Cobot"]

// function to execute on page load
$(document).ready(function() {   
    
    var Capability = class Capability {
        constructor(type, name) {
            this.type = type;
            this.name = name;
        }
    };

    var capabilities = [];

    //The already saved capabilities of the resource
    var old = document.getElementsByClassName("oldCapId");
    Array.from(old).forEach(elem => {
        capabilities.push(new Capability('old', elem.innerText || elem.textContent));
    });

    $(".capabilityForm").hide();
    $(".new-capability").hide();
    $(".select-capability").hide();

    /**************************************
     *  Show the form of capability
     *************************************/
    $("#new-resourcetype").change(function() {
        if( AGENTS.includes(this.value) ) {
            $(".capabilityForm").show();
        }
        else {
            $(".capabilityForm").hide();
            $(".new-capability").hide();
            $(".select-capability").hide();
        }
    });

    /**************************************
     *  Show the form to add a
     *  NEW CAPABILITY
     **************************************/
    $("#addNew").click(function() {
        $(".new-capability").show();
        $(".select-capability").hide();
    });

    /**************************************
     *  Show the form to add a
     *  PRE EXISTING CAPABILITY
     **************************************/
     $("#selectOld").click(function() {
        $(".new-capability").hide();
        $(".select-capability").show();
    });

    /***************************************
     *  ADD A NEW CAPABILITY
     * from the new resource
     * or the modified one
     **************************************/
    $("#new-doneNew").click(function() {
        addNew('new-capabilityname', '#result');
    });

    $("#doneNew").click(function() {
        addNew('capabilityname', '#resCap');
    });

    function addNew(element, result) {
        var name = document.getElementById(element).value;
        if(name === "") {
            window.alert("Enter all the information of the capability!")
        }
        else {            
            var tmp = new Capability('new', name);
            capabilities.push(tmp);

            //Built the string to append to display the capability
            var res = '';
            res += ("<div class='capability'>");
            res += ("<label class='capabilityId'>" + name + "</label> &nbsp;");
            res += ("<button class='delCapability'>Remove</button>");
            res += ("</div>")
            $(result).append(res);
            
            //reset the variables for the next capability
            document.getElementById(element).value = '';
            $(".new-capability").hide();
        }
    }


    /***************************************
     *  ADD A PRE EXISTING CAPABILITY
     * from the new resource
     * or the modified one
     **************************************/
     $("#new-doneSelect").click(function() {
        addSelected('new-selected-cap', "#result");
    });

    $("#doneSelect").click(function() {
        addSelected('selected-cap', "#resCap");
    });

    function addSelected(element, result) {
        var capabilityName = document.getElementById(element).value;

        if(capabilityName === "") {
            window.alert("Select one capability!")
        }
        else {
            var tmp = new Capability('old', capabilityName);
            capabilities.push(tmp);

            //Built the string to append to display the capability
            var res = '';
            res += ("<div class='capability'>");
            res += ("<label class='capabilityId'>" + capabilityName + "</label> &nbsp;");
            res += ("<button class='delCapability'>Remove</button>");
            res += ("</div>");
            $(result).append(res);

            //reset the variables for the next capability
            var index = document.getElementById(element).selectedIndex;
            document.getElementById(element).options[index].remove();
            document.getElementById(element).selectedIndex = "-1";
            $(".select-capability").hide();
        }
    }
        
    /**************************************
    *   Submit a resource
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var resourceName = document.getElementById('new-resourcename').value;
        var resourceDescription = document.getElementById('new-resourcedescr').value;
        var resourceCapacity = document.getElementById('new-resourcecapacity').value || "1";
        var type = document.getElementById('new-resourcetype').value;
        var aggregate = document.getElementById('new-aggregate_resource').value;

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            if(!AGENTS.includes(type))
                capabilities = []
            data.push({'name':resourceName, 'description':resourceDescription, 'capacity':resourceCapacity, 'type':type, 'aggregate':aggregate, 'capabilities':capabilities});
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
        var resourceCapacity = document.getElementById('resourcecapacity').value || "1";
        //TODO remove || innerText if resource type edit will be reimplemented
        var type = document.getElementById('resourcetype').value || document.getElementById('resourcetype').innerText || document.getElementById('resourcetype').textContent;
        var aggregate = document.getElementById('aggregate_resource').value;

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            data.push(resourceId)
            if(!AGENTS.includes(type)){
                capabilities = []
            }
            data.push({'name':resourceName, 'description':resourceDescription, 'capacity':resourceCapacity, 'type':type, 'aggregate':aggregate, 'capabilities':capabilities});

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

    // Manage the capability form
    $("#resourcetype").change(function() {
        if( AGENTS.includes(this.value) ) {
            $("#mod-capabilityForm").show();
        }
        else {
            $("#mod-capabilityForm").hide();
        }
    });

    /**************************************
    *  Remove a capability
    **************************************/
     $(document).on("click", ".delCapability", function () {
        tmp = $(this).siblings(".capabilityId").html();
        var index = capabilities.map(x => { return x.name;}).indexOf(tmp);
        capabilities.splice(index, 1);
        $(this).parent().remove();
    });
});