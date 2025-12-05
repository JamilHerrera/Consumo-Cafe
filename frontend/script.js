document.addEventListener('DOMContentLoaded', function() {
    console.log("☕ Honduras Coffee Trends: Recursos cargados correctamente.");
    
    // Ejemplo: Agregar un efecto sutil al título si se desea
    const title = window.parent.document.querySelector('h1');
    if (title) {
        title.style.textShadow = "2px 2px 4px rgba(0,0,0,0.1)";
    }
});