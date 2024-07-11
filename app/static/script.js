document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('createForm').addEventListener('click', function() {
        const rowDimensions = Array.from(document.getElementById('row_dimension').selectedOptions).map(option => option.value);
        const columnDimension = document.getElementById('column_dimension').value;

        fetch('/create_dynamic_form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                row_dimensions: rowDimensions,
                column_dimension: columnDimension
            }),
        })
        .then(response => response.json())
        .then(data => {
            const formContainer = document.getElementById('dynamicFormContainer');
            formContainer.innerHTML = data.html;
            setupFormSubmitHandler(columnDimension); 
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});

function setupFormSubmitHandler(columnDimension) {
    document.getElementById('dynamicForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);

        const jsonObject = {};
        formData.forEach((value, key) => {
            jsonObject[key] = value;
        });

        jsonObject['urunID'] = 1;  // test
        jsonObject['column_dimension'] = columnDimension;  
        console.log("Sending data:", jsonObject);

        fetch('/api/facts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonObject)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => { throw new Error(error.error); });
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            alert('Veriler başarıyla eklendi!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert(`Veri ekleme işleminde bir hata oluştu: ${error.message}`);
        });
    });
}
