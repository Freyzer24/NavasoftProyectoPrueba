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

// Función para procesar el login
function processLogin(event) {
    event.preventDefault(); // Evitar que el formulario se envíe

    // Obtener los valores ingresados
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Verificar si es Admin
    if (username === admin.username && password === admin.password) {
        window.location.href = "indexadmin.html"; // Redirigir a la página de Admin
    }
    // Verificar si es Empleado
    else if (username === empleado.username && password === empleado.password) {
        window.location.href = "indexempleado.html"; // Redirigir a la página de Empleado
    } 
    // Si no coincide, mostrar un mensaje de error
    else {
        alert("Usuario o contraseña incorrectos");
    }
}