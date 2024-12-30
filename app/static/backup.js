document.getElementById('backupButton').addEventListener('click', function() {
    // Recoger todos los checkboxes seleccionados
    const selectedScopes = [];
    document.querySelectorAll('input[name="scope"]:checked').forEach((checkbox) => {
        selectedScopes.push(checkbox.value);
    });

    if (selectedScopes.length > 0) {
        // Enviar los datos seleccionados al servidor usando fetch
        fetch('/backup_options', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ scopes: selectedScopes })  // Enviamos los valores seleccionados
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Si la solicitud fue exitosa, redirigimos a la ruta de procesamiento
                window.location.href = '/process_backup';
            } else {
                alert('No options selected');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred');
        });
    } else {
        alert('Please select at least one option');
    }
});


document.getElementById('logoutButton').addEventListener('click', function() {
    window.location.href = '/logout';  // Redirige a la URL de logout
});