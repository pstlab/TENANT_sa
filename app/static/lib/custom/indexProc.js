// function to execute on page load
$(document).ready(function() {
    
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

        /*
        else if (processList.length === 0) {
            window.alert("Enter at least one task!");
        } */

        else {
            var data = [];
            data.push({'name':processName, 'product':processProduct});
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
    *   Edit a process
    *************************************/
     $("#edit").click(function() {
        //take the elements
        var processId = document.getElementById('processid').value;

        var processName = document.getElementById('processname').value;
        var processProduct = document.getElementById('processproduct').value;

        if (processName === "" || processProduct === "") {
            window.alert("Enter all the information of the process!");
        }

        else {
            var data = [];
            data.push(processId)
            data.push({'name':processName, 'processProduct':processProduct});

            var myurl = '/process/viewProc/' + processId;
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: myurl,
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/process/");
            });
        }
    }); 
    
});