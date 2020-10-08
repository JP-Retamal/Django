$(function(){
    
    var special = new RegExp("^(?=.*[!@#$%&*])");
    var numbers = new RegExp("^(?=.*[0-9])");
    var  lower  = new RegExp("^(?=.*[a-z])");
    var len     = new RegExp("^(?=.{8,})");
    
    var regExp = [special, numbers, lower, len];
    var elementos = [$("#special"),$("#numbers"),$("#lower"),$("#len")];

    $("#registro-contrasenia1").on("keyup", function(){
        var pass = $("#registro-contrasenia1").val();

        for(var i = 0; i <5; i++){
            if(regExp[i].test(pass)){
                elementos[i].hide();
                $('#mensaje').css("background", "url(../img/check.png)");
            }else{
                elementos[i].show();
                $('#mensaje').css("background", "url(../img/check-.png)");
            }
        }
    
    });
    
});