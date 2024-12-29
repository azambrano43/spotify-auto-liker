document.querySelectorAll('.item').forEach(item => {
    item.addEventListener('click', () => {
      const url = item.getAttribute('data-url'); // Obtén la URL del atributo data-url
      window.location.href = url; // Redirige al archivo HTML correspondiente
    });
  });
  