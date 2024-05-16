// Obtener referencia al botón "Leer Datos"
const leerDatosBtn = document.getElementById('leer-datos-btn');

// Agregar evento de clic al botón "Leer Datos"
leerDatosBtn.addEventListener('click', function() {
    // Desactivar el botón "Leer Datos" al hacer clic en él
    leerDatosBtn.disabled = true;
});
