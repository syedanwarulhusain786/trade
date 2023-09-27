// Get references to the select and input elements
var transactionTypeSelect = document.getElementById("transactionType");
var chequeNumberInput = document.getElementById("chequeNumber");
var clearanceDateInput = document.getElementById("clearanceDate");
var chequeDate = document.getElementById("chequeDate");

transactionTypeSelect.addEventListener("change", function() {
    // Check the selected value and enable/disable fields accordingly
    if (transactionTypeSelect.value === "Cheque") {
        chequeNumberInput.disabled = false;
        clearanceDateInput.disabled = false;
        chequeDate.disabled = false;

    } else {
        chequeNumberInput.disabled = true;
        clearanceDateInput.disabled = true;
        chequeDate.disabled = true;

    }
});




// Get a reference to the date input element
const dateInput = document.getElementById('cashjournal_date');
const bankjournal_date = document.getElementById('bankjournal_date');


// Create a new Date object for today's date
const today = new Date();

// Get the year, month, and day in the format "YYYY-MM-DD"
const year = today.getFullYear();
const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
const day = today.getDate().toString().padStart(2, '0');

// Set the value of the date input to today's date
// dateInput.value = `${year}-${month}-${day}`;
bankjournal_date.value=`${year}-${month}-${day}`;


document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("#transactionTable tbody");

    tableBody.addEventListener('change', function (event) {
        const dropdown = event.target;
        if (dropdown.tagName === 'SELECT' && dropdown.id.startsWith('dropdown')) {
            const rowNum = dropdown.id.replace('dropdown', '');
            const catInput = document.getElementById(`cat${rowNum}`);
            const subInput = document.getElementById(`sub${rowNum}`);

            const selectedOption = dropdown.options[dropdown.selectedIndex];
            const subcategory = selectedOption.getAttribute('data-tokens');
            const category = selectedOption.getAttribute('data-value');

            console.log(`Selected Account Number for Row ${rowNum}:`, category);
            catInput.value = category;
            subInput.value = subcategory;
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // ...

    // Get a reference to the "Add Row" button
    const addRowButton = document.getElementById("addRowButton");

    // Function to add a new row to the table
    function addNewRow() {
        const table = document.getElementById("transactionTable");
        const newRow = table.insertRow(table.rows.length - 1); // Insert before the last row

        // Clone the cells from an existing row (you can choose any row as a template)
        const templateRow = table.rows[1]; // Assuming the second row (index 1) is your template
        for (let i = 0; i < templateRow.cells.length; i++) {
            const newCell = newRow.insertCell(i);
            newCell.innerHTML = templateRow.cells[i].innerHTML;
        }

        // Add a "Remove" button to the new row
        const removeCell = newRow.insertCell(templateRow.cells.length);
        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.classList.add("btn", "btn-danger", "remove-row-button");
        removeButton.textContent = "Remove";
        removeCell.appendChild(removeButton);

        // Attach a click event listener to the "Remove" button
        removeButton.addEventListener("click", function () {
            table.deleteRow(newRow.rowIndex);
            updateRowIds(); // Update the IDs after removing a row
        });

        // Update the IDs of the cloned elements to avoid duplicates
        const rowIndex = table.rows.length - 2; // Index of the new row (0-based)
        const elementsToChange = newRow.querySelectorAll("[id]");
        elementsToChange.forEach(function (element) {
            const id = element.getAttribute("id");
            const idParts = id.split(/\d+/);
            const num = rowIndex; // Adding 1 to match the row number
            element.setAttribute("id", idParts[0] + num);
            element.setAttribute("name", idParts[0] + num); // Also update the 'name' attribute if needed
            // element.value = ""; // Clear the input values in the new row
        });
    }

    // Add a click event listener to the "Add Row" button
    addRowButton.addEventListener("click", addNewRow);

    // Function to update the IDs of all rows after removing a row
    function updateRowIds() {
        const table = document.getElementById("transactionTable");
        for (let i = 1; i < table.rows.length - 1; i++) {
            const row = table.rows[i];
            const elementsToUpdate = row.querySelectorAll("[id]");
            elementsToUpdate.forEach(function (element) {
                const id = element.getAttribute("id");
                const idParts = id.split(/\d+/);
                const num = i - 1; // Subtract 1 to match the row number
                element.setAttribute("id", idParts[0] + num);
                element.setAttribute("name", idParts[0] + num); // Also update the 'name' attribute if needed
            });
        }
    }
});






// document.addEventListener("DOMContentLoaded", function () {
//     // ...

//     // Get a reference to the "Add Row" button
//     const addRowButton = document.getElementById("addRowButton");

//     // Function to add a new row to the table
//     function addNewRow() {
//         const table = document.getElementById("transactionTable");
//         const newRow = table.insertRow(table.rows.length - 1); // Insert before the last row

//         // Clone the cells from an existing row (you can choose any row as a template)
//         const templateRow = table.rows[1]; // Assuming the second row (index 1) is your template
//         for (let i = 0; i < templateRow.cells.length; i++) {
//             const newCell = newRow.insertCell(i);
//             newCell.innerHTML = templateRow.cells[i].innerHTML;
//         }

//         // Update the IDs of the cloned elements to avoid duplicates
//         const rowIndex = table.rows.length - 2; // Index of the new row (0-based)
//         console.log(rowIndex)
//         const elementsToChange = newRow.querySelectorAll("[id]");
//         elementsToChange.forEach(function (element) {
//             const id = element.getAttribute("id");
//             const idParts = id.split(/\d+/);
//             const num = rowIndex; // Adding 1 to match the row number
//             element.setAttribute("id", idParts[0] + num);
//             element.setAttribute("name", idParts[0] + num); // Also update the 'name' attribute if needed
//             // element.value = ""; // Clear the input values in the new row
//         });


//     }

//     // Add a click event listener to the "Add Row" button
//     addRowButton.addEventListener("click", addNewRow);
// });



document.addEventListener("DOMContentLoaded", function () {
    // Get references to elements

    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value; // Get the CSRF token from the form
    const form = document.getElementById("myActualForm");
    const submitButton = document.getElementById("submitForm");
    const clearFormButton = document.getElementById("clearFormButton");
    submitButton.addEventListener("click", function () {
        // Create a FormData object
        const formData = new FormData();
        const tableRows = form.querySelectorAll("tbody tr:not(:last-child)");
        const voucher = document.getElementById("voucher_no").value;
        const invoice_no = document.getElementById("invoice_no").value;
        const invoice_date = document.getElementById("invoice_date").value;

        const notes = document.getElementById("notes").value;
        formData.append(`notes`, notes);
        formData.append(`voucher`, voucher);
        formData.append(`invoice_no`, invoice_no);

        formData.append(`invoice_date`, invoice_date);

        tableRows.forEach((row, index) => {
            const select = row.querySelector("select");


            const cat = row.querySelector(`#cat${index + 1}`);
            const sub = row.querySelector(`#sub${index + 1}`);
            const nar = row.querySelector(`#nar${index + 1}`);
            const cre = row.querySelector(`#cre${index + 1}`);
            const deb = row.querySelector(`#deb${index + 1}`);
            console.log(index)
            // Append each field to the FormData object
            formData.append(`dropdown${index + 1}`, select.value);



            formData.append(`cat${index + 1}`, cat.value);
            formData.append(`sub${index + 1}`, sub.value);
            formData.append(`nar${index + 1}`, nar.value);
            formData.append(`cre${index + 1}`, cre.value);
            formData.append(`deb${index + 1}`, deb.value);
        });

        // Make an AJAX POST request
        fetch("/submit_journal/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken, // Include CSRF token
            },
            body: formData, // Use the FormData object
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response from the server
                updateModalData(data);
                // Hide loading animation and show checkmark
                setTimeout(function () {
                    $('#loading-animation').hide();
                    $('#success-checkmark').show();
                }, 1500);

            })
            .catch(error => {
                console.error("Error submitting the form:", error);
            });
    });
});

clearFormButton.addEventListener("click", function () {
    // Reset the form fields to their default values
    const form = document.getElementById("myActualForm");
    const tableRows = form.querySelectorAll("tbody tr");

    tableRows.forEach((row, index) => {
        const select = row.querySelector("select");
        const cat = row.querySelector(`#cat${index + 1}`);
        const sub = row.querySelector(`#sub${index + 1}`);
        const nar = row.querySelector(`#nar${index + 1}`);
        const cre = row.querySelector(`#cre${index + 1}`);
        const deb = row.querySelector(`#deb${index + 1}`);

        // Clear the form fields
        select.value = ''; // Clear the select value
        cat.value = ''; // Clear the cat input value
        sub.value = ''; // Clear the sub input value
        nar.value = ''; // Clear the nar input value
        cre.value = ''; // Clear the cre input value
        deb.value = ''; // Clear the deb input value
    });
});
// Update the modal content with data
function updateModalData(data) {
    const account = data.message.account;
    const voucherCode = data.message.voucherCode;
    const voucherNo = data.message.voucherNo;
    const modal = document.getElementById('myModal');
    const closeBtn = document.getElementsByClassName('close')[0];
    const closeBtn1 = document.getElementById('closeModalq');

    const voucherNoElement = document.getElementById('voucherNo');
    const voucherCodeElement = document.getElementById('voucherCode');
    const accountElement = document.getElementById('account');
    voucherNoElement.value = voucherNo;
    voucherCodeElement.value = voucherCode;
    accountElement.value = account;
    modal.style.display = 'block';  // Show the modal

    // Close the modal when the close button is clicked
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';

    });

    closeBtn1.addEventListener('click', () => {
        modal.style.display = 'none';
        const clearFormButton = document.getElementById("clearFormButton");

        // Simulate a click event on the clearFormButton
        clearFormButton.click();
    });
}







document.addEventListener("DOMContentLoaded", function () {
    // Attach input event listeners to elements with IDs starting with "cre" or "deb"
    const container = document.getElementById('transactionTable'); //
    const submitButton = document.getElementById('submitForm');
     // Assuming this is your input field for "Amount in Figures"

    // Function to calculate and log the totals
    function calculateAndLogTotals() {
        let creTotal = 0;
        let debTotal = 0;
        

        // Calculate the total of "cre" inputs
        const creInputs = container.querySelectorAll('input[id^="cre"]');

        creInputs.forEach(input => {
            const value2 = parseFloat(input.value) || 0; // Convert input value to a number, default to 0 if not a valid number
            creTotal += value2;
        });

        // Calculate the total of "deb" inputs
        const debInputs = container.querySelectorAll('input[id^="amt"]');
        debInputs.forEach(input => {
            const value1 = parseFloat(input.value) || 0; // Convert input value to a number, default to 0 if not a valid number
            debTotal += value1;


        });

        // Log the totals to the console
        var bankAmt_in_No = document.getElementById('bankAmt_in_No');

    
        const total_deb = document.getElementById("d_total");
        const total_cred = document.getElementById("c_total");
        total_deb.value = debTotal.toFixed(2)
        total_cred.value = creTotal.toFixed(2)

        // Set the total values in the corresponding input fields


        // Check if the difference between "Total Credit" and "Total Debit" is not zero
        if (creTotal == debTotal && debTotal==parseFloat(bankAmt_in_No.value) || 0 && creTotal !== 0 && debTotal !== 0) {
            // Enable the submit button
            submitButton.removeAttribute('disabled');
        } else {
            // Disable the submit button
            submitButton.setAttribute('disabled', 'disabled');
        }
    }
    container.addEventListener("input", calculateAndLogTotals);
});




document.addEventListener("DOMContentLoaded", function () {

    const voucher_numbe = document.getElementById("cashvoucher_no");
    const bankvoucher_number = document.getElementById("bankvoucher_no");
    reciept_voucher_number()


    function reciept_voucher_number() {
        // Make an AJAX request to your Django backend to get the next available account number
        fetch("/get_next_reciept_voucher_number/") // Replace with your Django endpoint URL
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    voucher_numbe.value = data.voucher_numbe;
                    bankvoucher_number.value = data.voucher_numbe;

                }
            })
            .catch(error => {
                console.error("Error fetching account number:", error);
            });
    }

    // You can also submit the form data to the Django backend using AJAX or a form submission, depending on your preference.
});


// const cashRadio = document.getElementById('cashRadio');
// const bankRadio = document.getElementById('bankRadio');
// const cashForm = document.getElementById('cashForm');
// const bankForm = document.getElementById('bankForm');


// cashRadio.addEventListener('change', () => {
//     if (cashRadio.checked) {
//         cashForm.style.display = 'block';
//         bankForm.style.display = 'none';

//     }
// });

// bankRadio.addEventListener('change', () => {
//     if (bankRadio.checked) {
//         cashForm.style.display = 'none';
//         bankForm.style.display = 'block';
//     }
// });


// You can also submit the form data to the Django backend using AJAX or a form submission, depending on your preference.

const cashRadio = document.getElementById('cashRadio');
const bankRadio = document.getElementById('bankRadio');
const cashLedgers = document.getElementById('cash_ledgers');
const initiallyDisplayedElements = [];

// Function to initialize the initially displayed elements
function initializeInitiallyDisplayedElements() {
    const colElements = document.querySelectorAll('.col');
    colElements.forEach(col => {
        if (window.getComputedStyle(col).display === 'block') {
            initiallyDisplayedElements.push(col);
        }
    });

}

// Call the initialization function when the page loads
initializeInitiallyDisplayedElements();

cashRadio.addEventListener('change', () => {
    if (cashRadio.checked) {
        // Hide elements that were not initially displayed as "block"
        const colElements = document.querySelectorAll('.col');
        colElements.forEach(col => {
            if (!initiallyDisplayedElements.includes(col)) {
                col.style.display = 'none';
            }
        });
    }
});

bankRadio.addEventListener('change', () => {
    
    if (bankRadio.checked) {
        // Show all elements with class "col"
        const colElements = document.querySelectorAll('.col');
        colElements.forEach(col => {
            col.style.display = 'block';
        });
    }
    cashLedgers.style.display = 'none';
    
});

