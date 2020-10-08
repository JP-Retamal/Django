var correo = document.getElementById('login-correoa').Value;
var contrasenia = document.getElementById('login-contrasenia').Value;

exprersion = /\w+@\w+\.+[a-z]/;

if(correo === "" || contrasenia === ""){
    alert("Todos los campods son obligatorios");
    return false;
}
else if(!exprersion.test(correo)){
    alert("El email ingresado no es valido");
    return false;
}

