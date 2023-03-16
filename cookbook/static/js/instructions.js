function delete_instruction_row(row) {
    // Get the table row element to delete
    var row_to_remove = row.parentNode.parentNode;
    // Get the table body element
    var tbody = row_to_remove.parentNode;
    // Remove the row from the table
    tbody.removeChild(row_to_remove);
}
  
function add_instruction_row() {
    // get the table body element
    var tableBody = document.querySelector('#instructions-table tbody');

    // create a new row
    var newRow = document.createElement('tr');

    var instructionInput = document.createElement('input');
    instructionInput.className = 'form-control'
    instructionInput.type = 'text';
    instructionInput.name = 'instructions-' + (tableBody.children.length) + '-instruction';

    var removeButton = document.createElement('input');
    removeButton.type = "button";
    removeButton.value = "Remove";
    removeButton.addEventListener('click', function (){
        newRow.remove();
    })

    // create new form fields for the new row
    var newInstructionInput = document.createElement('td');
    newInstructionInput.appendChild(instructionInput);
  
    var newRemoveField = document.createElement('td');
    newRemoveField.appendChild(removeButton);

    // add the form fields to the new row
    newRow.appendChild(newInstructionInput);
    newRow.appendChild(newRemoveField);

    // add the new row to the table
    tableBody.appendChild(newRow);
}
