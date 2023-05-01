function delete_ingredient_row(row) {
    // Get the table row element to delete
    var row_to_remove = row.parentNode.parentNode;
    // Get the table body element
    var tbody = row_to_remove.parentNode;
    // Remove the row from the table
    tbody.removeChild(row_to_remove);
}

function add_ingredient_row() {
    // get the table body element
    var tableBody = document.querySelector('#ingredients-table tbody');

    // create a new row
    var newRow = document.createElement('tr');

    var measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)", "Item"]

    // create input fields for each column
    var ingredientInput = document.createElement('input');
    ingredientInput.className = 'form-control'
    ingredientInput.type = 'text';
    ingredientInput.name = 'ingredients-' + (tableBody.children.length) + '-ingredient';
    ingredientInput.id = 'ingredients-' + (tableBody.children.length) + '-ingredient';
    ingredientInput.required = true;

    
    var amountInput = document.createElement('input');
    amountInput.className = 'form-control'
    amountInput.type = 'number';
    amountInput.step = 'any';
    amountInput.name = 'ingredients-' + (tableBody.children.length) + '-amount';
    amountInput.id = 'ingredients-' + (tableBody.children.length) + '-amount';
    amountInput.required = true;
    
    var unitSelect = document.createElement('select');
    unitSelect.name = 'ingredients-' + (tableBody.children.length) + '-unit';
    unitSelect.id = 'ingredients-' + (tableBody.children.length) + '-unit';
    unitSelect.className = 'form-control'
    unitSelect.required = true;

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
