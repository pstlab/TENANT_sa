// function to execute on page load
$(document).ready(function() {
        
    /**************************************
    *   Submit an aggregate resource
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var arName = document.getElementById('new-arname').value;
        var partOf = document.getElementById('new-ar-aggregate').value;
        //TODO list of resources

        if (arName === "") {
            window.alert("Enter all the information of the aggregate resource!");
        }

        else {
            var data = [];
            data.push({'name':arName, 'ar':partOf});
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
        var partOf = $(this).siblings('.ar-aggregate').value;

        if (name === "") {
            window.alert("Enter all the information of the aggregate resource!");
        }

        else {
            var data = [];
            data.push(arId);
            data.push({'name':name, 'ar':partOf});
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
    // Change the aggregate resource of an aggregate resource
    $(".ar-aggregate").change(function(){
        //Take the elements
        var arId = $(this).siblings(".id").html();
        var name = $(this).siblings(".arname").val();
        var partOf = this.value;

        if (name === "") {
            window.alert("Enter all the information of the aggregate resource!");
        }

        else {
            var data = [];
            data.push(arId);
            data.push({'name':name, 'ar':partOf});
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

    // Delete an aggregate resource from the aggregate resource
    $(".removeAR").click(function() {
        var aggrRes = $(this).parent().siblings('.mainproperties').children(".id").html();
        var aResId = $(this).siblings(".aResid").html();
        var tmp = [];
        tmp.push({'aggrRes':aggrRes, 'aggResId':aResId});
        tmp.push('removeAggRes')

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