// Escuchar eventos de los botones
document.getElementById('agregarBtn').addEventListener('click', agregarTarea);
document.getElementById('exportarBtn').addEventListener('click', exportarXLSX); // Agregamos el evento del botón de exportación
document.getElementById('exportarPdfBtn').addEventListener('click', exportarPDF); // Evento para exportar a PDF

const tareas = [];

function agregarTarea() {
    const nombre = document.getElementById('nombre').value;
    const fechaInicio = new Date(document.getElementById('fechaInicio').value);
    const fechaFin = new Date(document.getElementById('fechaFin').value);
    const porcentaje = document.getElementById('porcentaje').value;

    if (!nombre || !fechaInicio || !fechaFin || !porcentaje) {
        alert('Por favor, complete todos los campos.');
        return;
    }

    tareas.push({ nombre, fechaInicio, fechaFin, porcentaje: parseInt(porcentaje) });
    mostrarTareas();
    limpiarCampos();
}

function mostrarTareas() {
    const tareasDiv = document.getElementById('tareas');
    const timelineDiv = document.getElementById('timeline');
    tareasDiv.innerHTML = '';
    timelineDiv.innerHTML = '';

    let minDate = new Date(Math.min(...tareas.map(t => t.fechaInicio)));
    let maxDate = new Date(Math.max(...tareas.map(t => t.fechaFin)));
    const totalDays = Math.ceil((maxDate - minDate) / (1000 * 60 * 60 * 24)) + 1;

    // Crear la línea de tiempo
    let currentMonth = new Date(minDate);
    let months = [];
    let currentMonthDays = [];

    // Recorremos todos los días entre las fechas de inicio y fin
    for (let i = 0; i < totalDays; i++) {
        const day = new Date(minDate);
        day.setDate(day.getDate() + i);

        // Si cambiamos de mes o de año, agregamos el mes anterior y reiniciamos el array de días
        if (day.getMonth() !== currentMonth.getMonth() || day.getFullYear() !== currentMonth.getFullYear()) {
            months.push({ 
                month: currentMonth.getMonth(), 
                year: currentMonth.getFullYear(),
                days: currentMonthDays 
            });
            currentMonthDays = []; // Reiniciar los días del mes
            currentMonth = day; // Cambiar al nuevo mes
        }

        // Agregar el día al mes correspondiente
        currentMonthDays.push(day);
    }

    // Asegurarse de agregar el último mes
    if (currentMonthDays.length > 0) {
        months.push({ 
            month: currentMonth.getMonth(), 
            year: currentMonth.getFullYear(),
            days: currentMonthDays 
        });
    }

    // Mostrar los meses en la línea de tiempo
    months.forEach(month => {
        const monthDiv = document.createElement('div');
        monthDiv.className = 'month';
        const monthName = new Date(month.days[0]).toLocaleString('default', { month: 'long' });
        const year = month.year;  // Obtener el año

        monthDiv.innerHTML = `<div class="month-header">${monthName} ${year}</div>`;
        timelineDiv.appendChild(monthDiv);

        // Mostrar los días de ese mes
        month.days.forEach(day => {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'day';
            dayDiv.innerHTML = `<div class="day-number">${day.getDate()}</div>`;
            monthDiv.appendChild(dayDiv);
        });
    });

    // Mostrar las tareas
    tareas.forEach(tarea => {
        const tareaDiv = document.createElement('div');
        tareaDiv.className = 'gantt-row';

        const barraAncho = Math.ceil((tarea.fechaFin - tarea.fechaInicio) / (1000 * 60 * 60 * 24)) * (100 / totalDays);
        const inicioOffset = Math.ceil((tarea.fechaInicio - minDate) / (1000 * 60 * 60 * 24)) * (100 / totalDays);

        // Definir el color de la barra basado en el porcentaje
        let barraColor;
        if (tarea.porcentaje === 100) {
            barraColor = 'blue';
        } else if (tarea.porcentaje >= 65) {
            barraColor = 'green';
        } else if (tarea.porcentaje >= 34) {
            barraColor = 'yellow';
        } else {
            barraColor = 'red';
        }

        tareaDiv.innerHTML = `
            <div class="details">
                <div contenteditable="true">${tarea.nombre}</div>
                <div>${tarea.fechaInicio.toLocaleDateString()}</div>
                <div>${tarea.fechaFin.toLocaleDateString()}</div>
                <div contenteditable="true">${tarea.porcentaje}%</div>
            </div>
            <div class="bar" style="width: ${barraAncho}%; margin-left: ${inicioOffset}%; background-color: ${barraColor};"></div>
        `;

        tareasDiv.appendChild(tareaDiv);
    });
}

function limpiarCampos() {
    document.getElementById('nombre').value = '';
    document.getElementById('fechaInicio').value = '';
    document.getElementById('fechaFin').value = '';
    document.getElementById('porcentaje').value = '';
}

// Función para exportar a PDF
function exportarPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text(`Diagrama de Gantt - Proyecto`, 20, 20);

    // Datos de las tareas
    const tareas = Array.from(document.querySelectorAll('.gantt-row'));
    let yPosition = 30;
    
    tareas.forEach((row, index) => {
        const taskName = row.querySelector('span').textContent;
        const startDate = row.querySelectorAll('span')[1].textContent;
        const endDate = row.querySelectorAll('span')[2].textContent;
        const assigned = row.querySelectorAll('span')[3].textContent;
        const status = row.querySelector('.gantt-bar').classList[1];

        doc.setFontSize(12);
        doc.text(`${taskName} - ${startDate} - ${endDate} - ${assigned} - ${status}`, 20, yPosition);
        yPosition += 10;
        
        if (yPosition > 270) {
            doc.addPage();
            yPosition = 20;
        }
    });

    doc.save('Gantt_Proyecto.pdf');
}

// Función para exportar a XLSX
function exportarXLSX() {
    const tareas = Array.from(document.querySelectorAll('.gantt-row'));
    
    const data = tareas.map(row => {
        const taskName = row.querySelector('span').textContent;
        const startDate = row.querySelectorAll('span')[1].textContent;
        const endDate = row.querySelectorAll('span')[2].textContent;
        const assigned = row.querySelectorAll('span')[3].textContent;
        const status = row.querySelector('.gantt-bar').classList[1];

        return [taskName, startDate, endDate, assigned, status];
    });

    const ws = XLSX.utils.aoa_to_sheet([['Tarea', 'Fecha de Inicio', 'Fecha de Fin', 'Encargado', 'Estado'], ...data]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Gantt");

    XLSX.writeFile(wb, 'Gantt_Proyecto.xlsx');
}
