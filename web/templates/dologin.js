    /*function getData(){
        document.getElementById("ok").style.display = "none";
        document.getElementById("un").style.display = "none";
        document.getElementById("waiting").style.display = "inline";
        var username = $('#username').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "username": username,
                "password": password
            });

        $.ajax({
            url:'/authenticate',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            success: function(response){

                },
            error: function(response){
                if(response['status']==401){
                document.getElementById("waiting").style.display = "none";
                document.getElementById("un").style.display = "inline";}
                 else{
                 document.getElementById("waiting").style.display = "none";
                document.getElementById("ok").style.display = "inline";
                window.location.href="http://127.0.0.1:5000/static/chatweb.html"
                  }}
        });
    }*/
    function getData(){
        $('#fail').hide();
        $('#ok').hide()
        $('#loading').show();
        var username = $('#username').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "username": username,
                "password": password
            });

        $.ajax({
            url:'/authenticate',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            success: function(response){
                $('#action').html(response['statusText']);
                $('#loading').hide();
                $('#ok').show();
                window.location.href="http://127.0.0.1:5000/"
            },
            error: function(response){
                //alert(JSON.stringify(response));
                $('#loading').hide();
                $('#fail').show();
            }
        });
    }
