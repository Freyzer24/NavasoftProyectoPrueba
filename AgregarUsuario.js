// Definir la clase Empleado
class Empleado {
    constructor(nombre, telefono, correo, rol, usuario, contrasena) {
        this.nombre = nombre;
        this.telefono = telefono;
        this.correo = correo;
        this.rol = rol;
        this.usuario = usuario;
        this.contrasena = contrasena;
    }

    // Método para mostrar información del empleado (sin contraseña por seguridad)
    mostrarInfo() {
        return `Nombre: ${this.nombre}, Teléfono: ${this.telefono}, Correo: ${this.correo}, Rol: ${this.rol}, Usuario: ${this.usuario}`;
    }
}

// Arreglo para almacenar empleados
const empleados = [];

// Referencia al formulario
const formEmpleado = document.getElementById('formEmpleado');
const listaEmpleados = document.getElementById('listaEmpleados');

// Manejar el envío del formulario
formEmpleado.addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar recargar la página

    // Obtener los valores de los campos
    const nombre = document.getElementById('nombre').value;
    const telefono = document.getElementById('telefono').value;
    const correo = document.getElementById('correo').value;
    const rol = document.getElementById('rol').value;
    const usuario = document.getElementById('usuario').value;
    const contrasena = document.getElementById('contrasena').value;

    // Crear un nuevo empleado
    const nuevoEmpleado = new Empleado(nombre, telefono, correo, rol, usuario, contrasena);

    // Agregar el empleado al arreglo
    empleados.push(nuevoEmpleado);

    // Limpiar el formulario
    formEmpleado.reset();

    // Actualizar la lista de empleados en la página
    actualizarListaEmpleados();
});

// Función para actualizar la lista de empleados
function actualizarListaEmpleados() {
    // Limpiar la lista actual
    listaEmpleados.innerHTML = '';

    // Mostrar cada empleado en la lista
    empleados.forEach((empleado, index) => {
        const li = document.createElement('li');
        li.textContent = `${index + 1}. ${empleado.mostrarInfo()}`;
        listaEmpleados.appendChild(li);
    });
}
