// function to execute on page load
$(document).ready(function() {

    /**************************************
    *   Add the product families to the list
    ***************************************/
   //TODO
    
        
    /**************************************
    *   Submit a product
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var productName = document.getElementById('new-productname').value;
        var productFamily = document.getElementById('new-productfamily').value;
        //TODO aggiungere le product families

        if (productName === "") {
            window.alert("Enter all the information of the product!");
        }

        else {
            var data = [];
            data.push({'name':productName, 'productfamily':productFamily});
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/products/newProd/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/products/");
            });
        }
    });

    /**************************************
    *   Delete a product
    ***************************************/
    $(".removeProd").click(function() {
        var demId = $(this).siblings(".id").html();

        //create the json data
        var js_data = JSON.stringify(demId);
        $.ajax({                        
            url: '/products/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/products/");
        });
    });

    /**************************************
    *   Edit a product
    **************************************/
     $("#edit").click(function() {
        //take the elements
        var productId = document.getElementById('productid').value;

        var productName = document.getElementById('productname').value;
        var productFamily = document.getElementById('productfamily').value;

        if (productName === "") {
            window.alert("Enter all the information of the product!");
        }

        else {
            var data = [];
            data.push(productId)
            data.push({'name':productName, 'productfamily':productFamily});

            var myurl = '/products/editProd/' + productId;
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: myurl,
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/products/");
            });
        }
    }); 
    
});