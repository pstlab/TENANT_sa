// function to execute on page load
$(document).ready(function() {

    /**************************************
    *   Add the products to the list
    ***************************************/
   //TODO
    
        
    /**************************************
    *   Submit a demand
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var demandName = document.getElementById('new-demandname').value;
        var type = document.getElementById('new-demandtype').value;
        var product = document.getElementById('new-demandproduct').value;
        var quantity = document.getElementById('new-demandquantity').value;

        if (demandName === "" || type === "" || product === "" || quantity === "") {
            window.alert("Enter all the information of the demand!");
        }

        else {
            var data = [];
            data.push({'name':demandName, 'type':type, 'product':product, 'quantity':quantity});
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

        if (demandName === "" || type === "" || product === "" || quantity === "") {
            window.alert("Enter all the information of the demand!");
        }

        else {
            var data = [];
            data.push(demandId)
            data.push({'name':demandName, 'type':type, 'product':product, 'quantity':quantity});

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

    
});