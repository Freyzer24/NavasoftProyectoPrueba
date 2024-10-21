let tasks = [
    ['1', 'Tarea Inicial', 'Grupo 1', new Date(2024, 9, 1), new Date(2024, 9, 5), null, 100, null]
];

// Cargar la librería de Google Charts
google.charts.load('current', {'packages': ['gantt']});
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
const form = document.getElementById("task_form");
const confirmationModal = document.getElementById("confirmation_modal");
const closeModal = document.querySelector(".close");
let isConfirmed = false;

// Mostrar el modal cuando se intenta enviar el formulario
form.addEventListener("submit", function(event) {
    if (!isConfirmed) {
        event.preventDefault();
        confirmationModal.style.display = "block"; // Mostrar el modal
    }
});

// Confirmar la acción
document.querySelector(".confirm").addEventListener("click", function() {
    isConfirmed = true;
    confirmationModal.style.display = "none";
    form.submit(); // Enviar el formulario
});

// Cancelar la acción
document.querySelector(".cancel").addEventListener("click", function() {
    confirmationModal.style.display = "none";
    isConfirmed = false; // Cancelar la confirmación
});

// Cerrar el modal al hacer clic en la "X"
closeModal.addEventListener("click", function() {
    confirmationModal.style.display = "none";
    isConfirmed = false;
});

// Cerrar el modal si se hace clic fuera del contenido del modal
window.addEventListener("click", function(event) {
    if (event.target === confirmationModal) {
        confirmationModal.style.display = "none";
        isConfirmed = false;
    }
});
function descargarArchivo() {
    // Aquí puedes especificar la URL del archivo que quieres descargar
    const url = 'ruta/a/tu/archivo.pdf'; // Reemplaza con la ruta correcta
    const link = document.createElement('a');
    link.href = url;
    link.download = 'Diagrama de Gantt.pdf'; // Nombre con el que se guardará el archivo
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }