document.getElementById('client-form').addEventListener('submit', function(event) {
    var cuit = document.getElementById('cuit').value;
    if (!/^\d{11}$/.test(cuit)) {
        alert('El CUIT debe tener 11 dígitos.');
        event.preventDefault();
    }
});

function filterTable() {
    let nameFilter = document.getElementById('filter-name').value.toLowerCase();
    let emailFilter = document.getElementById('filter-email').value.toLowerCase();
    let table = document.getElementById('client-table');
    let tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        let tdName = tr[i].getElementsByTagName('td')[0];
        let tdEmail = tr[i].getElementsByTagName('td')[3];
        if (tdName && tdEmail) {
            let nameValue = tdName.textContent || tdName.innerText;
            let emailValue = tdEmail.textContent || tdEmail.innerText;
            if (nameValue.toLowerCase().indexOf(nameFilter) > -1 && emailValue.toLowerCase().indexOf(emailFilter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }       
    }
}

function deleteClient(btn) {
    let row = btn.parentNode.parentNode;
    let name = row.getElementsByTagName('td')[0].innerText;
    let email = row.getElementsByTagName('td')[3].innerText;

    if (confirm(`Are you sure you want to delete client ${name}?`)) {
        // Remove the row from the table
        row.parentNode.removeChild(row);

        // Call the server to delete the client (this part requires server-side implementation)
        // fetch(`/delete-client?email=${email}`, { method: 'DELETE' })
        //     .then(response => response.json())
        //     .then(data => console.log(data))
        //     .catch(error => console.error('Error:', error));
    }
}
