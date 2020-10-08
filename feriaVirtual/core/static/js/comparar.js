$(document).ready(function() {

	$('#registro-contrasenia2').keyup(function() {

        var pass1 = $('#registro-contrasenia1').val();
        var pass2 = $('#registro-contrasenia2').val();
        
        if(pass2 == pass1){
            $("#pass2").hide();
            $('#mensaje2').css("background", "url(../img/check.png)");
        }else{
            $("#pass2").show();
        }

	});

});