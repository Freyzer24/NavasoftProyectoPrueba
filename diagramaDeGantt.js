// Array para almacenar las tareas
let tasks = [];

// Al enviar el formulario
document.getElementById('task_form').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar recargar la página
    
    // Obtener los valores del formulario
    let taskName = document.getElementById('task_name').value;
    let taskStart = new Date(document.getElementById('task_start').value);
    let taskEnd = new Date(document.getElementById('task_end').value);
    let taskCompletion = parseInt(document.getElementById('task_completion').value) || 0;
    
    // Validar datos
    if (!taskName || !taskStart || !taskEnd || isNaN(taskCompletion)) {
        alert("Por favor, complete todos los campos correctamente.");
        return;
    }

    // Añadir la tarea al array
    tasks.push({ 
        name: taskName, 
        start: taskStart, 
        end: taskEnd, 
        completion: taskCompletion 
    });

    // Redibujar el gráfico de Gantt
    drawChart();

    // Limpiar el formulario
    document.getElementById('task_form').reset();
});

// Función para generar el diagrama de Gantt
function drawChart() {
    const ganttChart = document.getElementById('gantt_chart');
    ganttChart.innerHTML = ''; // Limpiar el gráfico antes de volver a dibujarlo

    // Obtener las fechas más tempranas y más tardías para establecer el rango de fechas
    let minDate = new Date(Math.min(...tasks.map(t => t.start)));
    let maxDate = new Date(Math.max(...tasks.map(t => t.end)));

    // Convertir las fechas a formato de año, mes, día
    const startYear = minDate.getFullYear();
    const endYear = maxDate.getFullYear();

    // Crear el contenedor para el gráfico
    const ganttTimeline = document.createElement('div');
    ganttTimeline.className = 'gantt-timeline';
    ganttChart.appendChild(ganttTimeline);

    // Generar las secciones de años, meses y días
    let currentDate = new Date(minDate);
    let months = [];

    // Crear las divisiones para los años y meses
    for (let year = startYear; year <= endYear; year++) {
        const yearDiv = document.createElement('div');
        yearDiv.className = 'year';
        yearDiv.innerText = year;
        ganttTimeline.appendChild(yearDiv);

        for (let month = 0; month < 12; month++) {
            const monthDiv = document.createElement('div');
            monthDiv.className = 'month';
            monthDiv.innerText = new Date(year, month).toLocaleString('default', { month: 'short' });
            ganttTimeline.appendChild(monthDiv);

            for (let day = 1; day <= 31; day++) {
                const dayDiv = document.createElement('div');
                dayDiv.className = 'day';
                dayDiv.innerText = day;
                ganttTimeline.appendChild(dayDiv);
            }
        }
    }

    // Dibujar las barras para cada tarea
    tasks.forEach(task => {
        const taskBar = document.createElement('div');
        taskBar.className = 'task-bar';

        // Calcular el ancho y desplazamiento de la barra
        const taskStartDay = Math.floor((task.start - minDate) / (1000 * 60 * 60 * 24));
        const taskEndDay = Math.floor((task.end - minDate) / (1000 * 60 * 60 * 24));
        const taskDuration = taskEndDay - taskStartDay;
        
        taskBar.style.left = `${taskStartDay * 20}px`;  // Ajustar la posición
        taskBar.style.width = `${taskDuration * 20}px`;  // Ajustar la longitud

        // Ajustar el color de la barra según el porcentaje completado
        if (task.completion === 100) {
            taskBar.style.backgroundColor = 'green';
        } else if (task.completion >= 65) {
            taskBar.style.backgroundColor = 'yellow';
        } else {
            taskBar.style.backgroundColor = 'red';
        }

        // Añadir la barra de tarea al gráfico
        ganttChart.appendChild(taskBar);
    });
}
