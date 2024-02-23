document.addEventListener('DOMContentLoaded', function () {
    const addDayBtn = document.querySelector('.add-day-btn');
    const daysContainer = document.querySelector('.days-container');

    addDayBtn.addEventListener('click', function () {
        const newDay = document.createElement('div');
        newDay.classList.add('day');
        newDay.innerHTML = `
            <h3>Día ${daysContainer.children.length + 1}</h3>
            <div class="exercises-container">
                <div class="exercise">
                    <label for="exercise-name">Ejercicio:</label>
                    <input type="text" id="exercise-name" placeholder="Nombre del ejercicio">
                    <label for="exercise-sets">Series:</label>
                    <input type="number" id="exercise-sets" placeholder="Número de series">
                    <label for="exercise-reps">Repeticiones:</label>
                    <input type="number" id="exercise-reps" placeholder="Número de repeticiones">
                </div>
                <!-- Puedes agregar más ejercicios aquí -->
            </div>
            <button class="add-exercise-btn">Añadir Ejercicio</button>
        `;
        daysContainer.appendChild(newDay);
    });

    daysContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('add-exercise-btn')) {
            const exercisesContainer = event.target.previousElementSibling;
            const newExercise = document.createElement('div');
            newExercise.classList.add('exercise');
            newExercise.innerHTML = `
                <label for="exercise-name">Ejercicio:</label>
                <input type="text" id="exercise-name" placeholder="Nombre del ejercicio">
                <label for="exercise-sets">Series:</label>
                <input type="number" id="exercise-sets" placeholder="Número de series">
                <label for="exercise-reps">Repeticiones:</label>
                <input type="number" id="exercise-reps" placeholder="Número de repeticiones">
            `;
            exercisesContainer.appendChild(newExercise);
        }
    });
});
