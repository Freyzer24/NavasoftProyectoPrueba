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