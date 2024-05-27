
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
