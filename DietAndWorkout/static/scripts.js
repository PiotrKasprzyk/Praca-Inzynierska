document.getElementById('toggle-theme').addEventListener('click', function () {
    document.body.classList.toggle('dark-theme');
});

document.getElementById('add-meal').addEventListener('click', function () {
    const mealsContainer = document.getElementById('meals');
    const mealForm = document.createElement('div');
    mealForm.classList.add('form-group');
    mealForm.innerHTML = `
        <label>Meal Type</label><br>
        <select name="meal_type">
            <option value="Śniadanie">Śniadanie</option>
            <option value="Drugie śniadanie">Drugie śniadanie</option>
            <option value="Obiad">Obiad</option>
            <option value="Kolacja">Kolacja</option>
            <option value="Deser">Deser</option>
        </select><br>
        <label>Name</label><br>
        <input type="text" name="name" size="32"><br>
        <label>Recipe</label><br>
        <textarea name="recipe" rows="3"></textarea><br>
    `;
    mealsContainer.appendChild(mealForm);
});

document.getElementById('add-exercise').addEventListener('click', function () {
    const exercisesContainer = document.getElementById('exercises');
    const exerciseForm = document.createElement('div');
    exerciseForm.classList.add('form-group');
    exerciseForm.innerHTML = `
        <label>Day</label><br>
        <select name="day">
            <option value="Monday">Monday</option>
            <option value="Tuesday">Tuesday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thursday">Thursday</option>
            <option value="Friday">Friday</option>
            <option value="Saturday">Saturday</option>
            <option value="Sunday">Sunday</option>
        </select><br>
        <label>Name</label><br>
        <input type="text" name="name" size="32"><br>
        <label>Reps</label><br>
        <input type="text" name="reps" size="32"><br>
        <label>Sets</label><br>
        <input type="text" name="sets" size="32"><br>
    `;
    exercisesContainer.appendChild(exerciseForm);
});
