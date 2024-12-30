document.getElementById('backupButton').addEventListener('click', function() {
    // Recoger todos los checkboxes seleccionados
    const selectedScopes = [];
    document.querySelectorAll('input[name="scope"]:checked').forEach((checkbox) => {
        selectedScopes.push(checkbox.value);
    });

    if (selectedScopes.length > 0) {
        // Mostrar el popup indicando que el proceso ha comenzado
        document.getElementById('backupPopup').style.display = 'flex';

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
                // Aquí esperamos que se complete el respaldo antes de continuar
                return fetch('/process_backup')
                    .then(response => {
                        if (response.ok) {
                            // Detener la animación
                            stopLoadingAnimation();

                            // Iniciar la descarga del archivo
                            window.location.href = response.url;
                        } else {
                            alert('An error occurred while processing the backup.');
                        }
                    });
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

// Función para detener la animación y ocultar el popup después de un retraso de 2 segundos
function stopLoadingAnimation() {
    setTimeout(function() {
        document.getElementById('backupPopup').style.display = 'none';
    }, 2000); // 2000 milisegundos = 2 segundos
}


document.getElementById('logoutButton').addEventListener('click', function() {
    window.location.href = '/logout';  // Redirige a la URL de logout
});