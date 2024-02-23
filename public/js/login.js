document.addEventListener('DOMContentLoaded', function () {
    onPageLoad();
});



/* 
    * Función que muestra el mensaje de error
*/

const showError = (message, focusInput = null) => {
    const errorContainer = document.getElementById('error-container');
    const txtError = document.getElementById('txterror');
    
    txtError.textContent = message;
    errorContainer.classList.add('mostrando');

    setTimeout(() => {
        errorContainer.classList.remove('mostrando');
    }, 2000);

    if (focusInput) {
        focusInput.focus();
    }
};



/*
    * Función que se ejecuta al cargar la página
*/
function onPageLoad() {
    
    // Verificar si el email está guardado en localStorage
    const savedEmail = localStorage.getItem('savedEmail');
    const remember = localStorage.getItem('remember');

    if (remember === 'true' && savedEmail !== "") {
        document.getElementById('remember').checked = true;
        document.getElementById('email').value = savedEmail;
    }

    //Establecer foco inicial
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    if (emailInput.value === "") {
        emailInput.focus();
    } 
    else if (passwordInput.value === "") {
        passwordInput.focus();
    }

}

function remember_check() {
    const remember = document.getElementById('remember').checked;
    const email = document.getElementById('email').value;

    if (remember && email !== "" && validate_email(email)) {
        localStorage.setItem('remember', remember);
        localStorage.setItem('savedEmail', email);
    } else {
        localStorage.setItem('remember', remember);
        localStorage.setItem('savedEmail', '');
    }
}

function validate_email(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email !== "" && !emailRegex.test(email)) {
        return false;
    } else {
        return true;
    }
}

/* 
    * Función que se ejecuta al hacer click en el botón de Acceder
*/
function login(event) {
    const email = document.getElementById('email');
    let emailValido = validate_email(email.value);

    // Si email no es correcto, mostrar mensaje de error
    if (!emailValido){
        showError('El email no es correcto', email);
        event.preventDefault();
    }
    
}

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    document.getElementById('loader').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('response.status:', response.status);
        console.log('response.ok:', response.ok);
        if (!response.ok) {
            showError(response.message);
            // No necesitas event.preventDefault() aquí porque ya lo hiciste al principio
        }
        document.getElementById('loader').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    })
    .catch(error => {

        if (error instanceof Response) {
            // Si el error es una instancia de Response, puedes acceder a sus propiedades
            console.log('Código de estado HTTP:', error.status);
            console.log('Texto de la respuesta:', error.statusText);

            // También puedes intentar leer el cuerpo de la respuesta si es un JSON
            error.json().then(data => {
                console.log('Datos de la respuesta:', data);
            }).catch(jsonError => {
                console.error('Error al leer JSON de la respuesta:', jsonError);
            });
        }

        document.getElementById('loader').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
        showError(error.message, document.getElementById('password'));
    });
});