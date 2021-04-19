// function to execute on page load
$(document).ready(function() {    

    /***********************************************
    *   Add the processes when a product is chosen
    *  in adding a new demand
    ************************************************/
   $("#new-demandproduct").change(function() {
        //set the previous value
        sessionStorage.setItem('selectedtem', this.value);

       //take the product
       var product = document.getElementById('new-demandproduct').value;
       data = [product, 'askForProcesses']
       var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/demands/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.reload();
            });
   });

   /***********************************************
    *   Add the processes when a product is chosen
    *  in modifying a demand
    ************************************************/
    $("#demandproduct").change(function() {
        //set the previous value
        sessionStorage.setItem('selectedtem', this.value);

       //take the product and the demand id
       //var product = document.getElementById('demandproduct').value;
       var product = this.value;
       var demId = document.getElementById('demandid').value;

       var myurl = '/demands/editDem/' + demId;
       data = [demId, product, 'askForProcesses']
       var js_data = JSON.stringify(data);
            $.ajax({                        
                url: myurl,
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.reload();
            });
   });
    
        
    /**************************************
    *   Submit a demand
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var demandName = document.getElementById('new-demandname').value;
        var type = document.getElementById('new-demandtype').value;
        var product = document.getElementById('new-demandproduct').value;
        var quantity = document.getElementById('new-demandquantity').value;
        var process = document.getElementById('new-demandprocess').value;

        //remove the session item
        sessionStorage.removeItem('selectedtem');

        if (demandName === "" || type === "" || product === "" || quantity === "") {
            window.alert("Enter all the information of the demand!");
        }

        else {
            var data = [];
            data.push({'name':demandName, 'type':type, 'product':product, 'quantity':quantity, 'process':process});
            data.push('new');
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/demands/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/demands/");
            });
        }
    });

    /**************************************
    *   Delete a demand
    ***************************************/
    $(".removeDem").click(function() {
        var demId = $(this).siblings(".id").html();

        //remove the session item
        sessionStorage.removeItem('selectedtem');

        var tmp =[demId, "removeDem"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/demands/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/demands/");
        });
    });

    /**************************************
    *   Edit a demand
    ***************************************/
     $("#edit").click(function() {
        //take the elements
        var demandId = document.getElementById('demandid').value;

        var demandName = document.getElementById('demandname').value;
        var type = document.getElementById('demandtype').value;
        var product = document.getElementById('demandproduct').value;
        var quantity = document.getElementById('demandquantity').value;
        var process = document.getElementById('demandprocess').value;

        //remove the session item
        sessionStorage.removeItem('selectedtem');

        if (demandName === "" || type === "" || product === "" || quantity === "") {
            window.alert("Enter all the information of the demand!");
        }

        else {
            var data = [];
            data.push(demandId)
            data.push({'name':demandName, 'type':type, 'product':product, 'quantity':quantity, 'process':process});

            var myurl = '/demands/editDem/' + demandId;
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: myurl,
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/demands/");
            });
        }
    });

    /************************************************
     * Clear the variables after each link
     ************************************************/
    $(".links").click(function() {
        //remove the session item
        sessionStorage.removeItem('selectedtem');
    });

    
});