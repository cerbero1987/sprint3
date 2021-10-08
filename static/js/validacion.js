
function validar_formulario(){
  
    vUsuario = document.getElementById("usuario").value;

    vEmail =  document.getElementById("email").value;
    var expReg = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;

    vPassword =  document.getElementById("password").value;
    
    if ( vUsuario == "" ){
        alert("El campo usuario no debe estar vacío.");
        return false
    }else if ( vUsuario.length < 8 ){
        alert("El campo usuario debe tener mínimo 8 caracteres.");
        return false
    }else if ( vEmail == "" ){
        alert("El campo del correo electrónico no debe estar vacío.");
        return false
    }else if ( expReg.test( vEmail ) == false ) {
        alert("El campo del correo electrónico no válido.");
        return false
    }else if ( vPassword == "" ){
        alert("El campo Contraseña no debe estar vacío.");
        return false
    }else if ( vPassword.length < 8 ){
        alert("El campo Contraseña debe tener mínimo 8 caracteres.");
        return false
    }
}

function mostrarPassword(){
    var obj = document.getElementById("password");
    obj.type = "text";
}

function ocultarPassword(){
    var obj = document.getElementById("password");
    obj.type = "password";
}