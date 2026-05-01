// Archivo main.js adaptado

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-cerrar alertas
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-important)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Búsqueda en tablas
    const searchInput = document.getElementById('searchArticulo');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const isMatch = text.includes(searchTerm);
                row.style.display = isMatch ? '' : 'none';
            });
        });
    }

    // Modo edición de perfil
    const editBtn = document.querySelector('.edit-profile-btn');
    const cancelBtn = document.querySelector('.cancel-edit-btn');
    const viewMode = document.querySelector('.view-mode');
    const editMode = document.querySelector('.edit-mode');
    
    if (editBtn && cancelBtn && viewMode && editMode) {
        editBtn.addEventListener('click', function() {
            viewMode.style.display = 'none';
            editMode.style.display = 'block';
            this.style.display = 'none';
        });
        
        cancelBtn.addEventListener('click', function() {
            viewMode.style.display = 'block';
            editMode.style.display = 'none';
            editBtn.style.display = 'inline-block';
        });
    }
});
