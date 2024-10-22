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