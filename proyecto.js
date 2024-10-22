// Seleccionamos todos los botones de eliminar
const deleteButtons = document.querySelectorAll('.delete-btn');

// Iteramos sobre cada botón y le añadimos un evento de clic
deleteButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Obtenemos la fila (tr) correspondiente al botón
        const row = this.closest('tr');

        // Eliminamos la fila de la tabla
        row.remove();
    });
});
