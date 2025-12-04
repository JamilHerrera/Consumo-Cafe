document.addEventListener("DOMContentLoaded", function() {
    // Animación de fade-in en títulos
    let headers = document.querySelectorAll("h1, h2, h3");
    headers.forEach(h => {
        h.style.opacity = 0;
        setTimeout(() => {
            h.style.transition = "opacity 2s";
            h.style.opacity = 1;
        }, 500);
    });
});
