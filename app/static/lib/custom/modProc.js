// function to execute on page load
$(document).ready(function() {
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