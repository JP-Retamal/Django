const $formulario = document.getElementById('registro-formulario');
const $inputs = document.querySelectorAll('.input');
const $checkBox = document.getElementById('registro-pasaporte');
const $selects = document.querySelectorAll('.contenedor-selects__select');
const $errores = document.querySelectorAll('.contenedor-inputs-error');

const validarRut = rut => {
    let runReverse = rut.substr(0, rut.indexOf('-')).split('').reverse();
    dvUsuario = rut.substr(rut.indexOf('-') + 1, 1)
    multiplicar = [2, 3, 4, 5, 6, 7, 2, 3];
    resultadoUno = 0;

    for (let i = 0; i < runReverse.length; i++) {
        resultadoUno += runReverse[i] * multiplicar[i]
    }

    let resultadoDos = Math.trunc(resultadoUno / 11)
    resultadoTres = resultadoDos * 11
    resta = resultadoUno - resultadoTres
    dvCorrecto = 11 - resta

    return (parseInt(dvUsuario, 10) === parseInt(dvCorrecto, 10)) ? true : false;
}

const inputLleno = {
    rut: false,
    fecha: false,
    nombre: false,
    paterno: false,
    materno: false,
    correo: false,
    celular: false,
    // region : false,
    // provincia : false,
    // comuna : false,
    contrasenia1: false,
    contrasenia1: false
};
const expresiones = {
    contrasenia: /^\w{6,12}$/,
    direccion: /^[A-z0-9#,\s]{1,50}$/,
    email: /^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+(?:[a-zA-Z]{2}|aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel)$/,
    fecha: /^[0-3][0-9]\/[0-1][0-9]\/\d{4}$/,
    numero: /^[0-9]{8,9}$/,
    run: /^\d{1,2}\.?\d{3}\.?\d{3}[-][0-9kK]{1}$/,
    texto: /^[a-zA-Z]+(([a-zA-Z ])?[a-zA-Z]*)*$/
};

const validarCampo = (input, expresion) => {

    let $inputName = input.target.name.substr(input.target.name.indexOf('-') + 1, input.target.name.length);

    // Valida que el input no sea el que contiene el rut
    if (input.target.name !== 'registro-rut' && input.target.name !== 'registro-contrasenia2') {
        // Evalua la expresion regular de acuerdo al valor del input
        if (expresion.test(input.target.value)) {
            // Se remueve el error cuando la expresion regular devuelve true
            document.querySelector(`div[name='registro-error-${$inputName}']`).classList.remove('block');
            // Agrega un borde verde
            document.querySelector(`input[name='registro-${$inputName}']`).classList.add('border-green-500', 'focus:border-green-500', 'border-2');
            inputLleno[$inputName] = true;
        } else {
            // En caso de que la expresion retorne false, se muestra el error
            document.querySelector(`div[name='registro-error-${$inputName}']`).classList.add('block');
            // Se remueve las clases verdes
            document.querySelector(`input[name='registro-${$inputName}']`).classList.remove('border-green-500', 'focus:border-green-500', 'border-2');
            // Se agrega un color rojo al input
            document.querySelector(`input[name='registro-fecha']`).classList.add('border-red-500', 'focus:border-red-500', 'border-2');
            inputLleno[$inputName] = false;
        }

        // Valida que el input sea el que contiene el rut
    } else if (input.target.name === 'registro-rut') {
        // Evalua la expresion regular de acuerdo al valor del input
        console.info(expresiones.run.test(input.target.value))
        if (expresiones.run.test(input.target.value)) {
            if ($checkBox.checked) {
                inputLleno[$inputName] = true;
            } else {
                (validarRut(input.target.value)) ? inputLleno[$inputName] = true: inputLleno[$inputName] = false;
            }

            if (inputLleno[$inputName] === true) {
                // Se remueve el error cuando la expresion regular devuelve true
                document.querySelector(`div[name='registro-error-${$inputName}']`).classList.remove('block');
                // Agrega un borde verde
                document.querySelector(`input[name='registro-${$inputName}']`).classList.add('border-green-500', 'focus:border-green-500', 'border-2');
            } else {
                document.querySelector(`div[name='registro-error-${$inputName}']`).classList.add('block');
                // Se remueve las clases verdes
                document.querySelector(`input[name='registro-${$inputName}']`).classList.remove('border-green-500', 'focus:border-green-500', 'border-2');
                // Se agrega un color rojo al input
                document.querySelector(`input[name='registro-${$inputName}']`).classList.add('border-red-500', 'focus:border-red-500', 'border-2');
            }
        } else {
            document.querySelector(`div[name='registro-error-${$inputName}']`).classList.add('block');
            // Se remueve las clases verdes
            document.querySelector(`input[name='registro-${$inputName}']`).classList.remove('border-green-500', 'focus:border-green-500', 'border-2');
            // Se agrega un color rojo al input
            document.querySelector(`input[name='registro-${$inputName}']`).classList.add('border-red-500', 'focus:border-red-500', 'border-2');
        }

        // Valida que el input sea el que contiene el la contrasenia2
    } else if (input.target.name === 'registro-contrasenia2') {
        if (input.target.value === $inputs[8].value) {
            // Evalua la expresion regular de acuerdo al valor del input
            document.querySelector(`div[name='registro-error-${$inputName}']`).classList.remove('block');
            document.querySelector(`input[name='registro-${$inputName}']`).classList.add('border-green-500', 'focus:border-green-500', 'border-2');
            inputLleno[$inputName] = true;
        } else {
            document.querySelector(`div[name='registro-error-${$inputName}']`).classList.add('block');
            // Se remueve las clases verdes
            document.querySelector(`input[name='registro-${$inputName}']`).classList.remove('border-green-500', 'focus:border-green-500', 'border-2');
            // Se agrega un color rojo al input
            document.querySelector(`input[name='registro-${$inputName}']`).classList.add('border-red-500', 'focus:border-red-500', 'border-2');
            inputLleno[$inputName] = false;
        }
    }

}

const validarFormulario = evento => {
    switch (evento.target.name) {
        case 'registro-rut':
            validarCampo(evento, expresiones.run)
            break;

        case 'registro-pasaporte':

            break;

        case 'registro-fecha':
            validarCampo(evento, expresiones.fecha)
            break;

        case 'registro-nombre':
            validarCampo(evento, expresiones.texto)
            break;

        case 'registro-paterno':
            validarCampo(evento, expresiones.texto)
            break;

        case 'registro-materno':
            validarCampo(evento, expresiones.texto)
            break;

        case 'registro-correo':
            validarCampo(evento, expresiones.email)
            break;

        case 'registro-celular':
            validarCampo(evento, expresiones.numero)
            break;

        case 'registro-direccion':
            validarCampo(evento, expresiones.direccion)
            break;

        case 'registro-region':
            validarCampo(evento, expresiones.run)
            break;

        case 'registro-provincia':
            validarCampo(evento, expresiones.run)
            break;

        case 'registro-comuna':
            validarCampo(evento, expresiones.run)
            break;

        case 'registro-contrasenia1':
            validarCampo(evento, expresiones.contrasenia)
            break;

        case 'registro-contrasenia2':
            validarCampo(evento, expresiones.contrasenia)
            break;
    }
};

$inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

const redireccionar = () => window.locationf = "http://127.0.0.1:8000/login/";

$formulario.addEventListener('submit', evento => {
    evento.preventDefault(); // Evita que el formulario se envie si no se encuentra completo.

    if (inputLleno.rut === true && inputLleno.fecha === true && inputLleno.nombre === true && inputLleno.paterno === true && inputLleno.materno === true &&
        inputLleno.correo === true && inputLleno.celular === true && inputLleno.direccion === true && inputLleno.contrasenia1 === true &&
        inputLleno.contrasenia2 === true) {
        $formulario.reset();
        document.querySelector('.contenedor-formulario-incompleto').classList.remove('block');
        document.querySelector('.contenedor-formulario-completo').classList.add('block');

        setTimeout(() => location.href = "http://127.0.0.1:8000/login/", 3000);
    } else {
        document.querySelector('.contenedor-formulario-completo').classList.remove('block');
        document.querySelector('.contenedor-formulario-incompleto').classList.add('block');
    }

});