// function to execute on page load
$(document).ready(function() {    
        
    /**************************************
    *   Submit a resource
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var resourceName = document.getElementById('new-resourcename').value;
        var type = document.getElementById('new-resourcetype').value;
        var aggregate = document.getElementById('new-aggregate_resource').value;

        //TODO funzioni della risorsa operatore

        if (resourceName === "" || type === "") {
            window.alert("Enter all the information of the resource!");
        }

        else {
            var data = [];
            data.push({'name':resourceName, 'type':type, 'aggregate':aggregate});
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
            data.push({'name':resourceName, 'type':type, 'aggregate':aggregate});

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