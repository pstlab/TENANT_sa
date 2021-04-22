// function to execute on page load
$(document).ready(function() {
        
    /**************************************
    *   Submit an aggregate resource
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var arName = document.getElementById('new-arname').value;
        //TODO list of resources

        if (arName === "") {
            window.alert("Enter all the information of the aggregate resource!");
        }

        else {
            var data = [];
            data.push({'name':arName});
            data.push('new');
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/sf/manageAggr/',
                type : 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/sf/manageAggr/");
            });
        }
    });

    /**************************************
    *   Delete an aggregate resource
    **************************************/
    $(".removeAR").click(function() {
        var arId = $(this).siblings(".id").html();
        var tmp = [arId, 'remove']

        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/sf/manageAggr/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/sf/manageAggr/");
        });
    });

    /**************************************
    *   Edit an aggregate resource
    *************************************/
    // Change the name
    $(".arname").change(function(){
        //Take the elements
        var arId = $(this).siblings(".id").html();
        var name = this.value;

        if (name === "") {
            window.alert("Enter all the information of the aggregate resource!");
        }

        else {
            var data = [];
            data.push(arId);
            data.push({'name':name});
            data.push('edit')
            //create the json data
            var js_data = JSON.stringify(data);
            $.ajax({                        
                url: '/sf/manageAggr/',
                type : 'post',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function() {
                location.replace("/sf/manageAggr/");
            });
        }
    });
    // Delete a resource from the aggregate resource
     $(".removeR").click(function() {
        var aggrRes = $(this).parent().siblings('.mainproperties').children(".id").html();
        var resId = $(this).siblings(".resid").html();
        var tmp = [];
        tmp.push({'aggrRes':aggrRes, 'resId':resId});
        tmp.push('removeRes')

        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/sf/manageAggr/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/sf/manageAggr/");
        });
    });
});