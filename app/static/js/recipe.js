function deleteRow(r) {
    var i = r.parentNode.parentNode.rowIndex;
    document.getElementById("ingredients-table").deleteRow(i);
}

function add_row() {
    // get the table body element
    var tableBody = document.querySelector('#ingredients-table tbody');

    // create a new row
    var newRow = document.createElement('tr');

    var measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)"]

    // create input fields for each column
    var ingredientInput = document.createElement('input');
    ingredientInput.className = 'form-control'
    ingredientInput.type = 'text';
    ingredientInput.name = 'ingredients-' + (tableBody.children.length + 1) + '-ingredient';

    
    var amountInput = document.createElement('input');
    amountInput.className = 'form-control'
    amountInput.type = 'number';
    amountInput.step = 'any';
    amountInput.name = 'ingredients-' + (tableBody.children.length + 1) + '-amount';
    
    var unitSelect = document.createElement('select');
    unitSelect.name = 'ingredients-' + (tableBody.children.length + 1) + '-unit';
    unitSelect.className = 'form-control'

    var removeButton = document.createElement('input');
    removeButton.type = "button";
    removeButton.value = "Remove";
    removeButton.addEventListener('click', function (){
        newRow.remove();
    })

    // add options to the select element
    for (var i = 0; i < measuring_units.length; i++) {
        var option = document.createElement('option');
        option.value = measuring_units[i];
        option.text = measuring_units[i];
        unitSelect.appendChild(option);
    }

    // create new form fields for the new row
    var newIngredientField = document.createElement('td');
    newIngredientField.appendChild(ingredientInput);

    var newAmountField = document.createElement('td');
    newAmountField.appendChild(amountInput);

    var newUnitField = document.createElement('td');
    newUnitField.appendChild(unitSelect);
    
    var newRemoveField = document.createElement('td');
    newRemoveField.appendChild(removeButton);

    // add the form fields to the new row
    newRow.appendChild(newIngredientField);
    newRow.appendChild(newAmountField);
    newRow.appendChild(newUnitField);
    newRow.appendChild(newRemoveField);

    // add the new row to the table
    tableBody.appendChild(newRow);
}
