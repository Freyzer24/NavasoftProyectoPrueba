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