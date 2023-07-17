// const filterDropdown = document.getElementById('filter-dropdown');
// const tableRows = document.querySelectorAll('#customers_table tbody tr');

// filterDropdown.addEventListener('change', () => {
//     const selectedValue = filterDropdown.value;

//     tableRows.forEach(row => {
//         const statusResult = row.querySelector('.statusResult');

//         if (selectedValue === '' || statusResult.classList.contains(selectedValue)) {
//             row.style.display = '';
//         } else {
//             row.style.display = 'none';
//         }
//     });
// });

// var modal = document.getElementById("filter-modal");
//     var btn = document.querySelector(".filter-button");
//     var span = document.getElementsByClassName("close")[0];

//     btn.onclick = function () {
//         modal.style.display = "block";
//     }

//     span.onclick = function () {
//         modal.style.display = "none";
//     }

//     window.onclick = function (event) {
//         if (event.target == modal) {
//             modal.style.display = "none";
//         }
//     }

// Open filter modal
function openFilterModal() {
    document.getElementById("filter-modal").style.display = "block";
}

// Close filter modal
function closeFilterModal() {
    document.getElementById("filter-modal").style.display = "none";
}

function filterTable() {
    var filter = document.getElementById("filter-select").value;
    var startDate = new Date(document.getElementById("start-date-select").value);
    var endDate = new Date(document.getElementById("end-date-select").value);
    endDate.setDate(endDate.getDate() + 1); 

    var rows = document.querySelectorAll(".table_body table tbody tr");

    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var result = row.querySelector(".statusResult");
        var examinedAt = row.cells[4].textContent.split(',');
        examinedAt[0] = examinedAt[0]+","
        console.log(examinedAt.join(' ')); 
        examinedAt = new Date(examinedAt.join(' '));
        
        if (
            (filter === "all" || result.classList.contains(filter)) &&
            (isNaN(startDate) || examinedAt >= startDate) &&
            (isNaN(endDate) || examinedAt < endDate)
        ) {
            console.log(result.classList)
            console.log(result)
            console.log(row)
            row.style.display = "table-row";
        } else {
            row.style.display = "none";
        }
    }
}
