// Crear objeto Admin
const admin = {
    username: "admin",
    password: "admin123"
};

// Crear objeto Empleado
const empleado = {
    username: "empleado",
    password: "empleado123"
};

// Crear objeto Visualizador
const visualizador = {
    username: "visualizador",
    password: "visualizador123"
};

// Crear objeto Super Administrador
const supadministrador = {
    username: "supadministrador",
    password: "supadministrador"
};

// Función para procesar el login
function processLogin(event) {
    event.preventDefault(); // Evitar que el formulario se envíe

    // Obtener los valores ingresados
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Referencias a los elementos del formulario
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');

    // Resetear los estilos y mensajes previos
    usernameInput.classList.remove('error');
    passwordInput.classList.remove('error');
    usernameError.style.display = 'none';
    passwordError.style.display = 'none';

    let hasError = false; // Bandera para saber si hay algún error

    // Verificar si es Admin
    if (username === admin.username && password === admin.password) {
        window.location.href = "indexadmin.html"; // Redirigir a la página de Admin
    }
    // Verificar si es Empleado
    else if (username === empleado.username && password === empleado.password) {
        window.location.href = "indexempleado.html"; // Redirigir a la página de Empleado
    }
    // Verificar si es Visualizador
    else if (username === visualizador.username && password === visualizador.password) {
        window.location.href = "indexempleado.html"; // Redirigir a la página de Visualizador
    }
    // Verificar si es Super Administrador
    else if (username === supadministrador.username && password === supadministrador.password) {
        window.location.href = "indexempleado.html"; // Redirigir a la página de Super Admin
    } 
   
    // Si no coincide, mostrar los errores
    else {
        if (username !== admin.username && username !== empleado.username && username !== visualizador.username && username !== supadministrador.username) {
            usernameInput.classList.add('error');
            usernameError.style.display = 'block';
            hasError = true;
        }

        if (password !== admin.password && password !== empleado.password && password !== visualizador.password && password !== supadministrador.password) {
            passwordInput.classList.add('error');
            passwordError.style.display = 'block';
            hasError = true;
        }
    }
}
