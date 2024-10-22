// Definimos el nodo de la lista enlazada
class Nodo {
    constructor(data) {
        this.data = data;  // El objeto con los datos del registro
        this.next = null;  // Puntero al siguiente nodo
    }
}

// Definimos la clase de la lista enlazada
class ListaEnlazada {
    constructor() {
        this.head = null;  // Inicialmente no hay nodos en la lista
    }

    // Método para agregar un nodo al final de la lista
    agregar(data) {
        const nuevoNodo = new Nodo(data);
        if (!this.head) {
            this.head = nuevoNodo;  // Si la lista está vacía, el nuevo nodo es el primero
        } else {
            let actual = this.head;
            while (actual.next) {
                actual = actual.next;  // Avanza al último nodo
            }
            actual.next = nuevoNodo;  // Añade el nuevo nodo al final
        }
        // Guardamos la lista en el localStorage
        this.guardarEnLocalStorage();
    }

    // Método para buscar un nodo por nombre y devolver su referencia
    buscarPorNombre(nombre) {
        let actual = this.head;
        while (actual) {
            if (actual.data.nombre === nombre) {
                return actual;  // Devuelve el nodo si encuentra el nombre
            }
            actual = actual.next;
        }
        return null;  // Retorna null si no encuentra coincidencia
    }

    // Método para mostrar la lista enlazada
    mostrar() {
        let actual = this.head;
        let html = '<h2>Registros Guardados:</h2><ul>';
        while (actual) {
            html += `<li>${JSON.stringify(actual.data)}</li>`;
            actual = actual.next;
        }
        html += '</ul>';
        document.getElementById('listContainer').innerHTML = html;
    }

    // Método para convertir la lista enlazada en un array
    toArray() {
        let actual = this.head;
        const array = [];
        while (actual) {
            array.push(actual.data);
            actual = actual.next;
        }
        return array;
    }

    // Método para reconstruir la lista enlazada desde un array
    fromArray(array) {
        array.forEach(data => this.agregar(data));
    }

    // Guardar la lista en localStorage
    guardarEnLocalStorage() {
        const listaArray = this.toArray();
        localStorage.setItem('listaEnlazada', JSON.stringify(listaArray));
    }

    // Cargar la lista desde localStorage
    cargarDesdeLocalStorage() {
        const listaGuardada = localStorage.getItem('listaEnlazada');
        if (listaGuardada) {
            const array = JSON.parse(listaGuardada);
            this.fromArray(array);
            this.mostrar();  // Mostramos la lista cargada
        }
    }
}

// Inicializamos la lista enlazada
const listaEnlazada = new ListaEnlazada();

// Variable global para saber si se está editando un registro existente
let nodoAEditar = null;

// Cargar la lista enlazada desde localStorage al iniciar la página
window.onload = function() {
    listaEnlazada.cargarDesdeLocalStorage();
};

function guardarDatos() {
    // Capturamos los valores del formulario
    const nombre = document.getElementById('nombre').value;
    const telefono = document.getElementById('telefono').value;
    const correo = document.getElementById('correo').value;
    const usuario = document.getElementById('usuario').value;
    const rol = document.getElementById('rol').value;
    const password = document.getElementById('password').value;
    
    // Creamos el objeto con los valores capturados
    const registro = {
        nombre: nombre,
        telefono: telefono,
        correo: correo,
        usuario: usuario,
        rol: rol,
        password: password
    };

    if (nodoAEditar) {
        // Si estamos editando un registro existente, actualizamos el nodo
        nodoAEditar.data = registro;
        nodoAEditar = null;  // Reiniciamos la variable después de editar
        // Guardamos los cambios en localStorage
        listaEnlazada.guardarEnLocalStorage();
    } else {
        // Si no estamos editando, agregamos un nuevo nodo a la lista
        listaEnlazada.agregar(registro);
    }

    // Mostramos la lista enlazada en la página
    listaEnlazada.mostrar();

    // Limpiamos el formulario
    resetForm();
}

function editarDatos() {
    const nombre = document.getElementById('nombre').value;

    // Buscamos el nodo por el nombre
    const nodoEncontrado = listaEnlazada.buscarPorNombre(nombre);

    if (nodoEncontrado) {
        // Rellenamos los campos con los datos del nodo encontrado
        document.getElementById('nombre').value = nodoEncontrado.data.nombre;
        document.getElementById('telefono').value = nodoEncontrado.data.telefono;
        document.getElementById('correo').value = nodoEncontrado.data.correo;
        document.getElementById('usuario').value = nodoEncontrado.data.usuario;
        document.getElementById('rol').value = nodoEncontrado.data.rol;
        document.getElementById('password').value = nodoEncontrado.data.password;

        // Guardamos una referencia al nodo que estamos editando
        nodoAEditar = nodoEncontrado;
    } else {
        alert("No se encontró un registro con ese nombre.");
    }
}

function resetForm() {
    // Limpiamos ambos formularios
    document.getElementById('registroForm1').reset();
    document.getElementById('registroForm2').reset();
    nodoAEditar = null;  // Reiniciamos la referencia de edición
}










//Perfil
function cambiarFoto(input, imgElementId) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(imgElementId).src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        // Puedes definir una imagen por defecto si no se selecciona ninguna
        document.getElementById(imgElementId).src = './imagenes/default-avatar.png'; // Cambia esta ruta por la de tu imagen por defecto
    }
  }
  
  // Añadiendo event listeners a los inputs de archivo
  document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoDosInput = document.getElementById('fotoDos');
  
    // Cambiar la foto del primer perfil
    fotoInput.addEventListener('change', function() {
        cambiarFoto(fotoInput, 'img');
    });
  
    // Cambiar la foto del segundo perfil
    fotoDosInput.addEventListener('change', function() {
        cambiarFoto(fotoDosInput, 'imgDos');
    });
  });




//Login
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





//Diagrama Gantt
let tasks = [
    ['1', 'Tarea Inicial', 'Grupo 1', new Date(2024, 9, 1), new Date(2024, 9, 5), null, 100, null]
];

// Cargar la librería de Google Charts
google.charts.load('current', { 'packages': ['gantt'] });
google.charts.setOnLoadCallback(drawChart);

// Función para dibujar el gráfico
function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'ID de la tarea');
    data.addColumn('string', 'Nombre de la tarea');
    data.addColumn('string', 'Recurso');
    data.addColumn('date', 'Inicio');
    data.addColumn('date', 'Fin');
    data.addColumn('number', 'Duración');
    data.addColumn('number', 'Porcentaje completado');
    data.addColumn('string', 'Dependencia');

    // Añadir las tareas
    data.addRows(tasks);

    var options = {
        height: 400,
        gantt: {
            trackHeight: 30
        }
    };

    var chart = new google.visualization.Gantt(document.getElementById('gantt_chart'));
    chart.draw(data, options);
}

// Función para agregar nuevas tareas
document.getElementById('task_form').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar recargar la página
    let taskName = document.getElementById('task_name').value;
    let taskStart = new Date(document.getElementById('task_start').value);
    let taskEnd = new Date(document.getElementById('task_end').value);
    let taskId = (tasks.length + 1).toString();
    let taskCompletion = parseInt(document.getElementById('task_completion').value) || 0;

    tasks.push([taskId, taskName, 'Grupo ' + taskId, taskStart, taskEnd, null, taskCompletion, null]);

    // Redibujar el gráfico con la nueva tarea
    drawChart();

    // Limpiar el formulario
    document.getElementById('task_form').reset();
});

// Función para descargar las tareas
document.getElementById('downloadBtn').addEventListener('click', function() {
    const formattedTasks = tasks.map(task => {
        return [
            `ID: "${task[0]}"`, // ID
            `Nombre: "${task[1]}"`, // Nombre
            `Recurso: "${task[2]}"`, // Recurso
            `Fecha de inicio: "${task[3].toISOString().split('T')[0]}"`, // Inicio
            `Fecha de fin: "${task[4].toISOString().split('T')[0]}"`, // Fin
            `Porcentaje completado: "${task[6]}"` // Porcentaje completado
        ].join(', ');
    }).join('\n');

    // Crear un blob con el texto
    const blob = new Blob([formattedTasks], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tareas.csv'; // Nombre del archivo

    // Simular clic en el enlace
    document.body.appendChild(a);
    a.click();

    // Limpiar
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// Cerrar el modal si se hace clic fuera del contenido del modal
window.addEventListener("click", function(event) {
    if (event.target === confirmationModal) {
        confirmationModal.style.display = "none";
        isConfirmed = false;
    }
});


//Gestión de usuarios
function showModal(user, role, task) {
    var modal = document.getElementById("userModal");
    var content = document.getElementById("modalContent");
    content.innerHTML = `
    <p><strong>Usuario:</strong> ${user}</p>
    <p><strong>Rol:</strong> ${role}</p>
    <p><strong>Tareas:</p></strong> ${task}</p>
`;

     modal.style.display = "flex"; // Mostrar el modal
}

function closeModal() {
    document.getElementById("userModal").style.display = "none"; // Ocultar el modal
}

// Cerrar el modal si el usuario hace clic fuera del contenido del modal
window.onclick = function(event) {
    var modal = document.getElementById("userModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Función para mostrar u ocultar secciones según el rol del usuario
function mostrarSeccionesPorRol(rol) {
    const adminSection = document.getElementById('adminSection');
    const userSection = document.getElementById('userSection');

    if (rol === 'admin') {
        adminSection.style.display = 'block';  // Muestra la sección de administradores
        userSection.style.display = 'none';    // Oculta la sección de usuarios estándar (si es necesario)
    } else if (rol === 'usuario') {
        adminSection.style.display = 'none';   // Oculta la sección de administradores
        userSection.style.display = 'block';   // Muestra la sección de usuarios
    } else {
        // Caso de manejo de otros roles o usuarios no autenticados
        adminSection.style.display = 'none';
        userSection.style.display = 'block';
    }
}

// Ejemplo: al cargar la página, detectamos el rol
window.onload = function() {
    // Simulación: obtener el rol del usuario (podría venir del backend o localStorage)
    const rolUsuario = 'admin';  // Ejemplo: 'admin' o 'usuario'
    mostrarSeccionesPorRol(rolUsuario);
};

function iniciarAplicacion() {
    const registro = listaEnlazada.buscarPorNombre('NombreUsuario');
    if (registro) {
        mostrarSeccionesPorRol(registro.data.rol);
    }
}

// Cargar la configuración al iniciar la página
window.onload = function() {
    listaEnlazada.cargarDesdeLocalStorage();
    iniciarAplicacion();
};