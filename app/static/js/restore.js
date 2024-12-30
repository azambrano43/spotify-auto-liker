// Detect when a file is selected
document.getElementById('fileInput').addEventListener('change', function () {
    const fileInput = this;
    const fileNameElement = document.getElementById('fileName');
  
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
  
      // Check if file is .txt
      if (file.name.endsWith('.txt')) {
        fileNameElement.textContent = `File selected: ${file.name}`;
      } else {
        fileNameElement.textContent = "Please select a valid .txt file.";
      }
    } else {
      fileNameElement.textContent = "No file selected.";
    }
  });






  document.getElementById("restoreButton").addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0]; // Obtener el archivo seleccionado
  
    if (!file) {
      alert("Por favor, selecciona un archivo antes de continuar.");
      console.log("No file selected");
      return;
    }
  
    console.log("Archivo seleccionado:", file.name);

    // Mostrar el popup indicando que el proceso ha comenzado
    document.getElementById('backupPopup').style.display = 'flex';
  
    // Crear un objeto FormData para enviar el archivo
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      // Realizar la solicitud POST
      const response = await fetch("/process_like", {
        method: "POST",
        body: formData,
      });
  
      // Verificar si la respuesta es exitosa
      if (response.ok) {
        const result = await response.json();  // Procesar la respuesta como JSON
        console.log("Respuesta del servidor:", result);
  
        // Si el backend respondió con éxito
        if (result.status === 'success') {
          stopLoadingAnimation()
          // alert("Archivo procesado correctamente. Redirigiendo...");
          // Redirigir al usuario si el servidor devuelve una URL de redirección
          window.location.href = result.redirect_url;
        } else {
          // Si hay un error en el backend
          alert("Error en el procesamiento: " + result.message);
          stopLoadingAnimation()
          console.error("Error:", result.message);
        }
      } else {
        // Manejar errores en la respuesta
        alert("Error al procesar el archivo. Código de respuesta: " + response.status);
        const errorText = await response.text();  // Obtener el cuerpo del error
        stopLoadingAnimation()
        console.error("Error:", response.status, response.statusText, errorText);
      }
    } catch (error) {
      // Capturar cualquier error en la solicitud
      alert("Ocurrió un error al enviar el archivo.");
      stopLoadingAnimation()
      console.error("Error:", error);
    }
  });


// Función para detener la animación y ocultar el popup después de un retraso de 2 segundos
function stopLoadingAnimation() {
    setTimeout(function() {
        document.getElementById('backupPopup').style.display = 'none';
    }, 500);
}